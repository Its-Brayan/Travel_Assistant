from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import ITINERARY_PROMPT
from Code.prompt_builder import build_prompt_body

class ItineraryAgent:

    def itinerary_result(self):
        prompt = build_prompt_body(load_config(ITINERARY_PROMPT))
        llm = get_llm('llama-3.3-70b-versatile')
        response = llm.invoke(prompt)
        return{
            'itinerary':response
        }