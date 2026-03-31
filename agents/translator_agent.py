import json
from utils.ollama_client import call_ollama
from utils.prompts import TRANSLATOR_PROMPT

def run_translator_agent(memory):
    prompt = TRANSLATOR_PROMPT.format(
        listing=json.dumps(memory.listing)
    )
    
    response = call_ollama(prompt)
    if response:
        try:
            translation_data = json.loads(response)
            memory.add_field("translation", translation_data)
        except json.JSONDecodeError:
            print("Failed to parse translator agent output.")
    return memory
