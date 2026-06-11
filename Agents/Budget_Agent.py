from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import BUDGET_PROMPT
from Code.prompt_builder import build_prompt_body
from langchain_mcp_adapters.tools import load_mcp_tools
class BudgetAgent:
   async def budget_plan(self, query:str, mcp_session:dict):
        currency_session = mcp_session.get('actors-mcp-server')
        tools = await load_mcp_tools(currency_session)
        llm = get_llm('llama-3.3-70b-versatile')
        llm_with_tools = llm.bind_tools(tools)
        config = load_config(BUDGET_PROMPT)
        prompt = build_prompt_body(config['budget_agent'],query)
      
        response = llm_with_tools.invoke(prompt)
        return{
            'budget_plan':response
        }