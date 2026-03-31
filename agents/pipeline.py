import os
import datetime
from agents.brand_agent import run_brand_agent
from agents.market_agent import run_market_agent
from agents.listing_agent import run_listing_agent
from agents.translator_agent import run_translator_agent
from agents.scoring_agent import run_scoring_agent

def run_pipeline(memory):
    # Log starting run
    with open("logs/runs.log", "a") as f:
        f.write(f"[{datetime.datetime.now()}] Starting pipeline for artisan {memory.artisan_profile.get('name')}\n")

    # Step 1: Run Brand Agent
    memory = run_brand_agent(memory)
    
    # Step 2: Run Market Agent
    memory = run_market_agent(memory)
    
    # Step 3: Run Listing Agent
    memory = run_listing_agent(memory)
    
    # Step 4: Run Translator Agent
    memory = run_translator_agent(memory)
    
    # Step 5: Run Scoring Agent
    memory = run_scoring_agent(memory)

    # Log completion
    with open("logs/runs.log", "a") as f:
        f.write(f"[{datetime.datetime.now()}] Completed pipeline for artisan {memory.artisan_profile.get('name')}\n")

    return memory
