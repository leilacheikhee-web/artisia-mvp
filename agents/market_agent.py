import json
from utils.ollama_client import call_ollama
from utils.prompts import MARKET_PROMPT

def run_market_agent(memory):
    prompt = MARKET_PROMPT.format(
        product=json.dumps(memory.product),
        market_input=json.dumps(memory.market_input)
    )
    
    response = call_ollama(prompt)
    if response:
        try:
            market_data = json.loads(response)
            memory.add_field("market", market_data)
        except json.JSONDecodeError:
            print("Failed to parse market agent output.")
    return memory
