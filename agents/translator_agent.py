import json
from utils.llm_client import call_llm
from utils.prompts import TRANSLATOR_PROMPT

def translator_agent(memory):
    """
    Artisia Translator Agent.
    Generates English and French listings from the listing section.
    """
    try:
        listing = memory["listing"]
    except (TypeError, KeyError):
        listing = getattr(memory, "listing", {})
        
    prompt = TRANSLATOR_PROMPT.format(
        listing=json.dumps(listing)
    )
    
    response_text = call_llm(prompt)
    
    if not response_text:
        raise Exception("Agent failed: No response from LLM.")
        
    try:
        translation_data = json.loads(response_text)
        
        # Store in memory
        if isinstance(memory, dict):
            memory["translation"] = translation_data
        else:
            memory.translation = translation_data
            
        return translation_data
        
    except json.JSONDecodeError:
        print(f"RAW LLM TEXT COULD NOT BE PARSED: {response_text}")
        raise Exception("Agent failed: LLM output is not valid JSON.")
