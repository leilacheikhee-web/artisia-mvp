import json
from utils.ollama_client import call_ollama
from utils.prompts import SCORING_PROMPT

def run_scoring_agent(memory):
    prompt = SCORING_PROMPT.format(
        memory=memory.model_dump_json()
    )
    
    response = call_ollama(prompt)
    if response:
        try:
            scoring_data = json.loads(response)
            memory.add_field("score", scoring_data)
        except json.JSONDecodeError:
            print("Failed to parse scoring agent output.")
    return memory
