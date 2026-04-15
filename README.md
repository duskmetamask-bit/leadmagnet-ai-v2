# LeadMagnet AI

Turn any URL into a lead magnet in 30 seconds.

## What It Does
- Paste a URL (article, blog, page)
- AI scrapes and extracts key content
- Outputs a structured lead magnet: title, hook, key takeaways, action steps, CTA
- Download as Markdown

## Tech Stack
- Streamlit (frontend)
- BeautifulSoup4 (scraping)
- OpenAI GPT-4o-mini (AI)
- reportlab (PDF export - optional)

## Setup

```bash
# Install deps
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY=sk-...

# Run
streamlit run app.py
```

## Deployment to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy

## Pricing
- Free: 3 lead magnets/month
- Pro: $9/month (50/month)
- Agency: $29/month (unlimited)

## Files
- `app.py` — main Streamlit app
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — theme config
