from Workflows.graph import run_pipeline
import streamlit as st
import asyncio
from groq import RateLimitError
from datetime import date
import traceback
import json
st.set_page_config(
    page_title="Travel Planner",
    layout="wide"   
)
st.title("🌍 Travel Planner")



if "result" not in st.session_state:
    st.session_state.result = None


query = st.text_area("Enter your travel request")

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start Date",
        min_value = date.today()
    )

with col2:
    duration = st.number_input(
        "Number of days",
        min_value=1,
        max_value= 30,
        value = 3
    )

def run_async_pipeline(inputs):
    return asyncio.run(run_pipeline(inputs))

if st.button("Plan Trip 🚀"):
 
    if not query:
        st.warning("Please enter a travel request")
        st.stop()

    inputs = {
        "query": query,
        "start_date": str(start_date),
        "duration": int(duration)
    }

    with st.spinner("Planning your trip..."):
        try:
            result = run_async_pipeline(inputs)
            st.session_state.result = result

        except Exception:
            st.error(f"Error: {traceback.format_exc()}")

# ----------------------------
# Output section
# ----------------------------
if st.session_state.result:
    st.subheader("📍 Generated Plan")

    res = st.session_state.result
  

    # st.markdown("### 🧭 Overview")
    # plan = st.write(res.get("plan"))
    # try:
    #     plan = json.load(plan)
    #     st.json(plan)
    # except:
    #     st.markdown(plan)

   
    # 1. Hide planner JSON completely
    st.markdown("### 🧭 Overview")
    st.markdown(res.get("plan", ""))

    # 2. Clean sections only
    st.markdown("### 🏨 Accommodation")
    st.markdown(res.get("accomodate", ""))

    st.markdown("### 🎯 Activities")
    st.markdown(res.get("activities", ""))

    st.markdown("### 💰 Budget")
    st.markdown(res.get("budget", ""))

    st.markdown("### 🗺️ Itinerary")
    st.markdown(res.get("itinerary", ""))

    st.download_button(
        label="Download Plan",
        data=str(st.session_state.result),
        file_name="travel_plan.json"
    )