import sys
import os
import shutil
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT_DIR)
from Agents.Planner_Agent import PlannerAgent
from Agents.Accomodation_Agent import AccomodationAgent
from Agents.Activities_Agent import ActivitesAgent
from Agents.Budget_Agent import BudgetAgent
from Agents.Itinerary_Agent import ItineraryAgent
from langgraph.graph import StateGraph,END
from typing import TypedDict
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client,StdioServerParameters
import asyncio
from langgraph.types import interrupt
import traceback

uvx_path = shutil.which('uvx')
npx_path = shutil.which('npx') or "npx"
print(npx_path)
PlannerAgent = PlannerAgent()
AccomodationAgent = AccomodationAgent()
ActivitesAgent = ActivitesAgent()
BudgetAgent = BudgetAgent()
ItineraryAgent = ItineraryAgent()
class TravelAgent(TypedDict):
    query: str
    plan: str
    accomodate:str
    activities:str
    duration: str
    start_date:str
    budget:str
    itinerary:str
    mcp_session:ClientSession

def planner_node(state:TravelAgent):
    # user_input = interrupt({
    #     "Message":"Please confirm trip dates and number of days"
    # })
    # state['start_date'] = user_input['start_date']
    # state['duration'] = user_input['duration']
    print("Planner Agent is thinking...")
    plan_result = PlannerAgent.plan(state['query'])
    result = plan_result['plan_result']
    clean_text = result.content
    print(f"Examining the question{state['query']}")
    if isinstance(clean_text,dict):
        clean_text = "/n".join(f"{k}:{v}" for k,v in clean_text.items())
    return{
        'plan' : clean_text
    }

def accomodation_node(state:TravelAgent):
    print("Finding the best hotel...")
    accomodation_result = AccomodationAgent.accomodate(state['plan'])
    result = accomodation_result['accomodation_result']
    clean_text = result.content
    print("Comparing prices...")
    if isinstance(clean_text,dict):
        clean_text = "\n".join(f"{k}:{v}" for k,v in clean_text.items())
    return{
        'accomodate':clean_text
    }

def activites_node(state:TravelAgent):
   print("Finding activities...")
   acitivities_result = ActivitesAgent.plan_activites(state['plan'])
   result = acitivities_result['activity_plan']
   clean_text = result.content
   if isinstance(clean_text,dict):
       clean_text = "\n".join(f"{k}:{v}" for k, v in clean_text.items())
   return{
       'activities': clean_text
   }

def budget_node(state:TravelAgent):
    print("Calculating budget and ensuring compliance...")
    budget_result = BudgetAgent.budget_plan(state['plan'])
    result = budget_result['budget_plan']
    clean_text = result.content
    if isinstance(clean_text,dict):
        clean_text = "\n".join(f"{k}:{v}" for k,v in clean_text.items())
    return{
        'budget': clean_text
    }

def itinerary_node(state:TravelAgent):
    print("Compiling Everything...")
    itinerary_result = ItineraryAgent.itinerary_result(
        accomodator=state['accomodate'],
        activities=state['activities'],
        budgeter=state['budget']
    )
    result = itinerary_result['itinerary']
    clean_text = result.content
    if isinstance(clean_text,dict):
        clean_text = "\n".join(f"{k}:{v}" for k, v in clean_text.items())
    return{
        'itinerary':clean_text
    }


def run_graph() -> StateGraph:
    workflow = StateGraph(TravelAgent)

    workflow.add_node('planner',planner_node)
    workflow.add_node('accomodator',accomodation_node)
    workflow.add_node('activities',activites_node)
    workflow.add_node('budgeter',budget_node)
    workflow.add_node('itinerary',itinerary_node)

    workflow.set_entry_point('planner')

    workflow.add_edge('planner','accomodator')
    workflow.add_edge('planner','activities')
    workflow.add_edge('planner','budgeter')
    workflow.add_edge('accomodator','itinerary')
    workflow.add_edge('activities','itinerary')
    workflow.add_edge('budgeter','itinerary')
    workflow.add_edge('itinerary',END)

    return workflow.compile()


async def run_pipeline(query:str):
     print(f"\n{'='*60}")
     print(f"Starting pipeline for {query}")
     print(f"\n{'='*60}\n")
     print("Starting MCP connection...")
     mcp_env = os.environ.copy()
     mcp_env["CURRENCY_EXCHANGE"] = os.getenv('CURRENCY_EXCHANGE')
     servers ={
         "weather":StdioServerParameters(
         command=sys.executable,
         args=[
        "-m",
        "mcp_weather_server"
      ],
      
     ),
     "web_search":StdioServerParameters(
         command = uvx_path,
         args=["duckduckgo-mcp-server"],
         env = {
                "DDG_SAFE_SEARCH": "STRICT",
                "DDG_REGION": ""
            }

     ),
     "currency-conversion": StdioServerParameters(
         command ='npx',
         args = [ 
        "-y",
        "mcp-remote",
        "https://vector384--currency-exchange-mcp.apify.actor/mcp",
        "--header",
        f"Authorization: Bearer {mcp_env}"
         ]
               
     )
     }
     sessions = {}
     for name, server_params in servers.items():
         async with stdio_client(server_params) as (read,write):
           async with ClientSession(read,write) as session:
                print("Transport (stdio) connected")
                print("Session created")
                await session.initialize()
                print("MCP initialized successfully")
                sessions[name] = session
                tools = await session.list_tools()
                print("Tools from: ",name )
                print("TOOLS",tools)
                for tool in tools.tools:
                 print(f"- {tool.name}")
     graph = run_graph()
     result = await graph.ainvoke(
                       {
                         "query":query,
                         'plan': '',
                         'accomodate':'',
                        'activities':'',
                        'budget':'',
                        'itinerary':'',
                        'mcp_session':session
                     }
                 )
     print(f"\n{'='*60}")
     print(f"Pipeline Complete")
     print(f"{'='*60}\n")

     return result
             



# if __name__ == '__main__':
#     result = asyncio.run(run_pipeline("hello"))
#     print(result)