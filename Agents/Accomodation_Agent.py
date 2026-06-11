from Code.llm import get_llm
from Code.paths import ACCOMODATION_PROMPT
from Code.load_yaml import load_config
from Code.prompt_builder import build_prompt_body
from langchain_mcp_adapters.tools import load_mcp_tools
class AccomodationAgent():
    llm = get_llm('llama-3.3-70b-versatile')
    async def accomodate(self, query:str, mcp_session:dict):
        search_session = mcp_session.get('web_search')
        tools = await load_mcp_tools(search_session)
        llm_with_tools = self.llm.bind_tools(tools)
        config = load_config(ACCOMODATION_PROMPT)
        prompt = build_prompt_body(config['accommodation_agent'],query)
       
        result = await llm_with_tools.ainvoke(prompt)

        return{
            'accomodation_result':result
        } 