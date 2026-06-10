from Code.llm import get_llm
from Code.paths import ACTIVITIES_PROMPT
from Code.prompt_builder import build_prompt_body
from Code.load_yaml import load_config

class ActivitesAgent:
    def plan_activites(self,query:str):
        config = load_config(ACTIVITIES_PROMPT)
        prompt = build_prompt_body(config['activities_agent'],query)
        llm = get_llm('llama-3.3-70b-versatile')
        response = llm.invoke(prompt)

        return {
            'activity_plan':response
        }
