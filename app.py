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
            def sanitize_result(obj):
                # Remove or stringify non-serializable/internal objects
                if isinstance(obj, dict):
                    out = {}
                    for k, v in obj.items():
                        if k == 'mcp_session':
                            out[k] = '<hidden:mcp_session>'
                            continue
                        out[k] = sanitize_result(v)
                    return out
                # unwrap objects with .content attribute (LLM responses)
                if hasattr(obj, 'content'):
                    try:
                        return sanitize_result(obj.content)
                    except Exception:
                        return str(obj.content)
                if isinstance(obj, (list, tuple)):
                    return [sanitize_result(x) for x in obj]
                if isinstance(obj, (str, int, float, bool)) or obj is None:
                    return obj
                try:
                    return str(obj)
                except Exception:
                    return '<unserializable>'

            st.session_state.result = sanitize_result(result)

        except Exception:
            st.error(f"Error: {traceback.format_exc()}")

# ----------------------------
# Output section
# ----------------------------
if st.session_state.result:
    st.subheader("📍 Generated Plan")

    plan = st.session_state.result

    # Friendly rendering of common fields
    if isinstance(plan, dict):
        if 'query' in plan:
            st.markdown(f"**Request:** {plan.get('query')}" )

        if 'plan' in plan:
            st.markdown("**Plan:**")
            st.write(plan.get('plan'))

        if 'accomodate' in plan:
            st.markdown("**Accommodation Recommendations:**")
            st.write(plan.get('accomodate'))

        if 'activities' in plan:
            st.markdown("**Activities:**")
            st.write(plan.get('activities'))

        if 'budget' in plan:
            st.markdown("**Budget:**")
            st.write(plan.get('budget'))

        if 'itinerary' in plan:
            st.markdown("**Itinerary:**")
            st.write(plan.get('itinerary'))

        # Fallback: show any other keys as collapsible JSON
        other_keys = {k: v for k, v in plan.items() if k not in {'query','plan','accomodate','activities','budget','itinerary'}}
        if other_keys:
            with st.expander("Other plan details (JSON)"):
                st.json(other_keys)

        # Download sanitized JSON
        st.download_button(
            label="Download Plan",
            data=json.dumps(plan, indent=2, ensure_ascii=False),
            file_name="travel_plan.json",
            mime='application/json'
        )
    else:
        st.write(plan)