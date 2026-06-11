from Code.llm import get_llm
from Code.paths import ACTIVITIES_PROMPT
from Code.prompt_builder import build_prompt_body
from Code.load_yaml import load_config
from langchain_mcp_adapters.tools import load_mcp_tools
class ActivitesAgent:
    async def plan_activites(self,query:str, mcp_session:dict):
        web_search = mcp_session.get('web_search')
        tools = await load_mcp_tools(web_search)
        llm = get_llm('llama-3.3-70b-versatile')
        llm_with_tools = llm.bind_tools(tools)
        config = load_config(ACTIVITIES_PROMPT)
        prompt = build_prompt_body(config['activities_agent'],query)
        response = llm_with_tools.invoke(prompt)

        return {
            'activity_plan':response
        }
