import json
from utils.llm_client import call_llm
from utils.prompts import LISTING_PROMPT

def listing_agent(memory):
    """
    Artisia Listing Agent.
    Creates a marketplace listing using brand and market info.
    """
    try:
        product = memory["product"]
        story = memory["story"]
        market = memory["market"]
    except (TypeError, KeyError):
        product = getattr(memory, "product", {})
        story = getattr(memory, "story", {})
        market = getattr(memory, "market", {})
        
    prompt = LISTING_PROMPT.format(
        product=json.dumps(product),
        story=json.dumps(story),
        market=json.dumps(market)
    )
    
    response_text = call_llm(prompt)
    
    if not response_text:
        raise Exception("Agent failed: No response from LLM.")
        
    try:
        listing_data = json.loads(response_text)
        
        # Store in memory
        if isinstance(memory, dict):
            memory["listing"] = listing_data
        else:
            memory.listing = listing_data
            
        return listing_data
        
    except json.JSONDecodeError:
        print(f"RAW LLM TEXT COULD NOT BE PARSED: {response_text}")
        raise Exception("Agent failed: LLM output is not valid JSON.")
