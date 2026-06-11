from Code.paths import PLANNER_PROMPT
from Code.llm import get_llm
from Code.prompt_builder import build_prompt_body
from Code.load_yaml import load_config
class PlannerAgent:
    llm = get_llm('llama-3.3-70b-versatile')
    def plan(self, query: str):
        config = load_config(PLANNER_PROMPT)
        prompt = build_prompt_body(config['planner_agent'],query)
        print(f"Here is the prompt:{prompt}")
        output = self.llm.invoke(prompt)

        result = {
            'plan_result':output
        }
        return result

