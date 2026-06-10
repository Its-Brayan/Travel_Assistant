from Code.llm import get_llm
from Code.paths import ACCOMODATION_PROMPT
from Code.load_yaml import load_config
from Code.prompt_builder import build_prompt_body

class AccomodationAgent():

    def accomodate(self, query:str):
        config = load_config(ACCOMODATION_PROMPT)
        prompt = build_prompt_body(config['accommodation_agent'],query)
        llm = get_llm('llama-3.3-70b-versatile')
        result = llm.invoke(prompt)

        return{
            'accomodation_result':result
        } 