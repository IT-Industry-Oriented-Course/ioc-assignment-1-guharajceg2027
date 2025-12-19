"""
Streamlit web UI for Clinical Workflow Automation Agent.
Professional interface for healthcare workflow management.
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from agent import ClinicalAgent
from functions import FUNCTION_MAP, FUNCTION_SCHEMAS
from data_store import data_store

# Page configuration
st.set_page_config(
    page_title="Clinical Workflow Automation",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Default API key
DEFAULT_API_KEY = "guha_key"

# Professional CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1f4788;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4788;
        margin: 0.5rem 0;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #28a745;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #dc3545;
    }
    .info-msg {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "api_key" not in st.session_state:
    st.session_state.api_key = DEFAULT_API_KEY
if "dry_run" not in st.session_state:
    st.session_state.dry_run = False
if "request_history" not in st.session_state:
    st.session_state.request_history = []
if "auto_init" not in st.session_state:
    st.session_state.auto_init = True
if "current_request" not in st.session_state:
    st.session_state.current_request = ""

def initialize_agent():
    """Initialize the agent with current settings."""
    try:
        if not st.session_state.api_key or st.session_state.api_key.strip() == "":
            st.error("Please enter a valid API key")
            return False
        st.session_state.agent = ClinicalAgent(
            hf_api_key=st.session_state.api_key,
            dry_run=st.session_state.dry_run
        )
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return False

def ensure_agent_initialized():
    """Ensure agent is initialized, auto-initialize if enabled."""
    if not st.session_state.agent:
        if st.session_state.auto_init:
            if initialize_agent():
                return True
            else:
                st.warning("Auto-initialization failed. Please check your API key and try again.")
                return False
        else:
            st.warning("Please initialize the agent from the sidebar first")
            return False
    return True

# Sidebar
with st.sidebar:
    st.title("Configuration")
    
    st.subheader("API Settings")
    api_key_input = st.text_input(
        "HuggingFace API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your HuggingFace API key"
    )
    st.session_state.api_key = api_key_input
    
    st.subheader("Operation Mode")
    dry_run = st.checkbox(
        "Dry-Run Mode",
        value=st.session_state.dry_run,
        help="Simulate actions without executing them"
    )
    st.session_state.dry_run = dry_run
    
    auto_init = st.checkbox(
        "Auto-Initialize Agent",
        value=st.session_state.auto_init,
        help="Automatically initialize agent on page load"
    )
    st.session_state.auto_init = auto_init
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Initialize", type="primary", use_container_width=True):
            if initialize_agent():
                st.success("Agent initialized successfully")
                st.rerun()
    
    with col2:
        if st.button("Reset", use_container_width=True):
            st.session_state.agent = None
            st.session_state.request_history = []
            st.session_state.current_request = ""
            st.rerun()
    
    st.divider()
    
    st.subheader("System Statistics")
    if st.session_state.agent:
        log_count = len(st.session_state.agent.action_log)
        st.metric("Audit Log Entries", log_count)
        mode_status = "Dry-Run" if st.session_state.dry_run else "Live"
        st.metric("Operation Mode", mode_status)
        
        st.metric("Total Patients", len(data_store.patients))
        total_slots = sum(len(slots) for slots in data_store.available_slots.values())
        st.metric("Available Slots", total_slots)
        st.metric("Booked Appointments", len(data_store.appointments))
    else:
        st.info("Initialize agent to view statistics")

# Main content area
st.markdown('<div class="main-header">Clinical Workflow Automation Agent</div>', unsafe_allow_html=True)

# Navigation
page = st.selectbox(
    "Navigation",
    ["Natural Language Processing", "Quick Actions", "Audit Logs", "Analytics Dashboard", "Function Schemas", "Data Browser", "System Information"],
    label_visibility="collapsed"
)

# Natural Language Page
if page == "Natural Language Processing":
    st.header("Natural Language Request Processing")
    
    if not ensure_agent_initialized():
        st.stop()
    
    st.write("Enter your request in natural language. The agent will automatically parse your request and execute appropriate functions.")
    
    # Example requests - Fixed to work properly
    st.subheader("Example Requests")
    example_requests = [
        ("Find Patient", "Find patient Ravi Kumar"),
        ("Check Insurance", "Check insurance eligibility for patient Ravi Kumar"),
        ("Find Appointments", "Find available cardiology appointments next week"),
        ("Complete Workflow", "Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility")
    ]
    
    # Check if any example button was clicked and update state before rendering text_area
    button_clicked = False
    cols = st.columns(4)
    for i, (label, request_text) in enumerate(example_requests):
        with cols[i]:
            if st.button(label, use_container_width=True, key=f"example_btn_{i}"):
                st.session_state.current_request = request_text
                button_clicked = True
    
    # If a button was clicked, rerun to update the text area
    if button_clicked:
        st.rerun()
    
    # Request input - Read value from session state
    # Don't use a key parameter to avoid widget state conflicts
    request = st.text_area(
        "Enter your request:",
        value=st.session_state.get("current_request", ""),
        height=120,
        placeholder="Example: Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility",
        help="Type your request in natural language. The agent will automatically determine which functions to call."
    )
    
    # Update session state with current text area value
    st.session_state.current_request = request
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        process_btn = st.button("Process Request", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("Clear", use_container_width=True)
    with col3:
        if st.session_state.request_history:
            history_count = len(st.session_state.request_history)
            st.caption(f"History: {history_count} requests")
    
    if clear_btn:
        st.session_state.current_request = ""
        st.rerun()
    
    if process_btn:
        if request and request.strip():
            with st.spinner("Processing request..."):
                try:
                    response = st.session_state.agent.process_request(request)
                    
                    # Add to history
                    st.session_state.request_history.insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "request": request,
                        "response": response
                    })
                    
                    # Display response
                    st.divider()
                    st.subheader("Response")
                    
                    if response.get("refused"):
                        st.markdown('<div class="error-msg"><strong>Request Refused:</strong> ' + response.get('error', 'Unknown reason') + '</div>', unsafe_allow_html=True)
                        st.info("The agent refused this request for safety reasons. It does not provide medical advice or perform unsafe actions.")
                    elif response.get("success"):
                        st.markdown('<div class="success-msg"><strong>Request completed successfully</strong></div>', unsafe_allow_html=True)
                        
                        if response.get("summary"):
                            st.markdown('<div class="info-msg"><strong>Summary:</strong> ' + response['summary'] + '</div>', unsafe_allow_html=True)
                        
                        # Detailed results
                        if response.get("results"):
                            st.subheader("Detailed Results")
                            for i, step_result in enumerate(response["results"], 1):
                                step = step_result.get("step", "unknown")
                                result = step_result.get("result", {})
                                
                                step_title = step.replace('_', ' ').title()
                                with st.expander(f"Step {i}: {step_title}", expanded=True):
                                    if result.get("success"):
                                        st.success("Operation successful")
                                        
                                        # Format output based on step
                                        if step == "search_patient" and result.get("patient"):
                                            patient = result["patient"]
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.write("**Patient Information (FHIR Format):**")
                                                st.json(patient)
                                            with col2:
                                                name_parts = patient.get("name", [{}])[0] if patient.get("name") else {}
                                                given = " ".join(name_parts.get("given", []))
                                                family = name_parts.get("family", "")
                                                full_name = f"{given} {family}".strip()
                                                st.write("**Quick View:**")
                                                st.metric("Patient Name", full_name)
                                                st.metric("Patient ID", patient.get("id", "N/A"))
                                                if patient.get("telecom"):
                                                    for telecom in patient.get("telecom", []):
                                                        if telecom.get("system") == "phone":
                                                            st.write(f"**Phone:** {telecom.get('value')}")
                                                        elif telecom.get("system") == "email":
                                                            st.write(f"**Email:** {telecom.get('value')}")
                                        
                                        elif step == "check_insurance_eligibility" and result.get("eligibility"):
                                            elig = result["eligibility"]
                                            col1, col2, col3 = st.columns(3)
                                            with col1:
                                                st.metric("Status", elig.get('status', 'N/A'))
                                                st.metric("Provider", elig.get('provider', 'N/A'))
                                            with col2:
                                                st.metric("Policy Number", elig.get('policy_number', 'N/A'))
                                                st.metric("Coverage Type", elig.get('coverage_type', 'N/A'))
                                            with col3:
                                                st.metric("Copay Amount", f"₹{elig.get('copay_amount', 'N/A')}")
                                                st.metric("Valid Until", elig.get('valid_until', 'N/A'))
                                        
                                        elif step == "find_available_slots" and result.get("available_slots"):
                                            slots = result["available_slots"]
                                            st.write(f"**Found {len(slots)} available slots**")
                                            
                                            if slots:
                                                df_slots = pd.DataFrame([
                                                    {
                                                        "Slot ID": slot.get("slot_id"),
                                                        "Date": slot.get("date"),
                                                        "Time": slot.get("time"),
                                                        "Doctor": slot.get("doctor"),
                                                        "Duration (min)": slot.get('duration_minutes')
                                                    }
                                                    for slot in slots
                                                ])
                                                st.dataframe(df_slots, use_container_width=True, hide_index=True)
                                                
                                                csv = df_slots.to_csv(index=False)
                                                st.download_button(
                                                    label="Download as CSV",
                                                    data=csv,
                                                    file_name=f"available_slots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                                    mime="text/csv"
                                                )
                                        
                                        elif step == "book_appointment" and result.get("appointment"):
                                            apt = result["appointment"]
                                            st.success("Appointment booked successfully")
                                            
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.write("**Appointment Details:**")
                                                st.write(f"**Appointment ID:** {apt.get('appointment_id')}")
                                                st.write(f"**Patient:** {apt.get('patient_name')} ({apt.get('patient_id')})")
                                                st.write(f"**Specialty:** {apt.get('specialty')}")
                                                st.write(f"**Reason:** {apt.get('reason', 'N/A')}")
                                            with col2:
                                                st.write("**Schedule:**")
                                                st.write(f"**Date:** {apt.get('date')}")
                                                st.write(f"**Time:** {apt.get('time')}")
                                                st.write(f"**Doctor:** {apt.get('doctor')}")
                                                st.write(f"**Duration:** {apt.get('duration_minutes')} minutes")
                                                st.write(f"**Status:** {apt.get('status')}")
                                            
                                            apt_json = json.dumps(apt, indent=2)
                                            st.download_button(
                                                label="Download Appointment Confirmation",
                                                data=apt_json,
                                                file_name=f"appointment_{apt.get('appointment_id')}_{datetime.now().strftime('%Y%m%d')}.json",
                                                mime="application/json"
                                            )
                                    else:
                                        st.error(f"Operation failed: {result.get('error', 'Unknown error')}")
                                        
                    else:
                        st.markdown('<div class="error-msg"><strong>Request failed:</strong> ' + response.get('error', 'Unknown error') + '</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
                    st.exception(e)
        else:
            st.warning("Please enter a request")
    
    # Request history
    if st.session_state.request_history:
        st.divider()
        st.subheader("Request History")
        
        # Filter history
        col1, col2 = st.columns([3, 1])
        with col1:
            history_filter = st.text_input("Filter history", placeholder="Search requests...", key="history_search")
        with col2:
            show_count = st.selectbox("Show", [5, 10, 20, "All"], index=1, key="history_count")
        
        filtered_history = st.session_state.request_history
        if history_filter:
            filtered_history = [
                h for h in filtered_history
                if history_filter.lower() in h['request'].lower()
            ]
        
        count = len(filtered_history) if show_count == "All" else min(show_count, len(filtered_history))
        
        for i, hist in enumerate(filtered_history[:count]):
            with st.expander(f"{hist['timestamp']}: {hist['request'][:80]}...", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**Request:**", hist['request'])
                    status = "Success" if hist['response'].get('success') else ("Refused" if hist['response'].get('refused') else "Failed")
                    if hist['response'].get('success'):
                        st.success(status)
                    elif hist['response'].get('refused'):
                        st.error(status)
                    else:
                        st.warning(status)
                with col2:
                    st.json(hist["response"])

# Quick Actions Page
elif page == "Quick Actions":
    st.header("Quick Actions")
    st.write("Direct access to all available functions. Use these tools to perform specific actions without natural language processing.")
    
    if not ensure_agent_initialized():
        st.stop()
    
    tabs = st.tabs(["Search Patient", "Check Insurance", "Find Slots", "Book Appointment"])
    
    with tabs[0]:
        st.subheader("Search Patient")
        patient_name = st.text_input("Patient Name", placeholder="e.g., Ravi Kumar", key="search_patient_name")
        
        if st.button("Search", type="primary", key="search_btn"):
            if patient_name and patient_name.strip():
                with st.spinner("Searching..."):
                    result = FUNCTION_MAP["search_patient"](patient_name)
                    if result.get("success"):
                        st.success("Patient found")
                        patient = result.get("patient")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.json(patient)
                        with col2:
                            name_parts = patient.get("name", [{}])[0] if patient.get("name") else {}
                            given = " ".join(name_parts.get("given", []))
                            family = name_parts.get("family", "")
                            full_name = f"{given} {family}".strip()
                            st.metric("Name", full_name)
                            st.metric("Patient ID", patient.get("id", "N/A"))
                    else:
                        st.error(result.get('error'))
            else:
                st.warning("Please enter a patient name")
    
    with tabs[1]:
        st.subheader("Check Insurance Eligibility")
        patient_id = st.text_input("Patient ID", placeholder="e.g., PAT001", key="check_insurance_id")
        
        if st.button("Check Eligibility", type="primary", key="check_btn"):
            if patient_id and patient_id.strip():
                with st.spinner("Checking eligibility..."):
                    result = FUNCTION_MAP["check_insurance_eligibility"](patient_id)
                    if result.get("success"):
                        st.success("Insurance information found")
                        elig = result.get("eligibility")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Status", elig.get('status'))
                            st.metric("Provider", elig.get('provider'))
                        with col2:
                            st.metric("Policy Number", elig.get('policy_number'))
                            st.metric("Coverage Type", elig.get('coverage_type'))
                        with col3:
                            st.metric("Copay Amount", f"₹{elig.get('copay_amount')}")
                            st.metric("Valid Until", elig.get('valid_until'))
                    else:
                        st.error(result.get('error'))
            else:
                st.warning("Please enter a patient ID")
    
    with tabs[2]:
        st.subheader("Find Available Slots")
        col1, col2 = st.columns(2)
        with col1:
            specialty = st.selectbox("Specialty", ["Cardiology", "Neurology", "General Medicine"], key="find_slots_specialty")
        with col2:
            days_ahead = st.slider("Days Ahead", 1, 30, 7, key="find_slots_days")
        
        if st.button("Find Slots", type="primary", key="find_slots_btn"):
            with st.spinner("Searching for available slots..."):
                result = FUNCTION_MAP["find_available_slots"](specialty, None, days_ahead)
                if result.get("success"):
                    slots = result.get("available_slots", [])
                    st.success(f"Found {len(slots)} available slots")
                    if slots:
                        df_slots = pd.DataFrame([
                            {
                                "Slot ID": slot.get("slot_id"),
                                "Date": slot.get("date"),
                                "Time": slot.get("time"),
                                "Doctor": slot.get("doctor"),
                                "Duration (min)": slot.get('duration_minutes')
                            }
                            for slot in slots
                        ])
                        st.dataframe(df_slots, use_container_width=True, hide_index=True)
                else:
                    st.error(result.get('error'))
    
    with tabs[3]:
        st.subheader("Book Appointment")
        col1, col2 = st.columns(2)
        with col1:
            book_patient_id = st.text_input("Patient ID", key="book_patient", placeholder="e.g., PAT001")
            book_specialty = st.selectbox("Specialty", ["Cardiology", "Neurology", "General Medicine"], key="book_specialty")
        with col2:
            book_slot_id = st.text_input("Slot ID", key="book_slot", placeholder="e.g., SLOT-0001")
            book_reason = st.text_input("Reason (optional)", key="book_reason")
        
        if st.button("Book Appointment", type="primary", key="book_btn"):
            if book_patient_id and book_slot_id and book_specialty:
                with st.spinner("Booking appointment..."):
                    result = FUNCTION_MAP["book_appointment"](book_patient_id, book_slot_id, book_specialty, book_reason)
                    if result.get("success"):
                        st.success("Appointment booked successfully")
                        apt = result.get("appointment")
                        st.json(apt)
                    else:
                        st.error(result.get('error'))
            else:
                st.warning("Please fill in all required fields")

# Audit Logs Page
elif page == "Audit Logs":
    st.header("Audit Logs Viewer")
    st.write("Comprehensive audit log viewing, searching, and filtering for compliance and auditing purposes.")
    
    if not ensure_agent_initialized():
        st.stop()
    
    logs = st.session_state.agent.get_audit_log()
    
    if logs:
        # Advanced Filters Panel
        with st.expander("Advanced Filters", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                filter_type = st.selectbox(
                    "Action Type",
                    ["All"] + sorted(list(set(log.get("action_type") for log in logs if log.get("action_type")))),
                    key="audit_filter"
                )
            with col2:
                date_filter = st.date_input(
                    "Date Filter",
                    value=None,
                    key="audit_date"
                )
            with col3:
                time_range = st.selectbox(
                    "Time Range",
                    ["All Time", "Today", "Last 7 Days", "Last 30 Days"],
                    key="audit_time_range"
                )
            with col4:
                show_dry_run = st.checkbox("Include Dry-Run", value=True, key="audit_dry_run")
        
        # Search Panel
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search Logs", placeholder="Search by keyword, function name, patient ID, etc...", key="audit_search")
        with col2:
            num_entries = st.number_input(
                "Max Entries",
                min_value=10,
                max_value=len(logs),
                value=min(100, len(logs)),
                step=10,
                key="audit_num"
            )
        
        # Apply filters
        filtered_logs = logs.copy()
        
        # Filter by action type
        if filter_type != "All":
            filtered_logs = [log for log in filtered_logs if log.get("action_type") == filter_type]
        
        # Filter by date
        if date_filter:
            date_str = date_filter.strftime("%Y-%m-%d")
            filtered_logs = [log for log in filtered_logs if date_str in log.get("timestamp", "")]
        
        # Filter by time range
        if time_range != "All Time":
            today = datetime.now().date()
            if time_range == "Today":
                date_str = today.strftime("%Y-%m-%d")
                filtered_logs = [log for log in filtered_logs if date_str in log.get("timestamp", "")]
            elif time_range == "Last 7 Days":
                cutoff = (today - timedelta(days=7)).isoformat()
                filtered_logs = [log for log in filtered_logs if log.get("timestamp", "") >= cutoff]
            elif time_range == "Last 30 Days":
                cutoff = (today - timedelta(days=30)).isoformat()
                filtered_logs = [log for log in filtered_logs if log.get("timestamp", "") >= cutoff]
        
        # Filter dry-run
        if not show_dry_run:
            filtered_logs = [log for log in filtered_logs if not log.get("dry_run", False)]
        
        # Search filter
        if search_term:
            search_lower = search_term.lower()
            filtered_logs = [log for log in filtered_logs if search_lower in json.dumps(log, default=str).lower()]
        
        # Sort by timestamp (newest first)
        filtered_logs = sorted(filtered_logs, key=lambda x: x.get("timestamp", ""), reverse=True)
        filtered_logs = filtered_logs[:num_entries]
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Logs", len(logs))
        with col2:
            st.metric("Filtered Logs", len(filtered_logs))
        with col3:
            function_calls = sum(1 for log in filtered_logs if log.get("action_type") == "function_call")
            st.metric("Function Calls", function_calls)
        with col4:
            errors = sum(1 for log in filtered_logs if log.get("action_type") == "request_error" or log.get("action_type") == "function_error")
            st.metric("Errors", errors)
        
        st.divider()
        
        # View Options
        view_mode = st.radio("View Mode", ["Table View", "Detailed View", "Timeline View"], horizontal=True, key="audit_view_mode")
        
        if view_mode == "Table View":
            # Create table view
            table_data = []
            for log in filtered_logs:
                action_type = log.get("action_type", "N/A")
                timestamp = log.get("timestamp", "N/A")
                dry_run = log.get("dry_run", False)
                data = log.get("data", {})
                
                # Extract key information
                function_name = data.get("function", "N/A") if action_type == "function_call" else "N/A"
                request_text = data.get("request", "")[:50] + "..." if data.get("request") else "N/A"
                
                table_data.append({
                    "Timestamp": timestamp,
                    "Action Type": action_type,
                    "Function": function_name,
                    "Request": request_text,
                    "Dry-Run": "Yes" if dry_run else "No"
                })
            
            if table_data:
                df_logs = pd.DataFrame(table_data)
                st.dataframe(df_logs, use_container_width=True, hide_index=True)
        
        elif view_mode == "Timeline View":
            # Group by date
            logs_by_date = {}
            for log in filtered_logs:
                timestamp = log.get("timestamp", "")
                if timestamp:
                    date = timestamp.split("T")[0] if "T" in timestamp else timestamp.split(" ")[0]
                    if date not in logs_by_date:
                        logs_by_date[date] = []
                    logs_by_date[date].append(log)
            
            for date in sorted(logs_by_date.keys(), reverse=True):
                with st.expander(f"{date} - {len(logs_by_date[date])} entries", expanded=False):
                    for log in logs_by_date[date]:
                        st.json(log)
        
        else:  # Detailed View
            st.write(f"**Displaying {len(filtered_logs)} of {len(logs)} entries**")
            for i, log in enumerate(filtered_logs, 1):
                action_type = log.get("action_type", "N/A")
                timestamp = log.get("timestamp", "N/A")
                dry_run = log.get("dry_run", False)
                
                # Color code by action type
                if action_type in ["request_error", "function_error"]:
                    status_color = "🔴"
                elif action_type == "request_completed":
                    status_color = "🟢"
                else:
                    status_color = "🟡"
                
                with st.expander(f"{status_color} {i}. {timestamp} - {action_type} {'(Dry-Run)' if dry_run else ''}", expanded=False):
                    st.json(log)
        
        # Download options
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                label="Download Filtered Logs (JSON)",
                data=json.dumps(filtered_logs, indent=2, default=str),
                file_name=f"audit_log_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="Download Full Audit Log (JSON)",
                data=json.dumps(logs, indent=2, default=str),
                file_name=f"audit_log_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col3:
            if view_mode == "Table View" and table_data:
                csv = pd.DataFrame(table_data).to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.info("No audit logs available. Process some requests to generate logs.")

# Analytics Dashboard Page
elif page == "Analytics Dashboard":
    st.header("Analytics Dashboard")
    st.write("Comprehensive visual analytics and insights from system data.")
    
    if not ensure_agent_initialized():
        st.stop()
    
    # Data preparation
    logs = st.session_state.agent.get_audit_log()
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Patients", len(data_store.patients))
    with col2:
        total_slots = sum(len(slots) for slots in data_store.available_slots.values())
        st.metric("Available Slots", total_slots)
    with col3:
        st.metric("Booked Appointments", len(data_store.appointments))
    with col4:
        st.metric("Total Requests", len(logs))
    with col5:
        active_insurance = sum(1 for ins in data_store.insurance.values() if ins.get("eligibility_status") == "Active")
        st.metric("Active Insurance", active_insurance)
    
    st.divider()
    
    # Dashboard Tabs
    dashboard_tabs = st.tabs(["Overview", "Appointments", "Patients & Insurance", "System Activity", "Trends"])
    
    with dashboard_tabs[0]:  # Overview
        st.subheader("System Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Available Slots by Specialty**")
            specialty_data = {}
            for specialty, slots in data_store.available_slots.items():
                specialty_data[specialty] = len(slots)
            
            if specialty_data:
                df_specialty = pd.DataFrame(list(specialty_data.items()), columns=["Specialty", "Available Slots"])
                df_specialty = df_specialty.sort_values("Available Slots", ascending=False)
                fig = px.bar(df_specialty, x="Specialty", y="Available Slots", color="Specialty",
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(showlegend=False, height=400, xaxis_title="", yaxis_title="Available Slots")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Insurance Coverage Distribution**")
            coverage_types = {}
            for insurance in data_store.insurance.values():
                coverage = insurance.get("coverage_type", "Unknown")
                coverage_types[coverage] = coverage_types.get(coverage, 0) + 1
            
            if coverage_types:
                df_coverage = pd.DataFrame(list(coverage_types.items()), columns=["Coverage Type", "Count"])
                fig = px.pie(df_coverage, values="Count", names="Coverage Type",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Request Performance Gauge
        if logs:
            st.write("**Request Performance**")
            success_count = sum(1 for log in logs if log.get("data", {}).get("response", {}).get("success"))
            total_requests = sum(1 for log in logs if log.get("action_type") == "request_completed")
            
            if total_requests > 0:
                success_rate = (success_count / total_requests) * 100
                col1, col2 = st.columns([2, 1])
                with col1:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=success_rate,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Success Rate (%)"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#1f4788"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.metric("Successful", success_count)
                    st.metric("Total Requests", total_requests)
                    st.metric("Success Rate", f"{success_rate:.1f}%")
                    st.metric("Failed", total_requests - success_count)
    
    with dashboard_tabs[1]:  # Appointments
        st.subheader("Appointment Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Appointment Slots Timeline (Next 14 Days)**")
            today = datetime.now().date()
            timeline_data = []
            for i in range(14):
                date = today + timedelta(days=i)
                date_str = date.strftime("%Y-%m-%d")
                count = 0
                for slots in data_store.available_slots.values():
                    count += sum(1 for slot in slots if slot.get("date") == date_str)
                timeline_data.append({"Date": date_str, "Available Slots": count})
            
            if timeline_data:
                df_timeline = pd.DataFrame(timeline_data)
                fig = px.line(df_timeline, x="Date", y="Available Slots", markers=True,
                             color_discrete_sequence=["#1f4788"], line_shape='spline')
                fig.update_layout(height=400, xaxis_title="Date", yaxis_title="Available Slots")
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Slots by Doctor**")
            doctor_counts = {}
            for specialty, slots in data_store.available_slots.items():
                for slot in slots:
                    doctor = slot.get("doctor", "Unknown")
                    doctor_counts[doctor] = doctor_counts.get(doctor, 0) + 1
            
            if doctor_counts:
                df_doctors = pd.DataFrame(list(doctor_counts.items()), columns=["Doctor", "Slots"])
                df_doctors = df_doctors.sort_values("Slots", ascending=True).tail(10)  # Top 10
                fig = px.barh(df_doctors, x="Slots", y="Doctor", color="Slots",
                             color_continuous_scale="Blues")
                fig.update_layout(height=400, xaxis_title="Number of Slots", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)
        
        # Booked vs Available
        if data_store.appointments:
            st.write("**Appointments by Specialty**")
            apt_by_specialty = {}
            for apt in data_store.appointments.values():
                specialty = apt.get("specialty", "Unknown")
                apt_by_specialty[specialty] = apt_by_specialty.get(specialty, 0) + 1
            
            if apt_by_specialty:
                df_apt_spec = pd.DataFrame(list(apt_by_specialty.items()), columns=["Specialty", "Booked"])
                fig = px.bar(df_apt_spec, x="Specialty", y="Booked", color="Specialty",
                            color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(showlegend=False, height=350, xaxis_title="", yaxis_title="Booked Appointments")
                st.plotly_chart(fig, use_container_width=True)
    
    with dashboard_tabs[2]:  # Patients & Insurance
        st.subheader("Patients & Insurance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Insurance Providers Distribution**")
            provider_counts = {}
            for insurance in data_store.insurance.values():
                provider = insurance.get("insurance_provider", "Unknown")
                provider_counts[provider] = provider_counts.get(provider, 0) + 1
            
            if provider_counts:
                df_providers = pd.DataFrame(list(provider_counts.items()), columns=["Provider", "Patients"])
                fig = px.pie(df_providers, values="Patients", names="Provider",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Copay Amount Distribution**")
            copay_data = [ins.get("copay", 0) for ins in data_store.insurance.values()]
            if copay_data:
                df_copay = pd.DataFrame({"Copay Amount": copay_data})
                fig = px.histogram(df_copay, x="Copay Amount", nbins=20, color_discrete_sequence=["#1f4788"])
                fig.update_layout(height=400, xaxis_title="Copay Amount (₹)", yaxis_title="Number of Patients")
                st.plotly_chart(fig, use_container_width=True)
        
        # Age distribution (if we can calculate from DOB)
        st.write("**Patient Age Distribution**")
        ages = []
        for patient in data_store.patients.values():
            dob_str = patient.get("date_of_birth")
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                    age = (datetime.now().date() - dob).days // 365
                    ages.append(age)
                except:
                    pass
        
        if ages:
            df_ages = pd.DataFrame({"Age": ages})
            fig = px.histogram(df_ages, x="Age", nbins=15, color_discrete_sequence=["#28a745"])
            fig.update_layout(height=350, xaxis_title="Age (Years)", yaxis_title="Number of Patients")
            st.plotly_chart(fig, use_container_width=True)
    
    with dashboard_tabs[3]:  # System Activity
        st.subheader("System Activity Analytics")
        
        if logs:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Audit Log Activity Distribution**")
                action_counts = {}
                for log in logs:
                    action_type = log.get("action_type", "unknown")
                    action_counts[action_type] = action_counts.get(action_type, 0) + 1
                
                if action_counts:
                    df_actions = pd.DataFrame(list(action_counts.items()), columns=["Action Type", "Count"])
                    df_actions = df_actions.sort_values("Count", ascending=False)
                    fig = px.bar(df_actions, x="Action Type", y="Count", color="Count",
                                color_continuous_scale="Viridis")
                    fig.update_layout(height=400, xaxis_title="", yaxis_title="Count", showlegend=False)
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Request Activity Over Time**")
                # Group logs by date
                date_counts = {}
                for log in logs:
                    timestamp = log.get("timestamp", "")
                    if timestamp:
                        try:
                            date = timestamp.split("T")[0] if "T" in timestamp else timestamp.split(" ")[0]
                            date_counts[date] = date_counts.get(date, 0) + 1
                        except:
                            pass
                
                if date_counts:
                    df_dates = pd.DataFrame(list(date_counts.items()), columns=["Date", "Count"])
                    df_dates = df_dates.sort_values("Date")
                    fig = px.line(df_dates, x="Date", y="Count", markers=True,
                                 color_discrete_sequence=["#dc3545"])
                    fig.update_layout(height=400, xaxis_title="Date", yaxis_title="Number of Actions")
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Function call distribution
            st.write("**Function Call Distribution**")
            function_calls = {}
            for log in logs:
                if log.get("action_type") == "function_call":
                    func_name = log.get("data", {}).get("function", "unknown")
                    function_calls[func_name] = function_calls.get(func_name, 0) + 1
            
            if function_calls:
                df_funcs = pd.DataFrame(list(function_calls.items()), columns=["Function", "Calls"])
                df_funcs = df_funcs.sort_values("Calls", ascending=True)
                fig = px.barh(df_funcs, x="Calls", y="Function", color="Calls",
                             color_continuous_scale="Greens")
                fig.update_layout(height=300, xaxis_title="Number of Calls", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No audit log data available for system activity analysis")
    
    with dashboard_tabs[4]:  # Trends
        st.subheader("Trend Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Available Slots Trend (Next 30 Days)**")
            today = datetime.now().date()
            weekly_data = []
            for week in range(4):
                week_start = today + timedelta(days=week*7)
                week_end = week_start + timedelta(days=6)
                count = 0
                for slots in data_store.available_slots.values():
                    for slot in slots:
                        slot_date = datetime.strptime(slot.get("date"), "%Y-%m-%d").date()
                        if week_start <= slot_date <= week_end:
                            count += 1
                weekly_data.append({
                    "Week": f"Week {week+1}",
                    "Start Date": week_start.strftime("%Y-%m-%d"),
                    "Slots": count
                })
            
            if weekly_data:
                df_weekly = pd.DataFrame(weekly_data)
                fig = px.bar(df_weekly, x="Week", y="Slots", color="Slots",
                            color_continuous_scale="Blues", text="Slots")
                fig.update_traces(textposition='outside')
                fig.update_layout(height=400, xaxis_title="", yaxis_title="Available Slots", showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Insurance Coverage Types**")
            coverage_types = {}
            for insurance in data_store.insurance.values():
                coverage = insurance.get("coverage_type", "Unknown")
                coverage_types[coverage] = coverage_types.get(coverage, 0) + 1
            
            if coverage_types:
                df_coverage = pd.DataFrame(list(coverage_types.items()), columns=["Coverage Type", "Count"])
                fig = px.funnel(df_coverage, x="Count", y="Coverage Type",
                               color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(height=400, xaxis_title="Number of Patients", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)

# Function Schemas Page
elif page == "Function Schemas":
    st.header("Function Schemas")
    st.write("View the JSON schemas for all available functions.")
    
    if not FUNCTION_SCHEMAS:
        st.warning("No function schemas available")
        st.stop()
    
    for schema in FUNCTION_SCHEMAS:
        func_def = schema.get("function", {})
        func_name = func_def.get("name", "unknown")
        func_desc = func_def.get("description", "No description")
        func_params = func_def.get("parameters", {})
        
        with st.expander(f"{func_name.replace('_', ' ').title()}", expanded=False):
            st.write(f"**Description:** {func_desc}")
            
            if func_params.get("properties"):
                st.write("**Parameters:**")
                params_data = []
                required = func_params.get("required", [])
                for param_name, param_info in func_params["properties"].items():
                    params_data.append({
                        "Parameter": param_name,
                        "Type": param_info.get("type", "N/A"),
                        "Description": param_info.get("description", "N/A"),
                        "Required": "Yes" if param_name in required else "No"
                    })
                st.dataframe(pd.DataFrame(params_data), use_container_width=True, hide_index=True)
            
            st.write("**Full Schema (JSON):**")
            st.json(schema)

# Data Browser Page
elif page == "Data Browser":
    st.header("Data Browser")
    st.write("Browse and explore all data in the system.")
    
    data_tabs = st.tabs(["Patients", "Insurance Records", "Available Slots", "Appointments"])
    
    with data_tabs[0]:
        st.subheader("Patient Search & Browse")
        st.write(f"**Total Patients:** {len(data_store.patients)}")
        
        if data_store.patients:
            # Advanced Search Panel
            with st.expander("Advanced Search Filters", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    search_name = st.text_input("Search by Name", key="patient_search_name")
                    search_id = st.text_input("Search by Patient ID", key="patient_search_id")
                with col2:
                    search_mrn = st.text_input("Search by MRN", key="patient_search_mrn")
                    search_email = st.text_input("Search by Email", key="patient_search_email")
                with col3:
                    search_phone = st.text_input("Search by Phone", key="patient_search_phone")
            
            # Quick search (if advanced panel is closed)
            if "patient_search_name" not in st.session_state or not st.session_state.get("patient_search_name"):
                search_name = st.text_input("Quick Search", placeholder="Search by name, ID, email, or phone...", key="patient_quick_search")
                if search_name:
                    st.session_state.patient_search_name = search_name
            
            # Sort options
            col1, col2 = st.columns([3, 1])
            with col2:
                sort_by = st.selectbox("Sort By", ["Patient ID", "Name", "Date of Birth", "Email"], key="patient_sort")
                sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True, key="patient_sort_order")
            
            # Filter and search
            patients_list = []
            search_terms = {
                "name": st.session_state.get("patient_search_name", "").lower(),
                "id": st.session_state.get("patient_search_id", "").lower(),
                "mrn": st.session_state.get("patient_search_mrn", "").lower(),
                "email": st.session_state.get("patient_search_email", "").lower(),
                "phone": st.session_state.get("patient_search_phone", "").lower(),
                "quick": st.session_state.get("patient_quick_search", "").lower()
            }
            
            for patient_id, patient in data_store.patients.items():
                # Apply all search filters
                match = True
                
                if search_terms["quick"]:
                    # Quick search across multiple fields
                    search_text = search_terms["quick"]
                    patient_text = f"{patient.get('name', '')} {patient_id} {patient.get('email', '')} {patient.get('phone', '')}".lower()
                    if search_text not in patient_text:
                        match = False
                else:
                    # Individual field searches
                    if search_terms["name"] and search_terms["name"] not in patient.get("name", "").lower():
                        match = False
                    if search_terms["id"] and search_terms["id"] not in patient_id.lower():
                        match = False
                    if search_terms["mrn"] and search_terms["mrn"] not in patient.get("medical_record_number", "").lower():
                        match = False
                    if search_terms["email"] and search_terms["email"] not in patient.get("email", "").lower():
                        match = False
                    if search_terms["phone"] and search_terms["phone"] not in patient.get("phone", "").lower():
                        match = False
                
                if match:
                    patients_list.append({
                        "Patient ID": patient_id,
                        "Name": patient.get("name"),
                        "Date of Birth": patient.get("date_of_birth"),
                        "Medical Record #": patient.get("medical_record_number"),
                        "Phone": patient.get("phone"),
                        "Email": patient.get("email"),
                        "Address": patient.get("address", "")[:50] + "..." if len(patient.get("address", "")) > 50 else patient.get("address", "")
                    })
            
            if patients_list:
                df_patients = pd.DataFrame(patients_list)
                
                # Apply sorting
                ascending = sort_order == "Ascending"
                if sort_by == "Name":
                    df_patients = df_patients.sort_values("Name", ascending=ascending)
                elif sort_by == "Date of Birth":
                    df_patients = df_patients.sort_values("Date of Birth", ascending=ascending)
                elif sort_by == "Email":
                    df_patients = df_patients.sort_values("Email", ascending=ascending)
                else:
                    df_patients = df_patients.sort_values("Patient ID", ascending=ascending)
                
                st.write(f"**Found {len(patients_list)} patients**")
                st.dataframe(df_patients, use_container_width=True, hide_index=True)
                
                # Download
                csv = df_patients.to_csv(index=False)
                st.download_button("Download as CSV", data=csv, file_name=f"patients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
            else:
                st.info("No patients found matching the search criteria.")
    
    with data_tabs[1]:
        st.subheader("Insurance Records")
        st.write(f"**Total Insurance Records:** {len(data_store.insurance)}")
        
        if data_store.insurance:
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                filter_provider = st.selectbox("Filter by Provider", ["All"] + sorted(list(set(ins.get("insurance_provider") for ins in data_store.insurance.values()))), key="ins_provider")
            with col2:
                filter_status = st.selectbox("Filter by Status", ["All", "Active", "Inactive"], key="ins_status")
            
            insurance_list = []
            for patient_id, insurance in data_store.insurance.items():
                if filter_provider != "All" and insurance.get("insurance_provider") != filter_provider:
                    continue
                if filter_status != "All" and insurance.get("eligibility_status") != filter_status:
                    continue
                    
                patient_name = data_store.patients.get(patient_id, {}).get('name', 'Unknown')
                insurance_list.append({
                    "Patient ID": patient_id,
                    "Patient Name": patient_name,
                    "Provider": insurance.get("insurance_provider"),
                    "Policy Number": insurance.get("policy_number"),
                    "Coverage Type": insurance.get("coverage_type"),
                    "Status": insurance.get("eligibility_status"),
                    "Copay": insurance.get("copay"),
                    "Valid Until": insurance.get("valid_until")
                })
            
            if insurance_list:
                df_insurance = pd.DataFrame(insurance_list)
                st.dataframe(df_insurance, use_container_width=True, hide_index=True)
                csv = df_insurance.to_csv(index=False)
                st.download_button("Download as CSV", data=csv, file_name=f"insurance_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    
    with data_tabs[2]:
        st.subheader("Available Appointment Slots")
        
        specialty_filter = st.selectbox("Filter by Specialty", ["All"] + list(data_store.available_slots.keys()), key="slot_filter")
        date_filter = st.date_input("Filter by Date (Optional)", value=None, key="slot_date")
        
        all_slots = []
        for specialty, slots in data_store.available_slots.items():
            if specialty_filter != "All" and specialty != specialty_filter:
                continue
            for slot in slots:
                if date_filter and slot.get("date") != date_filter.strftime("%Y-%m-%d"):
                    continue
                all_slots.append({
                    "Specialty": specialty,
                    "Slot ID": slot.get("slot_id"),
                    "Date": slot.get("date"),
                    "Time": slot.get("time"),
                    "Doctor": slot.get("doctor"),
                    "Duration (min)": slot.get("duration_minutes")
                })
        
        st.write(f"**Total Available Slots:** {len(all_slots)}")
        
        if all_slots:
            df_slots = pd.DataFrame(all_slots)
            st.dataframe(df_slots, use_container_width=True, hide_index=True)
            csv = df_slots.to_csv(index=False)
            st.download_button("Download as CSV", data=csv, file_name=f"slots_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    
    with data_tabs[3]:
        st.subheader("Booked Appointments")
        st.write(f"**Total Booked Appointments:** {len(data_store.appointments)}")
        
        if data_store.appointments:
            appointments_list = []
            for apt_id, apt in data_store.appointments.items():
                appointments_list.append({
                    "Appointment ID": apt_id,
                    "Patient ID": apt.get("patient_id"),
                    "Patient Name": apt.get("patient_name"),
                    "Specialty": apt.get("specialty"),
                    "Date": apt.get("date"),
                    "Time": apt.get("time"),
                    "Doctor": apt.get("doctor"),
                    "Duration (min)": apt.get("duration_minutes"),
                    "Status": apt.get("status"),
                    "Reason": apt.get("reason")
                })
            
            df_appointments = pd.DataFrame(appointments_list)
            st.dataframe(df_appointments, use_container_width=True, hide_index=True)
            csv = df_appointments.to_csv(index=False)
            st.download_button("Download as CSV", data=csv, file_name=f"appointments_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
        else:
            st.info("No appointments booked yet.")

# System Information Page
else:
    st.header("System Information & Documentation")
    
    # Create tabs for different sections
    info_tabs = st.tabs(["About", "Features", "Technology", "Data", "Safety & Compliance", "Quick Start"])
    
    with info_tabs[0]:  # About
        st.subheader("About Clinical Workflow Automation Agent")
        st.markdown("""
        The **Clinical Workflow Automation Agent** is an intelligent function-calling LLM agent designed to help 
        healthcare professionals manage patient workflows safely and efficiently. It acts as a workflow orchestrator,
        interpreting natural language requests and executing validated actions through structured function calls.
        
        ### Purpose
        
        This system addresses the challenge of managing complex healthcare workflows by providing:
        - **Automated Workflow Coordination**: Interprets natural language and executes appropriate actions
        - **Safety-First Design**: Built-in validation and refusal mechanisms prevent unsafe operations
        - **Compliance Ready**: Comprehensive audit logging for regulatory requirements
        - **User-Friendly Interface**: Intuitive natural language processing with visual analytics
        
        ### What This Agent Does
        
        - Searches for patients by name
        - Checks insurance eligibility and coverage
        - Finds available appointment slots across specialties
        - Books appointments with validation
        - Tracks all actions in audit logs
        
        ### What This Agent Does NOT Do
        
        - Does NOT provide medical diagnosis or advice
        - Does NOT prescribe treatments
        - Does NOT interpret clinical data
        - Does NOT perform destructive or unsafe actions
        
        The agent acts as a **workflow orchestrator**, not a medical advisor.
        """)
    
    with info_tabs[1]:  # Features
        st.subheader("Key Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Core Capabilities**")
            st.markdown("""
            - **Natural Language Processing**: Process requests in plain English
            - **Function Calling**: Automatic function selection and execution
            - **Patient Search**: FHIR-compatible patient lookup
            - **Insurance Verification**: Real-time eligibility checking
            - **Appointment Management**: Find and book appointments
            - **Audit Logging**: Complete action tracking
            """)
            
            st.write("**User Interface Features**")
            st.markdown("""
            - Natural language request processing
            - Quick action buttons for direct function access
            - Comprehensive analytics dashboard with visualizations
            - Advanced data browser with filtering
            - Detailed audit log viewer with search
            - Export capabilities (CSV/JSON)
            """)
        
        with col2:
            st.write("**Advanced Features**")
            st.markdown("""
            - **Dry-Run Mode**: Test workflows without making changes
            - **Auto-Initialization**: Automatic agent setup
            - **Request History**: Track previous requests
            - **Multiple View Modes**: Table, detailed, and timeline views
            - **Advanced Filtering**: Filter by type, date, time range
            - **Visual Analytics**: Charts and graphs for insights
            """)
            
            st.write("**Safety Features**")
            st.markdown("""
            - Request validation before execution
            - Refusal mechanism for unsafe requests
            - Input schema validation
            - Comprehensive error handling
            - Audit trail for all actions
            """)
    
    with info_tabs[2]:  # Technology
        st.subheader("Technology Stack")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Backend Technologies**")
            st.markdown("""
            - **Python 3.x**: Core programming language
            - **LangChain**: LLM framework for function calling
            - **HuggingFace**: LLM inference API
            - **Pydantic**: Data validation
            - **Requests**: HTTP client library
            """)
            
            st.write("**Data Storage**")
            st.markdown("""
            - In-memory data store (sample data)
            - FHIR-compatible data structures
            - Dictionary-based storage
            - JSON serialization support
            """)
        
        with col2:
            st.write("**Frontend Technologies**")
            st.markdown("""
            - **Streamlit**: Web application framework
            - **Plotly**: Interactive visualizations
            - **Pandas**: Data manipulation and analysis
            - **HTML/CSS**: Custom styling
            """)
            
            st.write("**API Integration**")
            st.markdown("""
            - HuggingFace Inference API
            - RESTful API design
            - JSON-based communication
            - Error handling and retries
            """)
        
        st.write("**Architecture**")
        st.markdown("""
        The system follows a modular architecture:
        
        1. **Agent Layer**: Core LLM agent with function calling capabilities
        2. **Function Layer**: Healthcare-specific function implementations
        3. **Data Layer**: In-memory data store with sample data
        4. **UI Layer**: Streamlit-based web interface
        5. **Analytics Layer**: Visualization and reporting tools
        """)
    
    with info_tabs[3]:  # Data
        st.subheader("Sample Data & System Information")
        
        st.write("**Data Summary**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Patients", len(data_store.patients))
        with col2:
            st.metric("Insurance Records", len(data_store.insurance))
        with col3:
            total_slots = sum(len(slots) for slots in data_store.available_slots.values())
            st.metric("Available Slots", total_slots)
        with col4:
            st.metric("Booked Appointments", len(data_store.appointments))
        
        st.divider()
        
        st.write("**Specialties Available**")
        specialty_cols = st.columns(3)
        for i, (specialty, slots) in enumerate(data_store.available_slots.items()):
            with specialty_cols[i % 3]:
                st.metric(specialty, f"{len(slots)} slots")
        
        st.divider()
        
        st.write("**Sample Patients**")
        sample_patients = list(data_store.patients.values())[:10]
        patient_data = [{"Name": p.get("name"), "ID": p.get("patient_id"), "DOB": p.get("date_of_birth")} 
                       for p in sample_patients]
        st.dataframe(pd.DataFrame(patient_data), use_container_width=True, hide_index=True)
        
        st.divider()
        
        st.write("**Insurance Providers**")
        providers = list(set(ins.get("insurance_provider") for ins in data_store.insurance.values()))
        st.write(", ".join(providers))
    
    with info_tabs[4]:  # Safety & Compliance
        st.subheader("Safety & Compliance")
        
        st.write("**Safety Mechanisms**")
        st.markdown("""
        1. **Request Validation**: All requests are validated before processing
        2. **Medical Advice Refusal**: System refuses to provide medical diagnosis or advice
        3. **Unsafe Action Prevention**: Destructive actions are blocked
        4. **Input Validation**: All inputs are validated against schemas
        5. **Error Handling**: Comprehensive error handling and reporting
        """)
        
        st.write("**Compliance Features**")
        st.markdown("""
        1. **Audit Logging**: Every action is logged with timestamp and details
        2. **Request Tracking**: Complete history of all requests and responses
        3. **Export Capabilities**: Download logs for compliance reporting
        4. **Data Privacy**: No patient data is stored permanently (in-memory only)
        5. **Traceability**: Full audit trail for all system actions
        """)
        
        st.write("**Validation Rules**")
        st.markdown("""
        - Patient search requires valid name input
        - Insurance checks require valid patient ID
        - Appointment booking validates patient, slot, and specialty
        - All function calls validate inputs against JSON schemas
        - Responses are structured and validated before return
        """)
    
    with info_tabs[5]:  # Quick Start
        st.subheader("Quick Start Guide")
        
        st.write("**Getting Started**")
        st.markdown("""
        1. **Initialize the Agent**: Click "Initialize" in the sidebar or enable auto-initialization
        2. **Enter Your Request**: Use natural language to describe what you want to do
        3. **Review Results**: Check the structured response and detailed results
        4. **Explore Features**: Use the navigation menu to explore all features
        """)
        
        st.write("**Example Requests**")
        st.code("""
        Find patient Ravi Kumar
        Check insurance eligibility for patient Ravi Kumar
        Find available cardiology appointments next week
        Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility
        """, language="text")
        
        st.write("**Using Quick Actions**")
        st.markdown("""
        - Navigate to "Quick Actions" for direct function access
        - Select the appropriate tab (Search Patient, Check Insurance, etc.)
        - Fill in the required fields
        - Click the action button
        """)
        
        st.write("**Viewing Analytics**")
        st.markdown("""
        - Go to "Analytics Dashboard" for visual insights
        - Explore different tabs: Overview, Appointments, Patients & Insurance, System Activity, Trends
        - Review charts and metrics for system performance
        """)
        
        st.write("**Audit Logs**")
        st.markdown("""
        - Navigate to "Audit Logs" for compliance tracking
        - Use filters to find specific entries
        - Choose view mode: Table, Detailed, or Timeline
        - Export logs as JSON or CSV
        """)
        
        st.write("**Tips**")
        st.markdown("""
        - Use Dry-Run mode to test workflows without making changes
        - Check request history to review previous interactions
        - Use the data browser to explore available data
        - Export data for record keeping and analysis
        - Review function schemas to understand available functions
        """)
