import json
from utils.llm_client import call_llm
from utils.prompts import MARKET_PROMPT

def market_agent(memory):
    """
    Artisia Market Agent.
    Estimates pricing range and target audience based on product and market data.
    """
    try:
        product = memory["product"]
        market_input = memory["market_input"]
    except (TypeError, KeyError):
        product = getattr(memory, "product", {})
        market_input = getattr(memory, "market_input", {})
        
    prompt = MARKET_PROMPT.format(
        product=json.dumps(product),
        market_input=json.dumps(market_input)
    )
    
    response_text = call_llm(prompt)
    
    if not response_text:
        raise Exception("Agent failed: No response from LLM.")
        
    try:
        market_data = json.loads(response_text)
        
        # Store in memory
        if isinstance(memory, dict):
            memory["market"] = market_data
        else:
            memory.market = market_data
            
        return market_data
        
    except json.JSONDecodeError:
        print(f"RAW LLM TEXT COULD NOT BE PARSED: {response_text}")
        raise Exception("Agent failed: LLM output is not valid JSON.")
