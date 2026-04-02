import os
import datetime
from agents.brand_agent import brand_agent
from agents.market_agent import market_agent
from agents.listing_agent import listing_agent
from agents.translator_agent import translator_agent
from agents.scoring_agent import run_scoring_agent
from utils.memory import ProductMemory

def run_pipeline(input_data):
    # Initialize basic memory if input is a string
    if isinstance(input_data, str):
        memory = ProductMemory()
        memory.product = {"name": input_data}
        memory.artisan_profile = {"name": "Unknown Artisan", "region": "Unknown Region"}
        memory.story_input = {"start_year": "", "inspiration": "", "emotion": ""}
        memory.market_input = {"current_price": "", "customers": "", "sales_channels": ""}
    else:
        memory = input_data

    artisan_name = "Unknown"
    if hasattr(memory, "artisan_profile") and isinstance(memory.artisan_profile, dict):
        artisan_name = memory.artisan_profile.get("name", "Unknown")
    elif isinstance(memory, dict) and "artisan_profile" in memory:
        artisan_name = memory["artisan_profile"].get("name", "Unknown")

    # Log starting run
    with open("logs/runs.log", "a") as f:
        f.write(f"[{datetime.datetime.now()}] Starting pipeline for artisan {artisan_name}\n")

    # Step 1: Run Brand Agent
    brand_agent(memory)
    
    # Step 2: Run Market Agent
    market_agent(memory)
    
    # Step 3: Run Listing Agent
    listing_agent(memory)
    
    # Step 4: Run Translator Agent
    translator_agent(memory)
    
    # Step 5: Run Scoring Agent
    # scoring_agent returns memory
    memory = run_scoring_agent(memory)

    # Log completion
    with open("logs/runs.log", "a") as f:
        f.write(f"[{datetime.datetime.now()}] Completed pipeline for artisan {artisan_name}\n")

    # Determine how to extract fields safely depending on whether memory is a dict or an object
    score = memory.get("score") if isinstance(memory, dict) else memory.score
    final_listing = memory.get("listing") if isinstance(memory, dict) else memory.listing

    return {
        "memory": memory,
        "score": score,
        "final_listing": final_listing
    }

