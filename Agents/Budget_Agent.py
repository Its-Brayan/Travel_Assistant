from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import BUDGET_PROMPT
from Code.prompt_builder import build_prompt_body

class BudgetAgent:
    def budget_plan(self, query:str):
        config = load_config(BUDGET_PROMPT)
        prompt = build_prompt_body(config['budget_agent'],query)
        llm = get_llm('llama-3.3-70b-versatile')
        response = llm.invoke(prompt)
        return{
            'budget_plan':response
        }