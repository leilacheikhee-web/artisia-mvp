import json
from utils.ollama_client import call_ollama
from utils.prompts import LISTING_PROMPT

def run_listing_agent(memory):
    prompt = LISTING_PROMPT.format(
        story=json.dumps(memory.story),
        market=json.dumps(memory.market),
        product=json.dumps(memory.product)
    )
    
    response = call_ollama(prompt)
    if response:
        try:
            listing_data = json.loads(response)
            memory.add_field("listing", listing_data)
        except json.JSONDecodeError:
            print("Failed to parse listing agent output.")
    return memory
