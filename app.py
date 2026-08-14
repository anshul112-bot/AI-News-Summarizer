from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)

# Configure your API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

def extract_article_text(url):
    """Extract article text from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:3000]  # Limit to 3000 chars
    except Exception as e:
        return None

def summarize_text(text, length='medium'):
    """Summarize text using OpenAI API"""
    if not OPENAI_API_KEY:
        # Fallback: simple extractive summarization
        return generate_fallback_summary(text, length)
    
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        
        length_prompts = {
            'short': '3-4',
            'medium': '5-7',
            'long': '8-10'
        }
        
        bullet_count = length_prompts.get(length, '5-7')
        
        prompt = f"""Summarize the following article in {bullet_count} bullet points. 
Each bullet point should be concise and capture a key fact.
Focus on the most important information.

Article:
{text}

Provide only the bullet points, starting each with a dash (-)."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful news summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return generate_fallback_summary(text, length)

def generate_fallback_summary(text, length='medium'):
    """Generate a simple fallback summary when API is unavailable"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s for s in sentences if len(s) > 20]
    
    length_map = {'short': 3, 'medium': 5, 'long': 8}
    num_sentences = min(length_map.get(length, 5), len(sentences))
    
    # Simple extractive summarization - take first and distributed sentences
    if num_sentences <= len(sentences):
        step = len(sentences) / num_sentences
        selected = [sentences[int(i * step)] for i in range(num_sentences)]
    else:
        selected = sentences
    
    bullets = [f"- {s.strip()}" for s in selected if s.strip()]
    return '\n'.join(bullets)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """API endpoint for summarization"""
    data = request.get_json()
    article_text = data.get('text', '').strip()
    article_url = data.get('url', '').strip()
    summary_length = data.get('length', 'medium')
    
    if not article_text and not article_url:
        return jsonify({'error': 'Please provide either text or URL'}), 400
    
    # Extract text from URL if provided
    if article_url:
        extracted = extract_article_text(article_url)
        if not extracted:
            return jsonify({'error': 'Could not extract content from URL'}), 400
        article_text = extracted
    
    if len(article_text.strip()) < 50:
        return jsonify({'error': 'Article text is too short'}), 400
    
    try:
        summary = summarize_text(article_text, summary_length)
        return jsonify({
            'success': True,
            'summary': summary,
            'text_length': len(article_text)
        })
    except Exception as e:
        return jsonify({'error': f'Summarization failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
