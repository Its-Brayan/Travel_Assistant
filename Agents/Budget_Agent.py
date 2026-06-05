from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import BUDGET_PROMPT
from Code.prompt_builder import build_prompt_body

class BudgetAgent:
    def budget_plan(self, query:str):
        prompt = build_prompt_body(load_config(BUDGET_PROMPT),query)
        llm = get_llm('llama-3.3-70b-versatile')
        response = llm.invoke(prompt)
        return{
            'budget_plan':response
        }