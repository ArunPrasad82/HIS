"""Patient management pages."""

import streamlit as st
from datetime import datetime, date
from config.database import get_db_context
from modules.patient.controller import PatientController
from utils.validators import validate_email, validate_phone, validate_aadhar
from utils.helpers import format_date, get_age_from_dob
import pandas as pd


def show_patient_management():
    """Display patient management page."""
    st.header("👨‍⚕️ Patient Management")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["List Patients", "Register Patient", "Search Patient", "Patient Details"])
    
    with tab1:
        show_patient_list()
    
    with tab2:
        show_register_patient()
    
    with tab3:
        show_search_patient()
    
    with tab4:
        show_patient_details()


def show_patient_list():
    """Display list of patients."""
    st.subheader("Registered Patients")
    
    hospital_id = st.session_state.get("hospital_id")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        limit = st.selectbox("Records per page", [10, 25, 50, 100])
    
    with get_db_context() as db:
        patient_controller = PatientController(db)
        result = patient_controller.list_patients(hospital_id=hospital_id, limit=limit)
        
        if result["success"]:
            if result["patients"]:
                patients_data = []
                for patient in result["patients"]:
                    patients_data.append({
                        "ID": patient["id"],
                        "UHID": patient["uhid"],
                        "Name": patient["full_name"],
                        "Phone": patient["mobile"],
                        "City": patient["city"],
                        "Status": patient["status"]
                    })
                
                df = pd.DataFrame(patients_data)
                st.dataframe(df, use_container_width=True)
                st.success(f"Total Patients: {result['total']}")
            else:
                st.info("No patients found.")
        else:
            st.error(f"Error: {result['error']}")


def show_register_patient():
    """Display patient registration form."""
    st.subheader("Register New Patient")
    
    hospital_id = st.session_state.get("hospital_id")
    
    with st.form("register_patient_form"):
        # Personal Information
        st.markdown("### Personal Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            first_name = st.text_input("First Name *", placeholder="John")
        with col2:
            middle_name = st.text_input("Middle Name", placeholder="Kumar")
        with col3:
            last_name = st.text_input("Last Name *", placeholder="Doe")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dob = st.date_input("Date of Birth *", value=date(2000, 1, 1))
        with col2:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        with col3:
            blood_group = st.selectbox("Blood Group", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "Unknown"])
        
        # Contact Information
        st.markdown("### Contact Information")
        col1, col2 = st.columns(2)
        with col1:
            mobile_primary = st.text_input("Primary Mobile *", placeholder="9876543210")
        with col2:
            mobile_secondary = st.text_input("Secondary Mobile", placeholder="9876543211")
        
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email", placeholder="patient@example.com")
        with col2:
            aadhar = st.text_input("Aadhar Number", placeholder="123456789012")
        
        # Address Information
        st.markdown("### Address Information")
        address = st.text_area("Address *", placeholder="Enter full address", height=80)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            city = st.text_input("City *", placeholder="New Delhi")
        with col2:
            state = st.text_input("State *", placeholder="Delhi")
        with col3:
            postal_code = st.text_input("Postal Code", placeholder="110001")
        
        # Additional Information
        st.markdown("### Additional Information")
        col1, col2 = st.columns(2)
        with col1:
            occupation = st.text_input("Occupation", placeholder="Engineer")
        with col2:
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed", "Not Specified"])
        
        # Emergency Contact
        st.markdown("### Emergency Contact")
        col1, col2 = st.columns(2)
        with col1:
            emergency_name = st.text_input("Emergency Contact Name", placeholder="Jane Doe")
        with col2:
            emergency_phone = st.text_input("Emergency Contact Phone", placeholder="9876543210")
        
        col1, col2 = st.columns(2)
        with col1:
            emergency_relation = st.selectbox("Relationship", ["Spouse", "Parent", "Child", "Sibling", "Other"])
        with col2:
            pass
        
        submit = st.form_submit_button("Register Patient", use_container_width=True)
        
        if submit:
            # Validation
            errors = []
            
            if not first_name or not last_name or not mobile_primary or not address or not city or not state:
                errors.append("Please fill all required fields")
            
            is_valid, error_msg = validate_phone(mobile_primary)
            if not is_valid:
                errors.append(f"Mobile: {error_msg}")
            
            if email:
                is_valid, error_msg = validate_email(email)
                if not is_valid:
                    errors.append(f"Email: {error_msg}")
            
            if aadhar:
                is_valid, error_msg = validate_aadhar(aadhar)
                if not is_valid:
                    errors.append(f"Aadhar: {error_msg}")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Register patient
                with get_db_context() as db:
                    patient_controller = PatientController(db)
                    result = patient_controller.create_patient(hospital_id, {
                        "first_name": first_name,
                        "middle_name": middle_name,
                        "last_name": last_name,
                        "date_of_birth": dob,
                        "gender": gender.lower(),
                        "blood_group": blood_group,
                        "mobile_primary": mobile_primary,
                        "mobile_secondary": mobile_secondary,
                        "email": email,
                        "aadhar_number": aadhar,
                        "address": address,
                        "city": city,
                        "state": state,
                        "postal_code": postal_code,
                        "occupation": occupation,
                        "marital_status": marital_status.lower(),
                        "emergency_contact_name": emergency_name,
                        "emergency_contact_phone": emergency_phone,
                        "emergency_contact_relation": emergency_relation.lower()
                    })
                    
                    if result["success"]:
                        st.success(f"✅ Patient registered successfully!")
                        st.info(f"UHID: **{result['uhid']}**")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {result['error']}")


def show_search_patient():
    """Display patient search page."""
    st.subheader("Search Patient")
    
    hospital_id = st.session_state.get("hospital_id")
    search_query = st.text_input(
        "Search by UHID, Phone, or Name",
        placeholder="Enter UHID, phone number, or patient name"
    )
    
    if search_query:
        with get_db_context() as db:
            patient_controller = PatientController(db)
            result = patient_controller.search_patient(hospital_id, search_query)
            
            if result["success"]:
                if result["results"]:
                    for patient in result["results"]:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.markdown(f"**{patient['full_name']}**")
                                st.text(f"UHID: {patient['uhid']}")
                            with col2:
                                st.text(f"Phone: {patient['mobile']}")
                                st.text(f"DOB: {patient['date_of_birth']}")
                            with col3:
                                if st.button("View Details", key=patient["id"]):
                                    st.session_state.selected_patient_id = patient["id"]
                            st.markdown("---")
                else:
                    st.info("No patients found matching your search.")
            else:
                st.error(f"Error: {result['error']}")


def show_patient_details():
    """Display patient details page."""
    st.subheader("Patient Details")
    
    hospital_id = st.session_state.get("hospital_id")
    patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)
    
    if patient_id:
        with get_db_context() as db:
            patient_controller = PatientController(db)
            patient = patient_controller.get_patient(hospital_id, patient_id)
            
            if patient:
                # Display tabs
                tab1, tab2, tab3, tab4 = st.tabs(["Basic Info", "Medical History", "Allergies", "Edit"])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("UHID", patient["uhid"])
                        st.metric("Full Name", patient["full_name"])
                        st.metric("Gender", patient["gender"])
                    with col2:
                        age = get_age_from_dob(patient["date_of_birth"])
                        st.metric("Age", f"{age} years")
                        st.metric("Blood Group", patient["blood_group"] or "Not specified")
                        st.metric("Phone", patient["mobile_primary"])
                    
                    st.markdown("---")
                    st.subheader("Address")
                    st.text(patient["address"])
                    st.text(f"{patient['city']}, {patient['state']} {patient['postal_code']}")
                
                with tab2:
                    st.info("Medical History - Coming Soon")
                
                with tab3:
                    st.info("Patient Allergies - Coming Soon")
                
                with tab4:
                    st.info("Edit Patient - Coming Soon")
            else:
                st.error("Patient not found.")
