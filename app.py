"""Main Streamlit Application - Hospital Information System."""

import streamlit as st
import sys
from pathlib import Path
from config.settings import AppSettings
from config.database import get_db_context

# Set page configuration
st.set_page_config(
    page_title=AppSettings.APP_NAME,
    page_icon="🏥",
    layout=AppSettings.STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded"
)

# Apply custom theme
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "hospital_id" not in st.session_state:
        st.session_state.hospital_id = None
    if "token" not in st.session_state:
        st.session_state.token = None
    if "page" not in st.session_state:
        st.session_state.page = "login"

def login_page():
    """Display login page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""<h1 style='text-align: center; color: #1f77b4;'>🏥 Hospital Information System</h1>""", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    # Authenticate user
                    from modules.users.controller import UserController
                    
                    with get_db_context() as db:
                        user_controller = UserController(db)
                        result = user_controller.authenticate_user(username, password)
                        
                        if result["success"]:
                            st.session_state.user_id = result["user_id"]
                            st.session_state.username = result["username"]
                            st.session_state.role = result["role"]
                            st.session_state.hospital_id = result["hospital_id"]
                            st.session_state.token = result["token"]
                            st.session_state.page = "dashboard"
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(result["error"])

def dashboard_page():
    """Display dashboard page."""
    st.sidebar.header(f"Welcome, {st.session_state.username}!")
    st.sidebar.info(f"Role: {st.session_state.role.upper()}")
    
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()
    
    st.markdown(f"""<h1 style='text-align: center; color: #1f77b4;'>Hospital Information System</h1>""", unsafe_allow_html=True)
    
    # Dashboard content based on role
    if st.session_state.role == "super_admin":
        show_super_admin_dashboard()
    elif st.session_state.role == "admin":
        show_admin_dashboard()
    else:
        show_user_dashboard()

def show_super_admin_dashboard():
    """Show Super Admin Dashboard."""
    st.markdown("---")
    st.subheader("Super Admin Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Hospitals", "5", "↑ 2")
    with col2:
        st.metric("Active Users", "45", "↑ 8")
    with col3:
        st.metric("Total Revenue", "₹2.5L", "↑ 15%")
    
    st.markdown("---")
    
    # Menu options
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Hospitals", "Users", "Reports", "Settings"]
    )
    
    if menu == "Hospitals":
        st.info("Hospital Management - Coming Soon")
    elif menu == "Users":
        st.info("User Management - Coming Soon")
    elif menu == "Reports":
        st.info("Reports Module - Coming Soon")
    elif menu == "Settings":
        st.info("System Settings - Coming Soon")

def show_admin_dashboard():
    """Show Admin Dashboard."""
    st.markdown("---")
    st.subheader("Hospital Admin Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", "1,250", "↑ 45")
    with col2:
        st.metric("Active Admissions", "85", "↑ 12")
    with col3:
        st.metric("Today's Appointments", "120", "↑ 8")
    with col4:
        st.metric("Pending Billings", "₹5.2L", "↑ 2.3L")
    
    st.markdown("---")
    
    # Menu options
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "IPD", "OPD", "Billing", "Master Data", "Reports", "Settings"]
    )
    
    if menu == "IPD":
        st.info("IPD Module - Coming Soon")
    elif menu == "OPD":
        st.info("OPD Module - Coming Soon")
    elif menu == "Billing":
        st.info("Billing Module - Coming Soon")
    elif menu == "Master Data":
        st.info("Master Data Management - Coming Soon")
    elif menu == "Reports":
        st.info("Reports Module - Coming Soon")
    elif menu == "Settings":
        st.info("Hospital Settings - Coming Soon")

def show_user_dashboard():
    """Show User Dashboard."""
    st.markdown("---")
    st.subheader("Dashboard")
    
    # Menu options based on role
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Patients", "Appointments", "Consultations", "My Profile"]
    )
    
    if menu == "Patients":
        st.info("Patient Management - Coming Soon")
    elif menu == "Appointments":
        st.info("Appointments - Coming Soon")
    elif menu == "Consultations":
        st.info("Consultations - Coming Soon")
    elif menu == "My Profile":
        st.info("Profile Management - Coming Soon")

def main():
    """Main application entry point."""
    initialize_session_state()
    
    if st.session_state.page == "login" or not st.session_state.user_id:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
