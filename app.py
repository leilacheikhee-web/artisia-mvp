import streamlit as st
import json
import os
import csv
import io
import base64
from datetime import datetime
from PIL import Image
from pipeline import run_pipeline
from utils import format_readiness_score, format_json_output

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Artisia AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --ink: #0A0A0F;
    --cream: #F5F2EB;
    --gold: #C9A84C;
    --gold-light: #E8D5A3;
    --muted: #6B6B7A;
    --card-bg: #FFFFFF;
    --border: #E2DDD6;
    --green: #3A7A34;
    --green-bg: #F0F7EF;
    --red: #9B2B2B;
    --red-bg: #FDF0F0;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: var(--cream); color: var(--ink); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

.hero-badge { display:inline-block; background:var(--ink); color:var(--gold); font-family:'Syne',sans-serif; font-size:0.65rem; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; padding:6px 14px; border-radius:2px; margin-bottom:1.2rem; }
.hero-title { font-family:'Syne',sans-serif; font-size:3rem; font-weight:800; line-height:1.05; letter-spacing:-0.03em; color:var(--ink); margin:0 0 0.6rem; }
.hero-title span { color:var(--gold); }
.hero-sub { font-size:1rem; font-weight:300; color:var(--muted); max-width:560px; line-height:1.65; }
.divider { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }
.input-label { font-family:'Syne',sans-serif; font-size:0.68rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:var(--muted); margin-bottom:0.4rem; }

.output-card { background:var(--card-bg); border:1px solid var(--border); border-radius:8px; padding:1.3rem 1.5rem; margin-bottom:0.9rem; }
.output-card-label { font-family:'Syne',sans-serif; font-size:0.62rem; font-weight:700; letter-spacing:0.16em; text-transform:uppercase; color:var(--gold); margin-bottom:0.4rem; }
.output-card-value { font-size:0.95rem; color:var(--ink); line-height:1.6; }
.output-title-value { font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:var(--ink); }

.score-number { font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:800; color:var(--gold); line-height:1; }
.score-label { font-size:0.82rem; color:var(--muted); font-weight:300; line-height:1.5; }
.score-bar-track { background:var(--border); border-radius:99px; height:6px; width:100%; margin-top:0.5rem; }
.score-bar-fill { height:6px; border-radius:99px; background:linear-gradient(90deg,var(--gold),#F0C96A); }

.pipeline-strip { display:flex; gap:0.4rem; align-items:center; margin:1rem 0; flex-wrap:wrap; }
.pipeline-step { background:var(--ink); color:var(--cream); font-family:'Syne',sans-serif; font-size:0.6rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; padding:4px 11px; border-radius:2px; }
.pipeline-arrow { color:var(--gold); font-size:0.75rem; }

.stButton > button { background:var(--ink) !important; color:var(--gold) !important; border:none !important; font-family:'Syne',sans-serif !important; font-size:0.75rem !important; font-weight:700 !important; letter-spacing:0.12em !important; text-transform:uppercase !important; padding:0.7rem 2rem !important; border-radius:3px !important; width:100% !important; transition:opacity 0.2s !important; }
.stButton > button:hover { opacity:0.82 !important; }

.history-card { background:white; border:1px solid var(--border); border-radius:6px; padding:0.85rem 1rem; margin-bottom:0.6rem; }
.history-title { font-family:'Syne',sans-serif; font-size:0.82rem; font-weight:700; color:var(--ink); }
.history-meta { font-size:0.72rem; color:var(--muted); margin-top:2px; }

.flag-chip { display:inline-block; background:var(--red-bg); color:var(--red); font-size:0.72rem; border-radius:3px; padding:3px 8px; margin:2px; }
.rec-chip { display:inline-block; background:var(--green-bg); color:var(--green); font-size:0.72rem; border-radius:3px; padding:3px 8px; margin:2px; }
.voice-note { background:#FFFBF0; border:1px solid var(--gold-light); border-radius:6px; padding:0.7rem 1rem; font-size:0.82rem; color:var(--muted); margin-top:0.5rem; }
.enterprise-badge { display:inline-block; background:var(--green-bg); color:var(--green); font-family:'Syne',sans-serif; font-size:0.62rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:4px 10px; border-radius:2px; }
.not-ready-badge { display:inline-block; background:var(--red-bg); color:var(--red); font-family:'Syne',sans-serif; font-size:0.62rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:4px 10px; border-radius:2px; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "voice_transcript" not in st.session_state:
    st.session_state.voice_transcript = ""

# ─── Export Helpers ───────────────────────────────────────────────────────────
def export_csv(result: dict) -> str:
    market = result.get("agents", {}).get("market_intelligence", {})
    branding = result.get("agents", {}).get("branding", {})
    validation = result.get("agents", {}).get("validation", {})
    extraction = result.get("agents", {}).get("extraction", {})
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["Field", "Value"])
    rows = [
        ("Product Title", result.get("product_title", "")),
        ("Short Description", result.get("short_description", "")),
        ("Full Description", result.get("description", "")),
        ("Suggested Price", result.get("price_suggestion", "")),
        ("Global Readiness Score", result.get("global_readiness_score", "")),
        ("Enterprise Ready", validation.get("enterprise_ready", "")),
        ("Market Opportunity", market.get("market_opportunity", "")),
        ("Target Audience", market.get("target_audience", "")),
        ("Top Regions", ", ".join(market.get("top_selling_regions", []))),
        ("Key Features", ", ".join(extraction.get("key_features", []))),
        ("SEO Tags", ", ".join(branding.get("suggested_tags", []))),
        ("Brand Tone", branding.get("brand_tone", "")),
        ("CTA", branding.get("call_to_action", "")),
        ("Quality Flags", "; ".join(validation.get("quality_flags", []))),
        ("Recommendations", "; ".join(validation.get("recommendations", []))),
    ]
    for row in rows:
        w.writerow(row)
    return output.getvalue()


def export_pdf(result: dict):
    try:
        from fpdf import FPDF
        market = result.get("agents", {}).get("market_intelligence", {})
        branding = result.get("agents", {}).get("branding", {})
        validation = result.get("agents", {}).get("validation", {})
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(18, 18, 18)
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(10, 10, 15)
        pdf.cell(0, 12, "ARTISIA AI", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(107, 107, 122)
        pdf.cell(0, 6, "Autonomous Product Intelligence Report", ln=True)
        pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.ln(4)
        pdf.set_draw_color(201, 168, 76)
        pdf.set_line_width(0.6)
        pdf.line(18, pdf.get_y(), 192, pdf.get_y())
        pdf.ln(6)

        def section(title, content):
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 5, title.upper(), ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(10, 10, 15)
            safe = content.encode("latin-1", errors="replace").decode("latin-1")
            pdf.multi_cell(0, 5.5, safe)
            pdf.ln(3)

        section("Product Title", result.get("product_title", "—"))
        section("Short Description", result.get("short_description", "—"))
        section("Full Description", result.get("description", "—"))
        section("Suggested Price", result.get("price_suggestion", "—"))
        section("Market Positioning", result.get("market_positioning", "—"))
        section("Global Readiness Score", f"{result.get('global_readiness_score',0)}/100 — {format_readiness_score(result.get('global_readiness_score',0))}")
        section("Key Selling Points", "\n".join([f"• {p}" for p in branding.get("key_selling_points", [])]))
        section("SEO Tags", ", ".join(branding.get("suggested_tags", [])))
        section("Quality Flags", "\n".join([f"! {f}" for f in validation.get("quality_flags", [])]) or "None")
        section("Recommendations", "\n".join([f"• {r}" for r in validation.get("recommendations", [])]))
        return bytes(pdf.output())
    except ImportError:
        return None


def transcribe_audio(audio_file) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        audio_file.seek(0)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", audio_file, "audio/wav"),
        )
        return transcript.text
    except Exception as e:
        st.warning(f"Voice transcription unavailable: {e}")
        return ""


# ─── Sidebar: Session History ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ Session History")
    if not st.session_state.history:
        st.markdown('<div style="font-size:0.82rem;color:#6B6B7A;">No runs yet.</div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            idx = len(st.session_state.history) - 1 - i
            score = item["result"].get("global_readiness_score", 0)
            title = item["result"].get("product_title", "Unnamed")
            ts = item["timestamp"]
            st.markdown(f"""
            <div class="history-card">
              <div class="history-title">{title[:38]}{"…" if len(title)>38 else ""}</div>
              <div class="history-meta">Score {score}/100 · {ts}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Load →", key=f"load_{idx}"):
                st.session_state.current_result = item["result"]
                st.rerun()
    if st.session_state.history:
        st.divider()
        if st.button("🗑 Clear History"):
            st.session_state.history = []
            st.session_state.current_result = None
            st.rerun()

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-badge">✦ Multi-Agent AI System</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Artisia <span>AI</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Transform raw product inputs into structured, enterprise-ready intelligence — powered by a five-agent autonomous pipeline.</p>', unsafe_allow_html=True)
st.markdown("""
<div class="pipeline-strip">
  <span class="pipeline-step">① Extraction</span><span class="pipeline-arrow">→</span>
  <span class="pipeline-step">② Translation</span><span class="pipeline-arrow">→</span>
  <span class="pipeline-step">③ Market Intel</span><span class="pipeline-arrow">→</span>
  <span class="pipeline-step">④ Branding</span><span class="pipeline-arrow">→</span>
  <span class="pipeline-step">⑤ Validation</span>
</div>
<hr class="divider"/>
""", unsafe_allow_html=True)

# ─── Layout ───────────────────────────────────────────────────────────────────
col_input, col_gap, col_output = st.columns([1, 0.06, 1.6])

with col_input:
    # Image Upload
    st.markdown('<div class="input-label">Product Image</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload product image", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True)

    # Voice Input
    st.markdown('<div class="input-label" style="margin-top:1.1rem;">Voice Input <span style="color:#C9A84C;font-size:0.6rem;margin-left:4px;">BETA</span></div>', unsafe_allow_html=True)
    audio_file = st.audio_input("Record product description", label_visibility="collapsed")
    if audio_file:
        with st.spinner("Transcribing…"):
            t = transcribe_audio(audio_file)
            if t:
                st.session_state.voice_transcript = t
        if st.session_state.voice_transcript:
            st.markdown(f'<div class="voice-note">🎙 <em>"{st.session_state.voice_transcript[:110]}{"…" if len(st.session_state.voice_transcript)>110 else ""}"</em></div>', unsafe_allow_html=True)

    # Text Description
    st.markdown('<div class="input-label" style="margin-top:1.1rem;">Product Description</div>', unsafe_allow_html=True)
    description = st.text_area(
        "Describe your product",
        value=st.session_state.voice_transcript,
        placeholder="e.g. Handmade leather wallet, RFID blocking, brown, 8 card slots…",
        height=120,
        label_visibility="collapsed"
    )

    st.markdown("<br/>", unsafe_allow_html=True)
    run_btn = st.button("✦ Generate Product Intelligence")

# ─── Pipeline Trigger ─────────────────────────────────────────────────────────
with col_output:
    if run_btn:
        if not description.strip() and uploaded_file is None:
            st.warning("Please provide a description or image.")
        else:
            with st.spinner(""):
                progress = st.empty()
                agents_list = ["Extraction","Translation","Market Intelligence","Branding","Validation"]
                import time
                for i in range(len(agents_list) + 1):
                    pills = "".join([
                        f'<span style="display:inline-block;background:{"#3A7A34" if j<i else "#0A0A0F"};color:white;'
                        f'font-family:Syne,sans-serif;font-size:0.6rem;font-weight:700;letter-spacing:0.08em;'
                        f'text-transform:uppercase;padding:4px 10px;border-radius:2px;margin:2px;">'
                        f'{"✓" if j<i else "◌"} {a}</span>'
                        for j, a in enumerate(agents_list)
                    ])
                    progress.markdown(pills, unsafe_allow_html=True)
                    time.sleep(0.35)
                progress.empty()

                # Encode image for Claude Vision
                image_b64, image_media_type = None, None
                if uploaded_file:
                    uploaded_file.seek(0)
                    image_b64 = base64.b64encode(uploaded_file.read()).decode("utf-8")
                    ext = uploaded_file.name.split(".")[-1].lower()
                    image_media_type = {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png","webp":"image/webp"}.get(ext,"image/jpeg")

                result = run_pipeline(image_b64=image_b64, image_media_type=image_media_type, description=description)

            st.session_state.history.append({"timestamp": datetime.now().strftime("%H:%M:%S"), "result": result})
            st.session_state.current_result = result
            st.rerun()

    # ─── Results Display ──────────────────────────────────────────────────────
    result = st.session_state.current_result
    if result:
        validation = result.get("agents", {}).get("validation", {})
        branding   = result.get("agents", {}).get("branding", {})
        market     = result.get("agents", {}).get("market_intelligence", {})

        st.markdown(f"""
        <div class="output-card">
          <div class="output-card-label">Product Title</div>
          <div class="output-title-value">{result.get("product_title","—")}</div>
          <div style="margin-top:5px;font-size:0.85rem;color:#6B6B7A;font-style:italic;">{result.get("short_description","")}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="output-card">
          <div class="output-card-label">Product Description</div>
          <div class="output-card-value">{result.get("description","—").replace(chr(10),"<br/>")}</div>
        </div>""", unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            pr = market.get("suggested_price_range", {})
            st.markdown(f"""
            <div class="output-card">
              <div class="output-card-label">Suggested Price</div>
              <div class="output-title-value">{result.get("price_suggestion","—")}</div>
              <div style="font-size:0.78rem;color:#6B6B7A;margin-top:4px;">Range ${pr.get("low","—")} – ${pr.get("high","—")}</div>
            </div>""", unsafe_allow_html=True)
        with cb:
            score_pct = int(result.get("global_readiness_score", 0))
            ent = validation.get("enterprise_ready", False)
            badge = '<span class="enterprise-badge">✓ Enterprise Ready</span>' if ent else '<span class="not-ready-badge">Not Enterprise Ready</span>'
            st.markdown(f"""
            <div class="output-card">
              <div class="output-card-label">Global Readiness Score</div>
              <div style="display:flex;align-items:center;gap:1rem;">
                <div class="score-number">{score_pct}</div>
                <div class="score-label">/100<br/>{badge}</div>
              </div>
              <div class="score-bar-track"><div class="score-bar-fill" style="width:{score_pct}%"></div></div>
              <div style="font-size:0.75rem;color:#6B6B7A;margin-top:6px;">{format_readiness_score(score_pct)}</div>
            </div>""", unsafe_allow_html=True)

        regions = ", ".join(market.get("top_selling_regions", [])[:4])
        trends = " · ".join(market.get("market_trends", [])[:2])
        st.markdown(f"""
        <div class="output-card">
          <div class="output-card-label">Market Positioning</div>
          <div class="output-card-value">{result.get("market_positioning","—")}</div>
          <div style="font-size:0.78rem;color:#6B6B7A;margin-top:6px;">📍 {regions}</div>
          <div style="font-size:0.78rem;color:#6B6B7A;margin-top:2px;">📈 {trends}</div>
        </div>""", unsafe_allow_html=True)

        ksp = branding.get("key_selling_points", [])
        if ksp:
            bullets = "".join([f'<div style="font-size:0.88rem;padding:3px 0;">• {p}</div>' for p in ksp])
            st.markdown(f'<div class="output-card"><div class="output-card-label">Key Selling Points</div>{bullets}</div>', unsafe_allow_html=True)

        tags = branding.get("suggested_tags", [])
        if tags:
            tag_html = "".join([f'<span style="display:inline-block;background:#F5F2EB;border:1px solid #E2DDD6;border-radius:3px;padding:3px 9px;font-size:0.75rem;margin:2px;">{t}</span>' for t in tags])
            st.markdown(f'<div class="output-card"><div class="output-card-label">SEO Tags</div><div style="margin-top:4px;">{tag_html}</div></div>', unsafe_allow_html=True)

        flags = validation.get("quality_flags", [])
        recs  = validation.get("recommendations", [])
        if flags or recs:
            fh = "".join([f'<span class="flag-chip">⚠ {f}</span>' for f in flags])
            rh = "".join([f'<span class="rec-chip">✓ {r}</span>' for r in recs])
            st.markdown(f"""
            <div class="output-card">
              <div class="output-card-label">Validation Report</div>
              <div style="margin-bottom:6px;">{fh}</div>
              <div>{rh}</div>
              <div style="font-size:0.78rem;color:#6B6B7A;margin-top:8px;font-style:italic;">{validation.get("validation_summary","")}</div>
            </div>""", unsafe_allow_html=True)

        # ── Exports ──────────────────────────────────────────────────────────
        st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
        st.markdown('<div class="input-label">Export Results</div>', unsafe_allow_html=True)
        e1, e2, e3 = st.columns(3)
        safe_name = result.get("product_title","product")[:30].replace(" ","_")

        with e1:
            st.download_button("⬡ JSON", data=format_json_output(result),
                               file_name=f"artisia_{safe_name}.json", mime="application/json")
        with e2:
            st.download_button("⬡ CSV", data=export_csv(result),
                               file_name=f"artisia_{safe_name}.csv", mime="text/csv")
        with e3:
            pdf = export_pdf(result)
            if pdf:
                st.download_button("⬡ PDF", data=pdf,
                                   file_name=f"artisia_{safe_name}.pdf", mime="application/pdf")
            else:
                st.caption("PDF: pip install fpdf2")

        with st.expander("⬡ Full Structured JSON"):
            st.code(format_json_output(result), language="json")

    else:
        st.markdown("""
        <div style="border:1.5px dashed #D6D0C8;border-radius:10px;padding:3rem 2rem;text-align:center;background:white;margin-top:0.5rem;">
            <div style="font-size:2rem;margin-bottom:0.8rem;">✦</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;color:#0A0A0F;margin-bottom:0.4rem;">Intelligence Output</div>
            <div style="font-size:0.88rem;color:#6B6B7A;font-weight:300;line-height:1.6;">
                Upload a product image or record your voice,<br/>then click <strong>Generate Product Intelligence</strong>.
            </div>
        </div>""", unsafe_allow_html=True)
