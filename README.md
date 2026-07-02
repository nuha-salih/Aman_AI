<div align="center">

# 🛡️ Aman AI
### AI-Powered Real-Time Deepfake & Financial Scam Detection Platform

**Proactive fraud detection system for financial institutions using real-time AI analysis.**
Protecting individuals and empowering banks against voice fraud, phishing, and social engineering — in Arabic, in real time.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4o%20%7C%20Whisper-412991)](https://openai.com/)
[![AraBERT](https://img.shields.io/badge/NLP-AraBERT-2E7D32)](https://github.com/aub-mind/arabert)
[![License](https://img.shields.io/badge/License-MIT-yellow)](#-license)

</div>

---

## 📌 The Problem

Financial scam calls, SMS phishing, and AI-generated deepfake voice fraud are rising sharply across Saudi Arabia and the wider Gulf region — yet almost no Arabic-language tools exist to detect them in real time, in dialect, at the point of contact.

**Aman AI** ("أمان" — Arabic for *safety*) closes that gap.

## 💡 The Solution

Aman AI is a **dual-sided AI platform**:

| | |
|---|---|
| 🧍 **B2C — Consumer Protection** | Real-time analysis of calls, SMS, links, and screenshots to flag scams and deepfake voices before damage is done |
| 🏦 **B2B — Enterprise Security** | Anonymized scam patterns power a **Scam Simulation System** that banks use to train employees and customers against real, localized fraud tactics |

Both sides feed the same **Encrypted Data Feedback Loop** — the more the system is used, the smarter it gets, without ever exposing raw user data externally.

---

## ✨ Key Features

### ✅ Implemented
- **Unified analysis** — multi-modal support for SMS, URLs, and plain text scam detection
- **Image/screenshot analysis** — extract and analyze text from suspicious screenshots
- **Audio transcription** — convert voice notes/calls to text via Speech-to-Text
- **AI-driven scoring** — every input returns a Risk Score, Confidence Score, Scam Classification, key Indicators, and a Summary
- **Persistent logging** — every analysis is stored and retrievable for audit and future model training

### 🚧 In Progress
- **Custom fraud detection model** trained on scam messages, phishing URLs, and voice samples
- **Decision Engine** — fuses AI analysis, the custom model, historical data, and bank identity verification into one unified verdict
- **Continuous learning loop** — stored logs feed periodic model retraining

### 🔮 Roadmap
- **Real-time call analysis** — live in-call risk alerts via a floating bubble + notification bar, triggered the moment a call comes in
- **Voice biometrics engine** — tone, stress, and emotion analysis to flag distress or coercion
- **Deepfake voice detection** — identify AI-synthesized or cloned voices
- **Bank Identity Verification** — a digital fingerprint per bank (official numbers, message style, terminology) to catch impersonation
- **Security Awareness Dashboard** — lets bank IT/security teams launch phishing simulations and measure staff/customer awareness

---

## 🏗️ System Architecture

When audio is submitted, the pipeline splits into parallel tracks to maximize both accuracy and privacy:

```
                              ┌──> [Local]  Deepfake Detection Model ─────> voice authenticity check
                              │
[ Encrypted Audio Input ] ────┼──> [Local]  Acoustic Feature Extraction ──> tone, tremor, stress analysis
                              │     (Librosa)
                              │
                              └──> [Cloud]  OpenAI Whisper ────────────────> speech-to-text transcription
                                                                                       │
                                                                                       ▼
                                                                            [ OpenAI GPT-4o ]
                                                                                       │
                                                                                       ▼
                                                                          contextual scam/deception analysis
```

**Privacy-by-design:** biometric and voice-tone data are processed **entirely locally** and never leave the server. Only the abstracted text transcript is sent externally for contextual analysis — fully aligned with Saudi NCA / NDMO data protection principles.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python) |
| Speech-to-Text | OpenAI Whisper |
| Contextual/Scam Analysis | OpenAI GPT-4o |
| Arabic NLP Classification | AraBERT (`aubmindlab/bert-base-arabertv2`) |
| Acoustic Feature Extraction | Librosa |
| Database | SQLite |
| Config & Secrets | python-dotenv |

---

## 📂 Project Structure

```
Aman_AI_Model/
├── datasets/
│   ├── arabic_calls/     # Arabic scam/legitimate call corpus (text + audio)
│   ├── scam_calls/       # English scam/non-scam reference data
│   └── saudi_custom/     # Team-collected Saudi-dialect samples
├── notebooks/            # Model training & experimentation notebooks
├── models/               # Trained model artifacts
├── outputs/               # Evaluation results, logs, exports
└── main.py                # FastAPI application entry point
```

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone <repo-url>
cd Aman_AI_Model

# 2. Install dependencies
pip install fastapi uvicorn openai python-dotenv pandas scikit-learn librosa joblib

# 3. Add your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# 4. Run the API
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `/docs`.

### Example — Analyze a message

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"type": "sms", "content": "حسابك البنكي معلق، اضغط الرابط فوراً"}'
```

**Response:**
```json
{
  "risk_score": 92,
  "confidence_score": 0.87,
  "scam_detected": true,
  "indicators": ["urgency", "suspicious_link", "bank_impersonation"],
  "summary": "Message displays strong social engineering markers typical of bank impersonation fraud."
}
```

---

## 📊 Data & Model Attribution

Aman AI's Arabic NLP layer builds on top of published academic research rather than reinventing scam-detection modeling from scratch, allowing our team to focus engineering effort on the platform, real-time pipeline, and enterprise features that make Aman AI unique.

- **Dataset:** [Arabic Scam and Legitimate Call Conversation Dataset (ASLC-448)](https://data.mendeley.com/datasets/p384bgyzz3) — 448 annotated multi-dialect Arabic call conversations (Tawfik, 2026)
- **Base model approach:** AraBERT fine-tuning methodology (`aubmindlab/bert-base-arabertv2`), retrained on our combined dataset (ASLC-448 + team-collected Saudi-dialect samples)

> If you use this dataset, please cite: Tawfik, Mohammed (2026), *"Arabic Scam and Legitimate Call Conversation Dataset (ASLC-448)"*, Mendeley Data, V2, doi: 10.17632/p384bgyzz3.2

All platform architecture, API design, the multi-modal pipeline, Decision Engine, Bank Identity Verification, and the Security Awareness Dashboard are original work by the Aman AI team.

---

## 🔒 Security & Privacy

- End-to-end encryption of stored audio and analysis data
- Anonymization before any long-term storage
- Minimal data sharing — only abstracted text (never raw voice biometrics) leaves the local environment
- **Enterprise option:** full on-premise deployment, where all data stays within the bank's own servers

---

## 💼 Business Model

Aman AI is offered as an **API-first product** that banks integrate directly into their existing apps — no separate app download or extra login required for end users.

- **Annual subscription licensing** per institution
- Optional **fully private deployment** inside the bank's own infrastructure for maximum data sovereignty
- Add-on: **Security Awareness module** for IT/cybersecurity departments to run phishing/vishing simulations and track staff readiness over time

---

## 👥 Team

- **نهى صلاح محمد احمد ,اعدل بقيه اسماء الفريق والادوار** — Lead Developer & Architect
- **[اسم عضو الفريق]** — [تخصصها/دورها]

## 📄 License

Distributed under the MIT License.

---

<div align="center">

### Built for Amd Hackathon (هكثون أمد) — Fintech Track

*Aman AI — because trust shouldn't be guesswork.*

</div>
