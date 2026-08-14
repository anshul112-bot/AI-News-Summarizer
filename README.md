# AI News Summarizer

A web application that generates concise bullet-point summaries of news articles using AI.

## Features ✨

- **Text Input**: Paste article text directly
- **URL Input**: Provide a link to fetch and summarize articles
- **Bullet-Point Summaries**: Get 3-10 key points from any article
- **Adjustable Length**: Choose between short, medium, and long summaries
- **Copy & Export**: Copy to clipboard or download as text file
- **Fast Processing**: Summaries generated in seconds

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "AI news Summarize"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key (optional - the app works without it with fallback summarization)
   ```bash
   copy .env.example .env
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open in your browser**
   - Navigate to `http://localhost:5000`
   - You should see the AI News Summarizer interface

3. **Start summarizing!**
   - Paste article text or enter a URL
   - Select summary length (short/medium/long)
   - Click "Summarize" and get your results

## How It Works

### Without OpenAI API
The app includes a fallback summarization method that:
- Uses extractive summarization (selecting key sentences)
- Works without any API keys
- Good for basic functionality testing

### With OpenAI API (Recommended)
- Provides higher quality, abstractive summaries
- Better understanding of article context
- More accurate key point extraction

Get your free API key: https://platform.openai.com/account/api-keys

## Project Structure

```
AI news Summarize/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main HTML interface
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend logic
```

## API Endpoints

### POST /api/summarize

Generates a summary of an article.

**Request:**
```json
{
  "text": "Full article text (optional if URL provided)",
  "url": "https://example.com/article (optional if text provided)",
  "length": "short|medium|long"
}
```

**Response:**
```json
{
  "success": true,
  "summary": "- Key point 1\n- Key point 2\n...",
  "text_length": 5000
}
```

## Troubleshooting

### Port already in use
- Change the port in `app.py` (line: `app.run(debug=True, port=5000)`)
- Or kill the process using port 5000

### Module not found errors
- Ensure your virtual environment is activated
- Run `pip install -r requirements.txt` again

### URL extraction fails
- Some sites require authentication or have robots.txt restrictions
- Try copying the article text instead
- Check the article URL is accessible

### Poor summary quality
- Add your OpenAI API key to `.env` for better results
- Try different summary lengths
- Some fallback summaries work better on longer articles

## Future Enhancements

- Multi-language support
- Batch processing of multiple articles
- Browser extension
- RSS feed integration
- Sentiment analysis
- Save/export history

## License

MIT License - Feel free to use and modify as needed

## Support

For issues or suggestions, please check the requirements.txt and ensure all dependencies are installed correctly.
