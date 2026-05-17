import streamlit as st
import os
from dotenv import load_dotenv
from summarizer import summarize_transcript
from transcriber import transcribe_audio
from file_parser import extract_text_from_file

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MeetMind – AI Meeting Summarizer",
    page_icon="🎙️",
    layout="centered"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main { background-color: #0d0d0d; color: #f0ede6; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #0d0d0d 0%, #111827 100%);
    min-height: 100vh;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f9c74f, #f3722c, #f94144);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: #9ca3af;
    font-weight: 300;
    margin-bottom: 2rem;
}

.summary-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-top: 1rem;
    color: #f0ede6;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #f9c74f;
    margin-bottom: 0.5rem;
}

.action-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.92rem;
    color: #d1d5db;
}

.badge {
    background: rgba(249,199,79,0.15);
    color: #f9c74f;
    border: 1px solid rgba(249,199,79,0.3);
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border: 1.5px dashed rgba(249,199,79,0.35);
    border-radius: 12px;
    padding: 1rem;
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #f0ede6 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stButton > button {
    background: linear-gradient(90deg, #f9c74f, #f3722c) !important;
    color: #0d0d0d !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover { opacity: 0.85 !important; }

.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: #9ca3af !important;
}

.stTabs [aria-selected="true"] {
    color: #f9c74f !important;
}

.stRadio label { color: #d1d5db !important; font-size: 0.9rem !important; }

.footer-note {
    text-align: center;
    color: #4b5563;
    font-size: 0.78rem;
    margin-top: 3rem;
    font-family: 'DM Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">MeetMind 🎙️</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Drop your meeting. Get the essence — summaries, decisions & action items instantly.</div>', unsafe_allow_html=True)

# ─── API Key Check ───────────────────────────────────────────────────────────
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found. Please add it to your `.env` file.")
    st.stop()

# ─── Input Tabs ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📄 Upload File", "🎙️ Upload Audio", "✏️ Paste Text"])

transcript_text = ""
input_source = ""

with tab1:
    uploaded_file = st.file_uploader(
        "Upload transcript (.txt, .pdf, .docx)",
        type=["txt", "pdf", "docx"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        with st.spinner("Parsing file..."):
            transcript_text = extract_text_from_file(uploaded_file)
        input_source = uploaded_file.name
        st.success(f"✅ Loaded `{uploaded_file.name}` — {len(transcript_text.split())} words")

with tab2:
    audio_file = st.file_uploader(
        "Upload audio (.mp3, .mp4, .wav, .m4a)",
        type=["mp3", "mp4", "wav", "m4a"],
        label_visibility="collapsed"
    )
    if audio_file:
        with st.spinner("Transcribing audio with Gemini..."):
            transcript_text = transcribe_audio(audio_file, api_key)
        input_source = audio_file.name
        if transcript_text:
            st.success(f"✅ Transcribed `{audio_file.name}`")
            with st.expander("View transcript"):
                st.text(transcript_text[:2000] + ("..." if len(transcript_text) > 2000 else ""))

with tab3:
    pasted = st.text_area(
        "Paste your meeting transcript here",
        height=200,
        placeholder="Paste raw meeting transcript text here...",
        label_visibility="collapsed"
    )
    if pasted.strip():
        transcript_text = pasted
        input_source = "pasted text"

# ─── Options ────────────────────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    summary_style = st.radio(
        "Summary Style",
        ["Concise (3–5 bullets)", "Detailed (paragraph)", "Executive Brief"],
        index=0
    )
with col2:
    output_language = st.radio(
        "Output Language",
        ["English", "Hindi", "Hinglish"],
        index=0
    )

# ─── Summarize Button ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
summarize_btn = st.button("✨ Summarize Meeting")

if summarize_btn:
    if not transcript_text.strip():
        st.warning("Please provide a transcript first.")
    else:
        with st.spinner("Analyzing meeting with Gemini..."):
            result = summarize_transcript(transcript_text, summary_style, output_language, api_key)

        if result:
            st.markdown("---")
            st.markdown("### 📋 Meeting Summary")

            # Overview
            st.markdown('<div class="summary-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">📝 Overview</div>', unsafe_allow_html=True)
            st.markdown(result.get("overview", "N/A"))
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-label">✅ Key Decisions</div>', unsafe_allow_html=True)
                for d in result.get("decisions", []):
                    st.markdown(f"• {d}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_b:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-label">🎯 Action Items</div>', unsafe_allow_html=True)
                for item in result.get("action_items", []):
                    owner = item.get("owner", "")
                    task = item.get("task", "")
                    badge = f'<span class="badge">{owner}</span> ' if owner else ""
                    st.markdown(f'<div class="action-item">{badge}{task}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Sentiment & Topics
            st.markdown("<br>", unsafe_allow_html=True)
            col_c, col_d = st.columns(2)

            with col_c:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-label">🌡️ Meeting Tone</div>', unsafe_allow_html=True)
                st.markdown(result.get("tone", "N/A"))
                st.markdown('</div>', unsafe_allow_html=True)

            with col_d:
                st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-label">🏷️ Topics Discussed</div>', unsafe_allow_html=True)
                topics = result.get("topics", [])
                st.markdown(", ".join([f"`{t}`" for t in topics]) if topics else "N/A")
                st.markdown('</div>', unsafe_allow_html=True)

            # Download
            st.markdown("<br>", unsafe_allow_html=True)
            export_text = f"""MEETING SUMMARY — MeetMind
{'='*50}
SOURCE: {input_source}

OVERVIEW:
{result.get('overview', '')}

KEY DECISIONS:
{chr(10).join(['• ' + d for d in result.get('decisions', [])])}

ACTION ITEMS:
{chr(10).join(['• [' + i.get('owner','?') + '] ' + i.get('task','') for i in result.get('action_items', [])])}

TOPICS: {', '.join(result.get('topics', []))}
TONE: {result.get('tone', '')}
"""
            st.download_button(
                "⬇️ Download Summary (.txt)",
                data=export_text,
                file_name="meeting_summary.txt",
                mime="text/plain"
            )

st.markdown('<div class="footer-note">Powered by Google Gemini · Built with Streamlit · MeetMind v1.0</div>', unsafe_allow_html=True)
