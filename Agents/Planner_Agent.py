from Code.paths import PLANNER_PROMPT
from Code.llm import get_llm
from Code.prompt_builder import build_prompt_body
from Code.load_yaml import load_config
class PlannerAgent:

    def plan(self, query: str):
        prompt = build_prompt_body(load_config(PLANNER_PROMPT),query)
        llm = get_llm('llama-3.3-70b-versatile')
        output = llm.invoke(prompt)

        result = {
            'plan_result':output
        }
        return result

