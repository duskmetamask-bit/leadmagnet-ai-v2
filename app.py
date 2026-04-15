"""
LeadMagnet AI — Turn any URL into a lead magnet in 30 seconds
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import os
import io
import re
from datetime import datetime

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_MODEL  = "gpt-4o-mini"

# ── URL Scraping ─────────────────────────────────────────────────────────

def scrape_url(url: str) -> str:
    """Fetch and extract clean text from a URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LeadMagnetAI/1.0; +https://emvyai.com)"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Remove noise
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    # Try main content
    main = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile(r"content|post|article|entry", re.I))
    text = (main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True))

    # Clean up
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(lines[:500])  # Cap at 500 lines

# ── AI Generation ───────────────────────────────────────────────────────

def build_prompt(content: str) -> str:
    return (
        "You are an expert content marketer. Analyze the content below and create a complete lead magnet.\n\n"
        "Create the following sections:\n"
        "1. **Title** — catchy, valuable title for the lead magnet\n"
        "2. **Hook** — compelling opening that hooks the reader immediately\n"
        "3. **Key Takeaways** — 5-8 bullet points of the most valuable insights (each 1-3 sentences)\n"
        "4. **Action Steps** — 3-5 concrete actionable steps the reader can take today\n"
        "5. **Bonus Tip** — one extra powerful insight or resource\n"
        "6. **CTA** — soft call to action pointing them to next step (e.g. 'Want more? Book a free call')\n\n"
        f"CONTENT TO REPURPOSE:\n\"\"\"\n{content[:4000]}\n\"\"\"\n\n"
        "Format each section clearly with headers. Keep it punchy, practical, and conversion-focused."
    )

def generate_leadmagnet(url: str, api_key: str) -> str:
    content = scrape_url(url)
    if len(content) < 200:
        return "ERROR: Could not extract enough content from that URL. Try a different page."

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "user", "content": build_prompt(content)}],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content

def format_markdown(content: str, url: str) -> str:
    title_match = re.search(r"\*\*Title[:\*\*]\s*\n?(.*)", content)
    title = title_match.group(1).strip() if title_match else "Lead Magnet"
    date = datetime.now().strftime("%Y-%m-%d")
    return f"# {title}\n\n*Generated from: {url} | {date}*\n\n---\n\n{content}\n\n---\n*Created with LeadMagnet AI — [Book your free AI audit →](https://calendly.com/emvyai/free-ai-chat)*"

# ── App ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="LeadMagnet AI",
    page_icon="🧲",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, .stApp { background: #0F172A; color: #F1F5F9; font-family: 'Inter', sans-serif; }

.stTextInput > div > div > input {
    background: #1E293B; color: #F1F5F9; border: 1px solid #14B8A6;
    font-size: 1.1rem; border-radius: 8px; padding: 0.6rem 1rem;
}
.stTextArea > div > div > textarea {
    background: #1E293B; color: #F1F5F9; border: 1px solid #14B8A6;
    border-radius: 8px;
}
.stButton > button {
    background: #14B8A6; color: #0F172A; font-weight: 700; border: none;
    border-radius: 8px; padding: 0.7rem 2.5rem; font-size: 1.05rem;
    transition: background 0.2s;
}
.stButton > button:hover { background: #0D9488; }

.result-box {
    background: #1E293B; border: 1px solid #14B8A6; border-radius: 12px;
    padding: 1.5rem 2rem; margin-top: 1.5rem;
}
section[data-testid="stSidebar"] { background: #162032; }
h1 { color: #F1F5F9; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<p style="color:#14B8A6;font-weight:900;font-size:1.3rem;letter-spacing:0.1em;">🧲 LEADMAGNET AI</p>
<h1 style="font-size:2.2rem;font-weight:900;">Turn Any URL Into a <span style="color:#14B8A6;">Lead Magnet</span> in 30 Seconds</h1>
<p style="color:#94A3B8;font-size:1.05rem;">Paste a blog post, article, or webpage → get a structured lead magnet: takeaways, action steps, CTA.</p>
<br/>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💰 Pricing")
    st.markdown("""
    | Tier | Price | Leads |
    |------|-------|-------|
    | **Free** | $0 | 3/month |
    | **Pro** | $9/mo | 50/month |
    | **Agency** | $29/mo | Unlimited |
    """)
    st.markdown("---")
    st.markdown("### ℹ️ How it works")
    st.markdown("""
    1. **Paste a URL** — any article, blog post, or page
    2. **AI extracts** — the key ideas and insights
    3. **Lead magnet generated** — takeaways, action steps, CTA
    4. **Download as .md** — ready to use or convert to PDF
    """)
    st.markdown("---")
    st.markdown("**Example uses:**")
    st.markdown("""
    - Blog posts → PDF guides
    - YouTube transcripts → checklists
    - Articles → email sequences
    - Reports → slide decks
    """)

# Main input
url = st.text_input("🔗 Paste any URL", placeholder="https://example.com/blog-post")
col_btn, col_status = st.columns([1, 2])

with col_btn:
    generate = st.button("🧲 Generate Lead Magnet", use_container_width=True)

if generate:
    if not url.strip():
        st.error("⚠️ Please paste a URL first.")
    elif not OPENAI_API_KEY:
        st.error("⚠️ OpenAI API key not set. Add OPENAI_API_KEY to your environment.")
    else:
        with st.spinner("🔍 Scraping content..."):
            try:
                result = generate_leadmagnet(url, OPENAI_API_KEY)
                if result.startswith("ERROR"):
                    st.error(result)
                else:
                    st.session_state["result"] = result
                    st.session_state["url"] = url
                    st.success("✅ Lead magnet generated!")
            except Exception as e:
                st.error(f"❌ Failed: {e}")

# Display
if "result" in st.session_state:
    st.markdown("---")
    st.markdown("## 📋 Your Lead Magnet")
    st.markdown(f"<div class='result-box'>{st.session_state['result'].replace(chr(10), '<br/>')}</div>", unsafe_allow_html=True)

    md = format_markdown(st.session_state["result"], st.session_state["url"])
    fname = f"lead-magnet-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
    st.download_button(
        label="📥 Download as Markdown",
        data=md,
        file_name=fname,
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown("""
    <br/>
    <p style="text-align:center;color:#14B8A6;font-size:0.95rem;">
    Want a full AI audit of your business? → <a href="https://calendly.com/emvyai/free-ai-chat" style="color:#14B8A6;">Book a free call</a>
    </p>
    """, unsafe_allow_html=True)

st.markdown("""
<br/>
<p style="text-align:center;color:#475569;font-size:0.8rem;">
LeadMagnet AI · Free: 3/month · Pro: $9/mo · Built with OpenAI GPT-4o
</p>
""", unsafe_allow_html=True)
