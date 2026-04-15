# LeadMagnet AI 🧲

Turn any URL into a polished, downloadable lead magnet guide — in seconds.

## What It Does

1. Paste a URL (article, blog post, landing page)
2. AI scrapes and summarizes the content
3. Outputs a formatted lead magnet with:
   - Catchy, benefit-driven title
   - Key takeaways
   - Problem/solution framing
   - Actionable insights
   - Concrete action items
4. Download as **Markdown** or **PDF**

---

## Quick Start

### Run Locally

```bash
cd prototype-leadmagnet

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Run
streamlit run app.py
```

Visit `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Set `OPENAI_API_KEY` in Streamlit Cloud secrets
5. Deploy

---

## Project Structure

```
prototype-leadmagnet/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── README.md               # This file
└── .streamlit/
    └── config.toml         # Dark theme config
```

---

## Monetization Plan

### Tier 1 — Free (Current)
- **3 lead magnets / month**
- Markdown + PDF export
- Full feature access
- **Purpose:** Lead capture, prove value, grow email list

### Tier 2 — Pro ($9/mo via Stripe)
- Unlimited lead magnet generations
- Priority queue (faster processing)
- PDF export included
- Early access to new features
- Bulk generation (up to 10 URLs at once)
- Custom branding (own logo on PDFs)

### Tier 3 — Agency ($29/mo)
- Everything in Pro
- 50 unlimited generations
- Team seats (up to 5)
- API access
- White-label PDF output
- Priority support

### Revenue Model
| Tier | Price | Target |
|------|-------|--------|
| Free | $0 | Lead capture |
| Pro | $9/mo | Hobbyists, freelancers |
| Agency | $29/mo | Small agencies, content teams |

**Conversion target:** 5% free → paid within 30 days

---

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Scraping:** requests + BeautifulSoup4
- **AI:** OpenAI GPT-4o-mini
- **PDF:** ReportLab
- **Deploy:** Streamlit Cloud (free tier available)

---

## Key Design Decisions

1. **Dark teal aesthetic** — signals "AI tool", high-contrast, modern
2. **URL-based input** — no login barrier for first use
3. **Immediate value** — see result before any paywall
4. **Dual export** — Markdown (free) + PDF (pro unlock potential)
5. **Usage cap** — 3/month free → drives conversion without being annoying

---

## Roadmap

- [ ] Stripe integration for Pro/Agency tiers
- [ ] Email capture before download
- [ ] Lead magnet templates (case study, checklist, whitepaper)
- [ ] Bulk URL processing
- [ ] API endpoint for power users
- [ ] Custom branding for Agency tier
- [ ] Lead magnet gallery (browse community outputs)
