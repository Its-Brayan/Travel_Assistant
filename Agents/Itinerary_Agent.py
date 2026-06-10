from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import ITINERARY_PROMPT
from Code.prompt_builder import build_prompt_body

class ItineraryAgent:

    def itinerary_result(self,accomodator:str,activities:str,budgeter:str):
        config = load_config(ITINERARY_PROMPT)
        prompt = build_prompt_body(config['itinerary_agent'])
        prompt += accomodator
        prompt += activities
        prompt += budgeter
        llm = get_llm('llama-3.3-70b-versatile')
        response = llm.invoke(prompt)
        return{
            'itinerary':response
        }