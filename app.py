import streamlit as st
import json
import os
from utils.memory import ProductMemory
from utils.interview import INTERVIEW_QUESTIONS
from agents.pipeline import run_pipeline

# Page Config
st.set_page_config(page_title="ARTISIA Listing Generator", layout="wide")

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2c3e50;
    }
    .agent-header {
        color: #3498db;
        border-bottom: 2px solid #3498db;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 ARTISIA Listing Generator")
st.markdown("Transforming artisan stories into global marketplace success.")

if 'memory' not in st.session_state:
    st.session_state.memory = ProductMemory()

# Sidebar for memory view
with st.sidebar:
    st.header("Memory Status")
    if st.button("Reset Session"):
        st.session_state.memory = ProductMemory()
        st.rerun()
    st.json(st.session_state.memory.model_dump())

# Main Interview UI
col1, col2 = st.columns(2)

with col1:
    st.header("Section 1: Artisan Profile")
    for q in INTERVIEW_QUESTIONS["artisan_profile"]:
        val = st.text_input(q["label"], key=f"q_{q['id']}")
        st.session_state.memory.artisan_profile[q["id"]] = val

    st.header("Section 2: Product Information")
    for q in INTERVIEW_QUESTIONS["product"]:
        val = st.text_input(q["label"], key=f"q_{q['id']}")
        st.session_state.memory.product[q["id"]] = val

with col2:
    st.header("Section 3: Story Questions")
    for q in INTERVIEW_QUESTIONS["story_input"]:
        val = st.text_area(q["label"], key=f"q_{q['id']}")
        st.session_state.memory.story_input[q["id"]] = val

    st.header("Section 4: Market Questions")
    for q in INTERVIEW_QUESTIONS["market_input"]:
        val = st.text_input(q["label"], key=f"q_{q['id']}")
        st.session_state.memory.market_input[q["id"]] = val

if st.button("🚀 Generate Listing"):
    with st.spinner("Pipeline running... This may take a moment."):
        result = run_pipeline(st.session_state.memory)
        st.session_state.memory = result["memory"]
        
        # Save output
        timestamp = os.popen('date /t').read().strip().replace('/', '-')
        filename = f"data/outputs/listing_{st.session_state.memory.artisan_profile.get('name', 'unknown')}.json"
        with open(filename, "w") as f:
            json.dump(memory.model_dump(), f, indent=4)
        
    st.success("Listing generated successfully!")

# Results Display
if st.session_state.memory.listing:
    st.divider()
    st.header("Final Output")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Story", "Price Recommendation", "Marketplace Listing", "Translations", "Readiness Score"])
    
    with tab1:
        st.subheader("Brand Narrative")
        story = st.session_state.memory.story
        st.write(f"**Origin Story:** {story.get('origin_story')}")
        st.write(f"**Brand Identity:** {story.get('brand_identity')}")
        st.write(f"**Tone:** {story.get('tone')}")
        st.write(f"**Cultural Elements:** {', '.join(story.get('cultural_elements', []))}")
        
    with tab2:
        st.subheader("Pricing Strategy")
        market = st.session_state.memory.market
        st.metric("Recommended Price Range", market.get("pricing_range"))
        st.write(f"**Target Customers:** {market.get('target_customers')}")
        st.write(f"**Target Markets:** {', '.join(market.get('target_markets', []))}")
        
    with tab3:
        listing = st.session_state.memory.listing
        st.subheader(listing.get("title"))
        st.write(listing.get("description"))
        st.markdown("### Key Features")
        for bp in listing.get("bullet_points", []):
            st.write(f"- {bp}")
        st.markdown(f"**Category:** {listing.get('category')}")
        st.markdown(f"**Tags:** {', '.join(listing.get('tags', []))}")
        
    with tab4:
        trans = st.session_state.memory.translation
        st.subheader("French Listing")
        st.write(f"**Titre:** {trans.get('title_fr')}")
        st.write(f"**Description:** {trans.get('description_fr')}")
        
    with tab5:
        score = st.session_state.memory.score
        st.metric("Global Readiness Score", f"{score.get('global_readiness', 0)}/100")
        st.info(f"**Strongest Factor:** {score.get('strongest_factor')}")
        st.warning(f"**Weakest Factor:** {score.get('weakest_factor')}")
        st.markdown("### Recommendations")
        for rec in score.get("recommendations", []):
            st.write(f"- {rec}")
