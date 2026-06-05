import os

ROOT_CONFIG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT_CONFIG,'Config')
ACCOMODATION_PROMPT = os.path.join(CONFIG_DIR,'accomodation_prompt.yaml')
ACTIVITIES_PROMPT = os.path.join(CONFIG_DIR,'activities_prompt.yaml')
BUDGET_PROMPT = os.path.join(CONFIG_DIR,'budget_prompt.yaml')
ITINERARY_PROMPT = os.path.join(CONFIG_DIR,'itinerary_prompt.yaml')
PLANNER_PROMPT = os.path.join(CONFIG_DIR,'planner_prompt.yaml')