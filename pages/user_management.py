"""User authentication and management pages."""

import streamlit as st
from config.database import get_db_context
from modules.users.controller import UserController
from utils.validators import validate_email, validate_phone, validate_password
from datetime import datetime


def show_user_management():
    """Display user management page."""
    st.header("👥 User Management")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["List Users", "Create User", "Edit User"])
    
    with tab1:
        show_user_list()
    
    with tab2:
        show_create_user()
    
    with tab3:
        show_edit_user()


def show_user_list():
    """Display list of users."""
    st.subheader("Users List")
    
    hospital_id = st.session_state.get("hospital_id")
    
    with get_db_context() as db:
        user_controller = UserController(db)
        result = user_controller.list_users(hospital_id=hospital_id, limit=100)
        
        if result["success"]:
            if result["users"]:
                # Create dataframe for display
                import pandas as pd
                users_data = []
                for user in result["users"]:
                    users_data.append({
                        "ID": user["id"],
                        "Username": user["username"],
                        "Email": user["email"],
                        "Name": f"{user['first_name']} {user['last_name']}",
                        "Role": user["role"],
                        "Verified": "✓" if user["is_verified"] else "✗"
                    })
                
                df = pd.DataFrame(users_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No users found.")
        else:
            st.error(f"Error: {result['error']}")


def show_create_user():
    """Display create user form."""
    st.subheader("Create New User")
    
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="John")
            last_name = st.text_input("Last Name *", placeholder="Doe")
            username = st.text_input("Username *", placeholder="johndoe")
        
        with col2:
            email = st.text_input("Email *", placeholder="john@example.com")
            phone = st.text_input("Phone", placeholder="9876543210")
            role = st.selectbox("Role *", [
                "super_admin", "admin", "consultant", "doctor", 
                "nurse", "receptionist", "billing_staff", "accountant"
            ])
        
        col3, col4 = st.columns(2)
        with col3:
            password = st.text_input("Password *", type="password", placeholder="Enter password")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm password")
        
        submit = st.form_submit_button("Create User", use_container_width=True)
        
        if submit:
            # Validation
            errors = []
            
            if not first_name or not last_name or not username or not email or not password:
                errors.append("Please fill all required fields")
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            is_valid, error_msg = validate_email(email)
            if not is_valid:
                errors.append(f"Email: {error_msg}")
            
            if phone:
                is_valid, error_msg = validate_phone(phone)
                if not is_valid:
                    errors.append(f"Phone: {error_msg}")
            
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                errors.append(f"Password: {error_msg}")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create user
                with get_db_context() as db:
                    user_controller = UserController(db)
                    result = user_controller.create_user({
                        "first_name": first_name,
                        "last_name": last_name,
                        "username": username,
                        "email": email,
                        "phone": phone,
                        "role": role,
                        "password": password,
                        "hospital_id": st.session_state.get("hospital_id")
                    })
                    
                    if result["success"]:
                        st.success(f"✅ {result['message']} (User ID: {result['user_id']})")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {result['error']}")


def show_edit_user():
    """Display edit user page."""
    st.subheader("Edit User")
    
    hospital_id = st.session_state.get("hospital_id")
    
    # Get list of users
    with get_db_context() as db:
        user_controller = UserController(db)
        result = user_controller.list_users(hospital_id=hospital_id, limit=1000)
        
        if result["users"]:
            user_options = {f"{u['username']} ({u['email']})": u["id"] for u in result["users"]}
            selected_user_display = st.selectbox("Select User", list(user_options.keys()))
            selected_user_id = user_options[selected_user_display]
            
            # Get user details
            user_data = user_controller.get_user(selected_user_id)
            
            if user_data:
                with st.form("edit_user_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        first_name = st.text_input("First Name", value=user_data["first_name"])
                        last_name = st.text_input("Last Name", value=user_data["last_name"])
                        email = st.text_input("Email", value=user_data["email"])
                    
                    with col2:
                        phone = st.text_input("Phone", value=user_data["phone"] or "")
                        role = st.selectbox(
                            "Role",
                            ["super_admin", "admin", "consultant", "doctor", "nurse", "receptionist", "billing_staff", "accountant"],
                            index=["super_admin", "admin", "consultant", "doctor", "nurse", "receptionist", "billing_staff", "accountant"].index(user_data["role"])
                        )
                    
                    submit = st.form_submit_button("Update User", use_container_width=True)
                    
                    if submit:
                        result = user_controller.update_user(selected_user_id, {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "phone": phone,
                            "role": role
                        })
                        
                        if result["success"]:
                            st.success(f"✅ {result['message']}")
                        else:
                            st.error(f"❌ Error: {result['error']}")
        else:
            st.info("No users found in your hospital.")


def show_change_password():
    """Display change password page."""
    st.header("🔐 Change Password")
    st.markdown("---")
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit = st.form_submit_button("Change Password", use_container_width=True)
        
        if submit:
            if new_password != confirm_password:
                st.error("New passwords do not match")
            else:
                with get_db_context() as db:
                    user_controller = UserController(db)
                    result = user_controller.change_password(
                        st.session_state.user_id,
                        current_password,
                        new_password
                    )
                    
                    if result["success"]:
                        st.success("✅ Password changed successfully")
                    else:
                        st.error(f"❌ Error: {result['error']}")
