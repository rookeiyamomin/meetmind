<div align="center">

# 🎙️ MeetMind
### AI-Powered Meeting Summarizer
###### Built by Rookeiya with ❤️

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com)
[![CI](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/meetmind/ci.yml?style=flat-square&label=CI)](https://github.com/YOUR_USERNAME/meetmind/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Drop your meeting transcript or audio. Get instant summaries, decisions, and action items.**

[Features](#-features) · [Demo](#-demo) · [Architecture](#-architecture) · [Setup](#-setup) · [Deploy](#-deploy)

</div>

---

## ✨ Features

- **Multi-format input** — Upload `.txt`, `.pdf`, `.docx` transcripts, audio files (`.mp3`, `.wav`, `.m4a`), or paste raw text
- **Native audio transcription** — Powered by Gemini's Files API; no Whisper needed
- **Smart summarization** — Three styles: Concise bullets, Detailed paragraphs, or Executive Brief
- **Decision extraction** — Automatically identifies key decisions made in the meeting
- **Action items with owners** — Extracts tasks and attributes them to specific people
- **Meeting tone analysis** — Detects whether the meeting was productive, tense, collaborative, etc.
- **Multilingual output** — English, Hindi, or Hinglish responses
- **Export** — Download the full summary as a `.txt` file

---

##  Demo

<img width="681" height="554" alt="image" src="https://github.com/user-attachments/assets/252079be-30a9-4d43-962d-b582d445e5f6" />

<img width="721" height="574" alt="image" src="https://github.com/user-attachments/assets/afeabfa0-fc66-4c77-a419-7f76d3b0ec2e" />


**Sample input (paste in the app):**
```
Rukayya: Good morning everyone. Let's start with the Q3 review.
Umar: Revenue is up 12% from last quarter. We hit $2.4M.
Sadiya: Great. We've decided to increase the marketing budget by 20%.
Hamza: I'll handle the new campaign rollout by end of month.
Umar: I'll send the financial report to stakeholders by Friday.
Sadiya: Perfect. Let's schedule a follow-up next Tuesday.
```

**Sample output:**
```
Overview:   Q3 revenue review — strong growth; budget and comms decisions made.
Decisions:  Marketing budget increased by 20%
Actions:    [Hamza] New campaign rollout — end of month
               [Umar] Financial report to stakeholders — Friday
Tone:       Productive and collaborative
Topics:     Q3 Review, Revenue, Marketing, Follow-up
```

---

##  Architecture

<img width="892" height="682" alt="architecture" src="https://github.com/user-attachments/assets/cf277c7c-5b88-42bb-8cfc-7fb3255aa7ae" />

## ️ FlowChart
<img width="1472" height="1784" alt="flowchart" src="https://github.com/user-attachments/assets/b724a82f-ba11-40d1-b309-d32ccfbf068c" />

##  Project Structure

```
meetmind/
├── app/
│   ├── main.py          # Streamlit UI & layout
│   ├── summarizer.py    # Gemini API · prompt builder · JSON parser
│   ├── transcriber.py   # Audio → transcript via Gemini Files API
│   └── file_parser.py   # PDF / DOCX / TXT text extraction
├── tests/
│   └── test_app.py      # Unit tests (pytest)
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI pipeline
├── .env                 # API key (never commit!)
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  Setup

### Prerequisites
- Python 3.11+, PyCharm (or any IDE)
- Google account with Gemini API access

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/meetmind.git
cd meetmind
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add your Gemini API key
Get your key from  https://aistudio.google.com/app/apikey

Open `.env` and add:
```
GEMINI_API_KEY=AIza...your_key
```

### Step 5 — Run
```bash
python -m streamlit run app/main.py
```

Open **http://localhost:8501** 

---

##  Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 🚀 Deploy to Streamlit Cloud (Free)

1. Push to GitHub (`.env` is gitignored — safe!)
2. Go to https://share.streamlit.io → connect your repo
3. Entry point: `app/main.py`
4. **Settings → Secrets** → add `GEMINI_API_KEY = "your_key"`
5. Deploy 

---

##  Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini 2.5 Flash |
| UI | Streamlit |
| PDF parsing | PyMuPDF (fitz) |
| DOCX parsing | python-docx |
| Audio transcription | Gemini Files API |
| CI/CD | GitHub Actions |
| Language | Python 3.11+ |

---

##  Roadmap

- [ ] Meeting history saved to SQLite
- [ ] Speaker diarization
- [ ] Google Calendar integration
- [ ] Slack / email export
- [ ] Auto-detect transcript language

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">Built using <strong>Google Gemini</strong> + <strong>Streamlit</strong></div>
