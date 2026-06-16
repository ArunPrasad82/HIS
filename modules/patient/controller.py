"""Patient management controllers."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.patient import Patient, PatientMedicalHistory, PatientAllergy, PatientStatus
from utils.generators import generate_uhid
from datetime import datetime, date


class PatientController:
    """Patient management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_patient(self, hospital_id: int, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new patient.
        
        Args:
            hospital_id: Hospital ID
            patient_data: Patient data dictionary
            
        Returns:
            Created patient data
        """
        try:
            # Check if patient already exists (by phone or aadhar)
            existing = self.db.query(Patient).filter(
                (Patient.mobile_primary == patient_data["mobile_primary"]) &
                (Patient.hospital_id == hospital_id)
            ).first()
            
            if existing:
                return {"success": False, "error": "Patient with this phone number already exists"}
            
            # Generate UHID
            uhid = generate_uhid("HOS001")  # Hospital code should be dynamic
            
            patient = Patient(
                hospital_id=hospital_id,
                uhid=uhid,
                first_name=patient_data["first_name"],
                middle_name=patient_data.get("middle_name"),
                last_name=patient_data.get("last_name"),
                date_of_birth=patient_data["date_of_birth"],
                gender=patient_data["gender"],
                blood_group=patient_data.get("blood_group"),
                aadhar_number=patient_data.get("aadhar_number"),
                mobile_primary=patient_data["mobile_primary"],
                mobile_secondary=patient_data.get("mobile_secondary"),
                email=patient_data.get("email"),
                address=patient_data["address"],
                city=patient_data["city"],
                state=patient_data["state"],
                postal_code=patient_data.get("postal_code"),
                country=patient_data.get("country", "India"),
                occupation=patient_data.get("occupation"),
                education=patient_data.get("education"),
                marital_status=patient_data.get("marital_status"),
                emergency_contact_name=patient_data.get("emergency_contact_name"),
                emergency_contact_phone=patient_data.get("emergency_contact_phone"),
                emergency_contact_relation=patient_data.get("emergency_contact_relation"),
                status=PatientStatus.ACTIVE,
                notes=patient_data.get("notes")
            )
            
            self.db.add(patient)
            self.db.commit()
            self.db.refresh(patient)
            
            return {
                "success": True,
                "message": "Patient created successfully",
                "patient_id": patient.id,
                "uhid": patient.uhid
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def get_patient(self, hospital_id: int, patient_id: int) -> Optional[Dict[str, Any]]:
        """Get patient by ID.
        
        Args:
            hospital_id: Hospital ID
            patient_id: Patient ID
            
        Returns:
            Patient data or None
        """
        try:
            patient = self.db.query(Patient).filter(
                Patient.id == patient_id,
                Patient.hospital_id == hospital_id
            ).first()
            
            if patient:
                return {
                    "id": patient.id,
                    "uhid": patient.uhid,
                    "abha_id": patient.abha_id,
                    "first_name": patient.first_name,
                    "middle_name": patient.middle_name,
                    "last_name": patient.last_name,
                    "full_name": patient.get_full_name(),
                    "date_of_birth": patient.date_of_birth,
                    "gender": patient.gender,
                    "blood_group": patient.blood_group,
                    "aadhar_number": patient.aadhar_number,
                    "mobile_primary": patient.mobile_primary,
                    "mobile_secondary": patient.mobile_secondary,
                    "email": patient.email,
                    "address": patient.address,
                    "city": patient.city,
                    "state": patient.state,
                    "postal_code": patient.postal_code,
                    "country": patient.country,
                    "occupation": patient.occupation,
                    "education": patient.education,
                    "marital_status": patient.marital_status,
                    "emergency_contact_name": patient.emergency_contact_name,
                    "emergency_contact_phone": patient.emergency_contact_phone,
                    "emergency_contact_relation": patient.emergency_contact_relation,
                    "status": patient.status.value,
                    "registration_date": patient.registration_date
                }
            return None
        except Exception:
            return None

    def search_patient(self, hospital_id: int, search_query: str) -> Dict[str, Any]:
        """Search for patients.
        
        Args:
            hospital_id: Hospital ID
            search_query: Search query (UHID, phone, name)
            
        Returns:
            Search results
        """
        try:
            query = self.db.query(Patient).filter(Patient.hospital_id == hospital_id)
            
            # Search by UHID, phone, or name
            from sqlalchemy import or_
            query = query.filter(
                or_(
                    Patient.uhid.ilike(f"%{search_query}%"),
                    Patient.mobile_primary.ilike(f"%{search_query}%"),
                    Patient.first_name.ilike(f"%{search_query}%"),
                    Patient.last_name.ilike(f"%{search_query}%")
                )
            )
            
            patients = query.limit(20).all()
            
            return {
                "success": True,
                "results": [
                    {
                        "id": p.id,
                        "uhid": p.uhid,
                        "full_name": p.get_full_name(),
                        "mobile": p.mobile_primary,
                        "date_of_birth": p.date_of_birth
                    }
                    for p in patients
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_patient(self, hospital_id: int, patient_id: int, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update patient.
        
        Args:
            hospital_id: Hospital ID
            patient_id: Patient ID
            patient_data: Updated patient data
            
        Returns:
            Update result
        """
        try:
            patient = self.db.query(Patient).filter(
                Patient.id == patient_id,
                Patient.hospital_id == hospital_id
            ).first()
            
            if not patient:
                return {"success": False, "error": "Patient not found"}
            
            # Update fields
            for key, value in patient_data.items():
                if hasattr(patient, key) and value is not None:
                    setattr(patient, key, value)
            
            self.db.commit()
            
            return {"success": True, "message": "Patient updated successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_patients(self, hospital_id: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List patients.
        
        Args:
            hospital_id: Hospital ID
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of patients
        """
        try:
            query = self.db.query(Patient).filter(
                Patient.hospital_id == hospital_id,
                Patient.is_active == True
            )
            total = query.count()
            patients = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "patients": [
                    {
                        "id": p.id,
                        "uhid": p.uhid,
                        "full_name": p.get_full_name(),
                        "mobile": p.mobile_primary,
                        "city": p.city,
                        "status": p.status.value
                    }
                    for p in patients
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_medical_history(self, patient_id: int, history_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add medical history to patient.
        
        Args:
            patient_id: Patient ID
            history_data: Medical history data
            
        Returns:
            Result
        """
        try:
            history = PatientMedicalHistory(
                patient_id=patient_id,
                condition_name=history_data["condition_name"],
                icd_code=history_data.get("icd_code"),
                diagnosis_date=history_data.get("diagnosis_date"),
                status=history_data.get("status"),
                notes=history_data.get("notes")
            )
            
            self.db.add(history)
            self.db.commit()
            
            return {"success": True, "message": "Medical history added successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def add_allergy(self, patient_id: int, allergy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add allergy to patient.
        
        Args:
            patient_id: Patient ID
            allergy_data: Allergy data
            
        Returns:
            Result
        """
        try:
            allergy = PatientAllergy(
                patient_id=patient_id,
                allergen=allergy_data["allergen"],
                reaction=allergy_data["reaction"],
                severity=allergy_data.get("severity"),
                notes=allergy_data.get("notes")
            )
            
            self.db.add(allergy)
            self.db.commit()
            
            return {"success": True, "message": "Allergy added successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}
