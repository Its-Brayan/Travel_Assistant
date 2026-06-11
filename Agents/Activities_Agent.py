from Code.llm import get_llm
from Code.paths import ACTIVITIES_PROMPT
from Code.prompt_builder import build_prompt_body
from Code.load_yaml import load_config
from langchain_mcp_adapters.tools import load_mcp_tools
class ActivitesAgent:
    llm = get_llm('llama-3.3-70b-versatile')
    async def plan_activites(self,query:str, mcp_session:dict):
        web_search = mcp_session.get('web_search')
        tools = await load_mcp_tools(web_search)
        llm_with_tools = self.llm.bind_tools(tools)
        config = load_config(ACTIVITIES_PROMPT)
        print("PLAN INPUT:", query)
        print("TOOLS LOADED:",tools)
        prompt = build_prompt_body(config['activities_agent'],query)
        response = await llm_with_tools.ainvoke(prompt)

        return {
            'activity_plan':response
        }
