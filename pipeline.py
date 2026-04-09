"""
pipeline.py — Agent orchestration for Artisia AI.

Supports:
  - Claude Vision (real image analysis via base64)
  - Text-only mode
  - Mock mode (USE_MOCK=true, no API key needed)

Set USE_MOCK=true in your .env for instant demo mode.
"""

import os
import json
import re
from agents import (
    EXTRACTION_AGENT_PROMPT,
    TRANSLATION_AGENT_PROMPT,
    MARKET_AGENT_PROMPT,
    BRANDING_AGENT_PROMPT,
    VALIDATION_AGENT_PROMPT,
)

# ─── Config ──────────────────────────────────────────────────────────────────
USE_MOCK       = os.getenv("USE_MOCK", "false").lower() == "true"
LLM_PROVIDER   = os.getenv("LLM_PROVIDER", "anthropic")
MODEL_ANTHROPIC = "claude-sonnet-4-20250514"
MODEL_OPENAI    = "gpt-4o"


# ─── LLM Call (text-only) ────────────────────────────────────────────────────

def call_llm(prompt: str) -> dict:
    """Send a text prompt to the configured LLM, return parsed JSON dict."""
    try:
        raw = _raw_llm(prompt)
        raw = re.sub(r"```json\s*|\s*```", "", raw).strip()
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[Pipeline] JSON parse error: {e}\nRaw: {raw[:300]}")
        return {}
    except Exception as e:
        print(f"[Pipeline] LLM call error: {e}")
        return {}


def _raw_llm(prompt: str) -> str:
    if LLM_PROVIDER == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        msg = client.messages.create(
            model=MODEL_ANTHROPIC,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text

    elif LLM_PROVIDER == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=MODEL_OPENAI,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        return resp.choices[0].message.content

    raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")


# ─── Vision Call (image + text) ──────────────────────────────────────────────

def call_llm_vision(prompt: str, image_b64: str, media_type: str) -> dict:
    """
    Send a prompt + base64 image to Claude Vision or GPT-4o.
    Falls back to text-only if vision fails.
    """
    try:
        if LLM_PROVIDER == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            msg = client.messages.create(
                model=MODEL_ANTHROPIC,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}},
                        {"type": "text", "text": prompt}
                    ]
                }]
            )
            raw = msg.content[0].text

        elif LLM_PROVIDER == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            resp = client.chat.completions.create(
                model=MODEL_OPENAI,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_b64}"}},
                        {"type": "text", "text": prompt}
                    ]
                }],
                max_tokens=1024,
            )
            raw = resp.choices[0].message.content
        else:
            raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")

        raw = re.sub(r"```json\s*|\s*```", "", raw).strip()
        return json.loads(raw)

    except json.JSONDecodeError as e:
        print(f"[Vision] JSON parse error: {e}")
        return {}
    except Exception as e:
        print(f"[Vision] Vision call error: {e} — falling back to text-only")
        return call_llm(prompt)


# ─── Mock Outputs ─────────────────────────────────────────────────────────────

def _mock_extraction():
    return {
        "detected_product_type": "Premium Leather Wallet",
        "key_features": ["RFID blocking", "Minimalist design", "8 card slots", "Full-grain leather"],
        "materials_or_ingredients": ["Full-grain leather", "RFID-blocking lining"],
        "colors_or_variants": ["Brown", "Black", "Tan"],
        "dimensions_or_specs": "9cm x 11cm x 1.2cm",
        "detected_language": "en",
        "confidence_score": 0.95,
    }

def _mock_translation():
    return {
        "normalized_description": "A handcrafted full-grain leather wallet featuring RFID-blocking technology, minimalist design, and 8 card slots.",
        "was_translated": False,
        "original_language": "English",
        "translation_notes": "No translation needed.",
    }

def _mock_market():
    return {
        "suggested_price_range": {"low": 35, "mid": 65, "high": 120, "currency": "USD"},
        "recommended_price": 65,
        "price_rationale": "Mid-range pricing aligns with premium leather + RFID feature set.",
        "target_audience": "Urban professionals aged 25–45 who value minimalist style and security.",
        "competitor_landscape": "Competes with Bellroy, Fossil, and DTC leather brands.",
        "market_opportunity": "High",
        "top_selling_regions": ["United States", "United Kingdom", "Germany", "Australia", "Canada"],
        "market_trends": ["Growing demand for RFID protection", "Minimalist accessories trend", "Rise of DTC leather goods"],
    }

def _mock_branding():
    return {
        "product_title": "Artisan RFID-Blocking Full-Grain Leather Wallet",
        "short_description": "Handcrafted protection meets minimalist elegance — for the modern professional.",
        "full_description": (
            "Crafted from full-grain leather and built for the modern world, this wallet combines timeless artisanal quality "
            "with cutting-edge RFID-blocking technology. Eight thoughtfully designed card slots keep your essentials organized "
            "without the bulk.\n\n"
            "Whether you're navigating a boardroom or a busy city street, this wallet is a quiet statement of taste and security. "
            "The slim profile fits effortlessly in any pocket, while the durable leather develops a rich patina over time.\n\n"
            "Available in brown, black, and tan. Built to last. Designed to impress."
        ),
        "key_selling_points": [
            "RFID-blocking lining protects against digital theft",
            "Full-grain leather for premium durability",
            "8 card slots — organized, never bulky",
            "Slim profile fits any pocket",
            "Handcrafted with artisanal attention to detail",
        ],
        "brand_tone": "Premium Artisanal",
        "suggested_tags": ["leather wallet", "RFID wallet", "minimalist wallet", "mens wallet", "slim wallet", "full grain leather", "handmade wallet"],
        "call_to_action": "Shop Now — Free Shipping Over $50",
    }

def _mock_validation():
    return {
        "global_readiness_score": 88,
        "score_breakdown": {"data_completeness": 23, "market_potential": 22, "content_quality": 24, "global_reach": 19},
        "quality_flags": ["No product weight specified", "Missing care instructions"],
        "recommendations": [
            "Add product weight for shipping calculators",
            "Include leather care instructions",
            "Add lifestyle photography for higher conversion",
            "Include size comparison vs credit card",
        ],
        "enterprise_ready": True,
        "validation_summary": "Strong product data with compelling copy and clear market positioning. Minor logistics gaps.",
    }


# ─── Agent Functions ─────────────────────────────────────────────────────────

def run_extraction_agent(description: str, image_b64: str = None, image_media_type: str = None) -> dict:
    if USE_MOCK:
        return _mock_extraction()

    prompt = EXTRACTION_AGENT_PROMPT.format(
        description=description or "(No text description provided — analyze the image.)",
        image_context="Product image attached." if image_b64 else "No image provided."
    )

    if image_b64 and image_media_type:
        return call_llm_vision(prompt, image_b64, image_media_type)
    return call_llm(prompt)


def run_translation_agent(description: str, detected_language: str) -> dict:
    if USE_MOCK:
        return _mock_translation()
    prompt = TRANSLATION_AGENT_PROMPT.format(
        description=description,
        detected_language=detected_language
    )
    return call_llm(prompt)


def run_market_agent(product_type: str, key_features: list, normalized_description: str) -> dict:
    if USE_MOCK:
        return _mock_market()
    prompt = MARKET_AGENT_PROMPT.format(
        product_type=product_type,
        key_features=", ".join(key_features),
        normalized_description=normalized_description
    )
    return call_llm(prompt)


def run_branding_agent(product_type: str, key_features: list, target_audience: str,
                       normalized_description: str, market_opportunity: str) -> dict:
    if USE_MOCK:
        return _mock_branding()
    prompt = BRANDING_AGENT_PROMPT.format(
        product_type=product_type,
        key_features=", ".join(key_features),
        target_audience=target_audience,
        normalized_description=normalized_description,
        market_opportunity=market_opportunity
    )
    return call_llm(prompt)


def run_validation_agent(branding: dict, market: dict, extraction: dict, translation: dict) -> dict:
    if USE_MOCK:
        return _mock_validation()
    prompt = VALIDATION_AGENT_PROMPT.format(
        product_title=branding.get("product_title", ""),
        full_description=branding.get("full_description", ""),
        recommended_price=market.get("recommended_price", ""),
        market_opportunity=market.get("market_opportunity", ""),
        top_selling_regions=", ".join(market.get("top_selling_regions", [])),
        key_features=", ".join(extraction.get("key_features", [])),
        was_translated=translation.get("was_translated", False)
    )
    return call_llm(prompt)


# ─── Master Pipeline ──────────────────────────────────────────────────────────

def run_pipeline(description: str = "", image_b64: str = None, image_media_type: str = None,
                 image=None) -> dict:
    """
    Full 5-agent pipeline.

    Args:
        description:      Product text description.
        image_b64:        Base64-encoded image string (for Claude Vision).
        image_media_type: MIME type e.g. "image/jpeg".
        image:            Legacy param — ignored (kept for backward compatibility).

    Returns:
        Unified structured output dict.
    """

    # Agent 1 — Extraction (with optional Vision)
    extraction = run_extraction_agent(description, image_b64, image_media_type)

    # Agent 2 — Translation
    detected_lang = extraction.get("detected_language", "en")
    translation = run_translation_agent(description, detected_lang)

    # Agent 3 — Market Intelligence
    market = run_market_agent(
        product_type=extraction.get("detected_product_type", "Unknown Product"),
        key_features=extraction.get("key_features", []),
        normalized_description=translation.get("normalized_description", description)
    )

    # Agent 4 — Branding
    branding = run_branding_agent(
        product_type=extraction.get("detected_product_type", "Unknown Product"),
        key_features=extraction.get("key_features", []),
        target_audience=market.get("target_audience", "General consumers"),
        normalized_description=translation.get("normalized_description", description),
        market_opportunity=market.get("market_opportunity", "Medium")
    )

    # Agent 5 — Validation
    validation = run_validation_agent(branding, market, extraction, translation)

    # ── Final Assembly ──
    price = market.get("recommended_price", 0)
    currency = market.get("suggested_price_range", {}).get("currency", "USD")

    return {
        "product_title":          branding.get("product_title", "Unnamed Product"),
        "short_description":      branding.get("short_description", ""),
        "description":            branding.get("full_description", ""),
        "price_suggestion":       f"${price:,.2f} {currency}" if price else "—",
        "market_positioning": (
            f"{market.get('market_opportunity','—')} opportunity · "
            f"Target: {market.get('target_audience','—')} · "
            f"Top regions: {', '.join(market.get('top_selling_regions',[])[:3])}"
        ),
        "global_readiness_score": validation.get("global_readiness_score", 0),
        "agents": {
            "extraction":         extraction,
            "translation":        translation,
            "market_intelligence": market,
            "branding":           branding,
            "validation":         validation,
        }
    }
