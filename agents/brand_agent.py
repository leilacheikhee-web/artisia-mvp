import json
from utils.llm_client import call_llm
from utils.prompts import BRAND_PROMPT

def brand_agent(memory):
    """
    Artisia Brand Agent.
    Creates an authentic brand story from artisan and product data.
    """
    # Prepare inputs for the prompt
    # Depending on whether memory is a dict or ProductMemory object
    try:
        artisan_profile = memory["artisan_profile"]
        product = memory["product"]
        story_input = memory["story_input"]
    except (TypeError, KeyError):
        artisan_profile = getattr(memory, "artisan_profile", {})
        product = getattr(memory, "product", {})
        story_input = getattr(memory, "story_input", {})

    prompt = BRAND_PROMPT.format(
        artisan_profile=json.dumps(artisan_profile),
        product=json.dumps(product),
        story_input=json.dumps(story_input)
    )
    
    # Call the shared LLM client
    response_text = call_llm(prompt)
    
    if not response_text:
        raise Exception("Agent failed: No response from LLM.")
        
    try:
        # Parse output into JSON
        story_data = json.loads(response_text)
        
        # Store in memory (handling both dict and ProductMemory)
        if isinstance(memory, dict):
            memory["story"] = story_data
        else:
            # Assuming ProductMemory has add_field or direct attribute access
            memory.story = story_data
            
        return story_data
        
    except json.JSONDecodeError:
        print(f"RAW LLM TEXT COULD NOT BE PARSED: {response_text}")
        raise Exception("Agent failed: LLM output is not valid JSON.")
