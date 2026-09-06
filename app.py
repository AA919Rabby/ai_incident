import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import streamlit as st
from src.orchestrator.crew_manager import IncidentOrchestrator

st.set_page_config(page_title="Smart City AI", layout="wide")

st.title("🏙️ Agentic AI Smart City Incident Manager")

# Initialize orchestrator
if 'orchestrator' not in st.session_state:
    with st.spinner("Loading..."):
        st.session_state.orchestrator = IncidentOrchestrator()
    st.success("System Ready!")

# --- UI STATE MANAGEMENT ---
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'ai_result' not in st.session_state:
    st.session_state.ai_result = None
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

def lock_ui():
    """Immediately locks the UI before any AI processing starts"""
    st.session_state.is_processing = True
    st.session_state.ai_result = None

# --- THE INPUT UI ---
# These are strictly tied to the 'is_processing' variable.
st.session_state.user_input = st.text_area(
    "Describe the Incident or Ask for News:",
    value=st.session_state.user_input,
    placeholder="e.g., tell me the latest traffic news in tongi",
    disabled=st.session_state.is_processing  # Greys out text box while running
)

# Button instantly triggers lock_ui()
st.button(
    "Process Incident",
    disabled=st.session_state.is_processing, # Greys out button while running
    on_click=lock_ui
)

# --- THE PROCESSING LOGIC ---
if st.session_state.is_processing:
    if not st.session_state.user_input.strip():
        st.warning("Please enter some text.")
        st.session_state.is_processing = False
        st.rerun()
    else:
        try:
            with st.spinner("AI Agents are gathering sources and analyzing... (Please wait)"):
                st.session_state.ai_result = st.session_state.orchestrator.process_incident(st.session_state.user_input)
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
        finally:
            # Unlocks the UI when finished and refreshes screen
            st.session_state.is_processing = False
            st.rerun()

# --- THE RESULTS UI ---
if st.session_state.ai_result is not None:
    response = st.session_state.ai_result

    col1, col2 = st.columns(2)
    with col1:
        st.header("🎯 1. Final Action Plan")
        st.info("The final result and recommendations.")
        st.markdown(response["final_action_plan"])

    with col2:
        st.header("🔎 2. Data Source & Reasoning")
        st.warning("Where found this information and its analysis.")
        st.markdown(response["source_info"])