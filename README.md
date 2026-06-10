# Travel Planner

A travel planning application built around an agent-based orchestration pipeline. Users submit a travel query through Streamlit, and the system coordinates multiple specialized agents to produce accommodation suggestions, activity plans, budgets, and a final itinerary.

## Architecture Overview

- `app.py` is the Streamlit entrypoint.
- `Workflows/graph.py` defines the planning pipeline as a state graph.
- Individual agents live under the `Agents/` directory.
- Agent prompts are stored in `Config/` and built with helpers from `Code/`.
- The system may use external MCP services for weather, web search, and currency conversion.

## Components

### 1. Streamlit UI (`app.py`)

The UI collects:
- `query` — the user travel request
- `start_date` — trip start date
- `duration` — number of days

When the user clicks **Plan Trip**, the app calls `Workflows.graph.run_pipeline(...)` and renders the returned plan sections.

### 2. Workflow Graph (`Workflows/graph.py`)

The workflow uses `langgraph.graph.StateGraph` and a typed state dictionary named `TravelAgent`.

The pipeline nodes are:
- `planner` — builds the initial travel plan
- `accomodator` — finds accommodations
- `activities` — develops a daily activity plan
- `budgeter` — estimates costs and checks budget compliance
- `itinerary` — assembles the final itinerary from previous outputs

Edges connect the nodes so the planner runs first, then accommodation/activity/budget agents run in parallel, and finally the itinerary agent combines their results.

### 3. Agent Modules

Each agent is implemented in `Agents/`:

- `Planner_Agent.py` — creates the main travel plan prompt and invokes the LLM
- `Accomodation_Agent.py` — finds hotels and lodging options
- `Activities_Agent.py` — builds daily schedules and may consult weather context
- `Budget_Agent.py` — estimates costs and budget compliance
- `Itinerary_Agent.py` — creates the final trip itinerary from earlier outputs

Each agent loads its prompt configuration from `Config/` using helper functions in `Code/`.

### 4. Prompt Management

The `Code/` directory contains shared helpers:
- `load_yaml.py` — loads YAML prompt configs
- `prompt_builder.py` — builds prompt bodies from YAML templates
- `llm.py` — gets the configured language model
- `paths.py` — stores prompt path constants

This separation keeps agent logic clean and lets prompts be updated separately.

### 5. MCP Integration

`Workflows/graph.py` also prepares MCP sessions for tool access:
- Weather service (`mcp_weather_server`)
- DuckDuckGo search (`duckduckgo-mcp-server`)
- Currency conversion MCP

These are launched as subprocess-backed sessions and listed for available tools before the workflow begins.

## How the Orchestration Works

1. `app.py` gathers user inputs and calls `run_pipeline`.
2. `run_pipeline` optionally spins up MCP servers and builds a `sessions` map.
3. The workflow graph is compiled and invoked with an initial state payload.
4. The `planner_node` generates the travel plan text.
5. `accomodation_node`, `activites_node`, and `budget_node` each receive the planner output and produce specialized results.
6. `itinerary_node` combines the accommodation, activity, and budget outputs into the final itinerary.
7. `app.py` renders the result sections and provides a download button.

## Running the Project

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

4. Open the browser URL shown in the terminal.

## Notes

- The system expects a working `uvx` or compatible MCP command for web search, and `npx` for currency conversion MCP.
- Prompt YAML files under `Config/` define the agent instructions and expected output format.
- The app currently renders the plan sections as Markdown instead of raw JSON.

## Directory Structure

```
app.py
requirements.txt
Agents/
  Accomodation_Agent.py
  Activities_Agent.py
  Budget_Agent.py
  Itinerary_Agent.py
  Planner_Agent.py
Code/
  llm.py
  load_yaml.py
  paths.py
  prompt_builder.py
Config/
  accomodation_prompt.yaml
  activities_prompt.yaml
  budget_prompt.yaml
  itinerary_prompt.yaml
  planner_prompt.yaml
Tools/
  weathertool.py
  websearch.py
Workflows/
  graph.py
```

## Contribution

- Update prompts in `Config/` for agent behavior changes.
- Change orchestration logic in `Workflows/graph.py` to add or reorder nodes.
- Adjust UI behavior in `app.py` if you want different user-facing layout or input fields.
