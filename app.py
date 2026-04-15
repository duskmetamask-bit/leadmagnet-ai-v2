import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import io
import re
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(
    page_title="LeadMagnet AI",
    page_icon="🧲",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0F172A;
}

.title-wrapper {
    text-align: center;
    padding: 2rem 0 1rem;
}

.title-wrapper h1 {
    font-size: 3.5rem;
    font-weight: 900;
    color: #F1F5F9;
    letter-spacing: -1px;
}

.title-wrapper h1 span {
    color: #14B8A6;
}

.title-wrapper p {
    color: #94A3B8;
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

.block-container {
    padding-top: 1rem;
}

.result-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
    color: #F1F5F9;
}

.result-card h2 {
    color: #14B8A6;
    font-size: 1.4rem;
    margin-bottom: 1rem;
}

.result-card ul {
    padding-left: 1.5rem;
}

.result-card li {
    color: #CBD5E1;
    margin-bottom: 0.5rem;
}

.cta-box {
    background: linear-gradient(135deg, #0F172A 0%, #14B8A6 200%);
    border: 1px solid #14B8A6;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin-top: 2rem;
    color: #F1F5F9;
}

.cta-box h3 {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.cta-box p {
    color: #94A3B8;
    margin-bottom: 1rem;
}

div[data-testid="stTextInput"] label,
div[data-testid="stButton"] label {
    color: #F1F5F9 !important;
}

.stTextInput > div > div > input {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #F1F5F9 !important;
    font-size: 1rem !important;
    border-radius: 10px !important;
}

.stTextInput > div > div > input::placeholder {
    color: #64748B !important;
}

.stButton > button {
    background-color: #14B8A6 !important;
    color: #0F172A !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #0D9488 !important;
    color: #F1F5F9 !important;
}

.download-col .stDownloadButton > button {
    background-color: #1E293B !important;
    color: #14B8A6 !important;
    border: 1px solid #14B8A6 !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
}

.usage-badge {
    display: inline-block;
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 100px;
    padding: 0.3rem 1rem;
    font-size: 0.85rem;
    color: #94A3B8;
    margin-bottom: 1.5rem;
}

.usage-badge strong {
    color: #14B8A6;
}

.info-box {
    background: #1E293B;
    border-left: 4px solid #14B8A6;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.5rem;
    color: #CBD5E1;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

.tier-info {
    background: linear-gradient(135deg, #1E293B, #0F172A);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 2rem;
    color: #F1F5F9;
}

.tier-info h3 {
    color: #14B8A6;
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
}

.tier-info .tier-row {
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    border-bottom: 1px solid #1E293B;
    color: #CBD5E1;
    font-size: 0.9rem;
}

.tier-info .tier-row:last-child {
    border-bottom: none;
}

.tier-info .tier-row .free {
    color: #14B8A6;
    font-weight: 700;
}

.tier-info .tier-row .pro {
    color: #F59E0B;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-wrapper">
    <h1>LeadMagnet <span>AI</span></h1>
    <p>Turn any URL into a polished lead magnet — in seconds</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "usage_count" not in st.session_state:
    st.session_state["usage_count"] = 0
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None
if "source_url" not in st.session_state:
    st.session_state["source_url"] = ""
if "generated_at" not in st.session_state:
    st.session_state["generated_at"] = None

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧲 LeadMagnet AI")
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("1. Paste a URL")
    st.markdown("2. We extract & summarize the content")
    st.markdown("3. Download your lead magnet")
    st.markdown("---")
    st.markdown("**Pricing:**")
    st.markdown("- 🆓 Free: **3 lead magnets / month**")
    st.markdown("- 💎 Pro: **Unlimited** — $9/mo")
    st.markdown("---")
    if st.session_state["usage_count"] > 0:
        st.markdown(f"**Used today:** {st.session_state['usage_count']} / 3")
    st.markdown("---")
    st.caption("Built with ❤️ by DAWN Labs AI")

# ── Helpers ─────────────────────────────────────────────────────────────────
MAX_FREE = 3

def extract_text_from_url(url: str) -> str:
    """Fetch and extract clean text from a URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Remove noise
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    # Collapse blank lines
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(lines[:3000])  # cap at ~3000 lines for token safety

def generate_lead_magnet(url: str, content: str) -> str:
    """Use GPT-4o-mini to generate a lead magnet from raw content."""
    prompt = f"""You are a world-class content strategist. A user wants to turn the following article/page into a compelling "lead magnet" — a downloadable guide that provides immediate value and captures email signups.

SOURCE URL: {url}

PAGE CONTENT:
{content[:6000]}

---

Generate a complete lead magnet in this exact format:

# [TITLE — catchy, benefit-driven]

> One-sentence hook that makes someone want to read this

## 📌 Key Takeaways
- [3-5 bullet points — the most valuable insights from this content]

## 🎯 The Problem
[2-3 sentences describing the pain point this content addresses]

## ✅ The Solution / Key Insights

### [Insight 1 Heading]
[2-3 sentences explaining this insight with actionable detail]

### [Insight 2 Heading]
[2-3 sentences]

### [Insight 3 Heading]
[2-3 sentences]

(Add more subsections as needed based on content depth)

## 🛠 Action Items
- [3-5 concrete, numbered action steps the reader can take right now]

## 💡 Bonus Insight
[One surprising or counterintuitive takeaway that adds unique value]

---

## Rules:
- Write for a general business audience
- Be specific — use numbers, names, and concrete details from the source
- Action items must be immediately actionable
- Tone: confident, sharp, value-forward — never vague
- If the source content is thin, supplement with your own domain knowledge but label it clearly
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are LeadMagnet AI — a world-class content strategist. Always output valid markdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content

def build_pdf(markdown_text: str) -> bytes:
    """Convert markdown to a simple PDF using ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib import colors

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="LeadMagnet AI — Generated Guide",
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=10,
        leading=28,
    )
    heading1_style = ParagraphStyle(
        "CustomH1",
        parent=styles["Heading1"],
        fontSize=14,
        textColor=colors.HexColor("#14B8A6"),
        spaceBefore=16,
        spaceAfter=6,
        leading=18,
    )
    heading2_style = ParagraphStyle(
        "CustomH2",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=12,
        spaceAfter=4,
        leading=16,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#334155"),
        leading=14,
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#334155"),
        leading=14,
        leftIndent=16,
        bulletIndent=4,
        spaceAfter=3,
    )
    hook_style = ParagraphStyle(
        "Hook",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#64748B"),
        leading=15,
        spaceAfter=12,
        leftIndent=8,
        rightIndent=8,
    )

    story = []

    # Parse markdown into story elements
    lines = markdown_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# ") and not line.startswith("##"):
            # Main title
            title_text = line[2:].strip()
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 8))
        elif line.startswith("## "):
            # Section heading
            heading_text = line[3:].strip()
            story.append(Paragraph(heading_text, heading1_style))
        elif line.startswith("### "):
            heading_text = line[4:].strip()
            story.append(Paragraph(heading_text, heading2_style))
        elif line.startswith(">"):
            # Blockquote / hook
            hook_text = line[1:].strip()
            story.append(Paragraph(f"<i>{hook_text}</i>", hook_style))
        elif line.startswith("- "):
            bullet_text = line[2:].strip()
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
        elif re.match(r"^\d+\.\s", line):
            # Numbered item
            item_text = re.sub(r"^\d+\.\s", "", line).strip()
            story.append(Paragraph(f"❖ {item_text}", bullet_style))
        elif line.strip() == "":
            story.append(Spacer(1, 6))
        else:
            # Body paragraph
            # Clean markdown bold/italic
            clean = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            clean = re.sub(r"\*(.+?)\*", r"<i>\1</i>", clean)
            if clean.strip():
                story.append(Paragraph(clean, body_style))

        i += 1

    # Footer
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Generated by LeadMagnet AI — dawnlabsai.com</i>",
        ParagraphStyle("footer", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#94A3B8"))
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ── Main UI ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input(
        "Paste a URL to transform into a lead magnet",
        placeholder="https://example.com/article",
        help="Works best with blog posts, articles, and guides",
    )

with col2:
    st.markdown("")  # spacer
    generate_clicked = st.button("🧲 Generate Lead Magnet")

# ── Usage gate ───────────────────────────────────────────────────────────────
if generate_clicked:
    if not url_input.strip():
        st.error("⚠️ Please enter a URL first.")
    elif st.session_state["usage_count"] >= MAX_FREE:
        st.error(f"🚫 You've hit your free limit of {MAX_FREE}/month. Upgrade to Pro for unlimited lead magnets.")
        st.stop()
    else:
        with st.spinner("🔍 Scraping content…"):
            try:
                raw_text = extract_text_from_url(url_input.strip())
            except Exception as e:
                st.error(f"❌ Failed to fetch URL: {e}")
                st.stop()

        if len(raw_text) < 200:
            st.error("❌ Not enough content found. Try a different URL.")
            st.stop()

        with st.spinner("🤖 Generating your lead magnet…"):
            try:
                lead_magnet = generate_lead_magnet(url_input.strip(), raw_text)
            except Exception as e:
                st.error(f"❌ AI generation failed: {e}")
                st.stop()

        st.session_state["usage_count"] += 1
        st.session_state["last_result"] = lead_magnet
        st.session_state["source_url"] = url_input.strip()
        st.session_state["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        st.success("✅ Lead magnet generated!")

# ── Display result ──────────────────────────────────────────────────────────
if st.session_state["last_result"]:
    result = st.session_state["result"] if "result" in st.session_state else st.session_state["last_result"]

    st.markdown("---")
    st.markdown(f"**Source:** {st.session_state['source_url']}")
    if st.session_state["generated_at"]:
        st.caption(f"Generated: {st.session_state['generated_at']} — {st.session_state['usage_count']}/{MAX_FREE} free uses")

    st.markdown(st.session_state["last_result"], unsafe_allow_html=False)

    # ── Download buttons ──────────────────────────────────────────────────────
    lm = st.session_state["last_result"]
    url_slug = re.sub(r"[^a-z0-9]+", "-", st.session_state["source_url"].lower())
    url_slug = url_slug[:50]
    md_filename = f"leadmagnet-{url_slug}.md"

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "📄 Download as Markdown",
            lm,
            file_name=md_filename,
            mime="text/markdown",
            use_container_width=True,
        )

    with c2:
        try:
            pdf_bytes = build_pdf(lm)
            st.download_button(
                "📕 Download as PDF",
                pdf_bytes,
                file_name=f"leadmagnet-{url_slug}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.button("📕 Download as PDF", disabled=True, use_container_width=True)
            st.caption(f"PDF generation error: {e}")

    # ── CTA ──────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="cta-box">
        <h3>🚀 Want unlimited lead magnets?</h3>
        <p>Upgrade to Pro for <strong>$9/month</strong> — unlimited generations, priority processing, early access to new features.</p>
        <p><a href="#" style="color:#14B8A6; font-weight:700;">👉 Upgrade to Pro</a></p>
    </div>
    """, unsafe_allow_html=True)

# ── Tier info ────────────────────────────────────────────────────────────────
if not st.session_state["last_result"]:
    st.markdown("---")
    st.markdown("""
    <div class="tier-info">
        <h3>💰 Pricing</h3>
        <div class="tier-row">
            <span class="free">🆓 Free</span>
            <span>3 lead magnets / month · All core features · Markdown export</span>
        </div>
        <div class="tier-row">
            <span class="pro">💎 Pro</span>
            <span>Unlimited lead magnets · PDF export · Priority queue · Early access</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
