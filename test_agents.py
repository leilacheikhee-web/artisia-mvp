import json
from agents.brand_agent import brand_agent
from agents.market_agent import market_agent
from agents.listing_agent import listing_agent
from agents.translator_agent import translator_agent

# 1. Create a sample ProductMemory (as a dictionary for generic compatibility)
memory = {
    "artisan_profile": {
        "name": "Chuchu",
        "region": "Lahore"
    },
    "product": {
        "name": "Handmade embroidered handbag",
        "materials": ["cotton fabric", "silk thread"],
        "technique": "traditional embroidery",
        "production_time": "5 hours"
    },
    "story_input": {
        "start_year": "2018",
        "inspiration": "learned from grandmother",
        "emotion": "proud when customers buy"
    },
    "market_input": {
        "current_price": "$20",
        "customers": "local women",
        "sales_channels": "Instagram and craft markets"
    }
}

def run_tests():
    print("--- TESTING BRAND AGENT ---")
    try:
        brand_data = brand_agent(memory)
        print(json.dumps(brand_data, indent=2))
    except Exception as e:
        print(f"Brand Agent Error: {e}")

    print("\n--- TESTING MARKET AGENT ---")
    try:
        market_data = market_agent(memory)
        print(json.dumps(market_data, indent=2))
    except Exception as e:
        print(f"Market Agent Error: {e}")

    print("\n--- TESTING LISTING AGENT ---")
    try:
        listing_data = listing_agent(memory)
        print(json.dumps(listing_data, indent=2))
    except Exception as e:
        print(f"Listing Agent Error: {e}")

    print("\n--- TESTING TRANSLATOR AGENT ---")
    try:
        translator_data = translator_agent(memory)
        print(json.dumps(translator_data, indent=2))
    except Exception as e:
        print(f"Translator Agent Error: {e}")

if __name__ == "__main__":
    run_tests()
