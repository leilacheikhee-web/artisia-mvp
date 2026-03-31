import json
from utils.ollama_client import call_ollama
from utils.prompts import BRAND_PROMPT

def run_brand_agent(memory):
    prompt = BRAND_PROMPT.format(
        artisan_profile=json.dumps(memory.artisan_profile),
        product=json.dumps(memory.product),
        story_input=json.dumps(memory.story_input)
    )
    
    response = call_ollama(prompt)
    if response:
        try:
            story_data = json.loads(response)
            memory.add_field("story", story_data)
        except json.JSONDecodeError:
            print("Failed to parse brand agent output.")
    return memory
