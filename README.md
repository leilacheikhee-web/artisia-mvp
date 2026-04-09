# ✦ Artisia AI — Autonomous Product Onboarding System

> Transform raw product inputs into structured, enterprise-ready intelligence — powered by a five-agent autonomous pipeline.

---

## 🏗 Architecture

```
Input (Image + Text)
        │
        ▼
┌─────────────────┐
│ Extraction Agent│  → Detects product type, features, language
└────────┬────────┘
         ▼
┌─────────────────┐
│Translation Agent│  → Normalizes all content to English
└────────┬────────┘
         ▼
┌─────────────────┐
│  Market Agent   │  → Pricing, audience, opportunity, regions
└────────┬────────┘
         ▼
┌─────────────────┐
│ Branding Agent  │  → Title, description, tags, CTA
└────────┬────────┘
         ▼
┌─────────────────┐
│Validation Agent │  → Global Readiness Score + QA flags
└────────┬────────┘
         ▼
   Structured JSON
```

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI — input, display, pipeline trigger |
| `agents.py` | Prompt templates for all 5 agents |
| `pipeline.py` | Agent functions + `run_pipeline()` orchestrator |
| `utils.py` | Output formatting helpers |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |

---

## 🚀 Quick Start

### 1. Clone & navigate
```bash
git clone <your-repo>
cd artisia-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and add your API key
```

### 5. Run in demo mode (no API key needed)
```bash
USE_MOCK=true streamlit run app.py
```

### 6. Run with real AI
```bash
streamlit run app.py
```

---

## ⚙️ Configuration

| Variable | Values | Description |
|----------|--------|-------------|
| `USE_MOCK` | `true` / `false` | Use mock data (no API calls) |
| `LLM_PROVIDER` | `anthropic` / `openai` | Which LLM to use |
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Your Anthropic key |
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI key |

---

## 🏆 Hackathon Notes

- All 5 agents produce **consistent JSON** — easy to chain or extend
- `USE_MOCK=true` enables full demo without API costs
- UI is production-grade but built fast with Streamlit
- Add voice input next: use `openai.audio.transcriptions` to feed `description`
