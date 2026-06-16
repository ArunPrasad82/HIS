"""IPD (Inpatient Department) controllers."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.ipd import Admission, Treatment, Prescription, PrescriptionItem, PatientVital, AdmissionNote, Surgery, AdmissionStatus, DischargeReason
from utils.generators import generate_admission_number, generate_prescription_number
from datetime import datetime, date


class AdmissionController:
    """Admission management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_admission(self, hospital_id: int, admission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new admission.
        
        Args:
            hospital_id: Hospital ID
            admission_data: Admission data dictionary
            
        Returns:
            Created admission data
        """
        try:
            # Generate admission number
            admission_number = generate_admission_number("HOS", "IPD")
            
            admission = Admission(
                hospital_id=hospital_id,
                patient_id=admission_data["patient_id"],
                admission_number=admission_number,
                department_id=admission_data["department_id"],
                consultant_id=admission_data["consultant_id"],
                bed_id=admission_data.get("bed_id"),
                room_id=admission_data.get("room_id"),
                admission_date=datetime.utcnow(),
                admission_time=admission_data.get("admission_time"),
                estimated_discharge_date=admission_data.get("estimated_discharge_date"),
                chief_complaint=admission_data["chief_complaint"],
                preliminary_diagnosis=admission_data.get("preliminary_diagnosis"),
                billing_type=admission_data["billing_type"],
                panel_id=admission_data.get("panel_id"),
                status=AdmissionStatus.ADMITTED,
                is_critical=admission_data.get("is_critical", False),
                reference_number=admission_data.get("reference_number"),
                referral_from=admission_data.get("referral_from")
            )
            
            self.db.add(admission)
            self.db.commit()
            self.db.refresh(admission)
            
            return {
                "success": True,
                "message": "Patient admitted successfully",
                "admission_id": admission.id,
                "admission_number": admission.admission_number
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def get_admission(self, hospital_id: int, admission_id: int) -> Optional[Dict[str, Any]]:
        """Get admission by ID.
        
        Args:
            hospital_id: Hospital ID
            admission_id: Admission ID
            
        Returns:
            Admission data or None
        """
        try:
            admission = self.db.query(Admission).filter(
                Admission.id == admission_id,
                Admission.hospital_id == hospital_id
            ).first()
            
            if admission:
                days = (date.today() - admission.admission_date.date()).days if admission.admission_date else 0
                return {
                    "id": admission.id,
                    "admission_number": admission.admission_number,
                    "patient_id": admission.patient_id,
                    "department_id": admission.department_id,
                    "consultant_id": admission.consultant_id,
                    "admission_date": admission.admission_date,
                    "chief_complaint": admission.chief_complaint,
                    "preliminary_diagnosis": admission.preliminary_diagnosis,
                    "final_diagnosis": admission.final_diagnosis,
                    "billing_type": admission.billing_type,
                    "status": admission.status.value,
                    "is_critical": admission.is_critical,
                    "current_stay_days": days
                }
            return None
        except Exception:
            return None

    def discharge_patient(self, hospital_id: int, admission_id: int, discharge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Discharge a patient.
        
        Args:
            hospital_id: Hospital ID
            admission_id: Admission ID
            discharge_data: Discharge data
            
        Returns:
            Discharge result
        """
        try:
            admission = self.db.query(Admission).filter(
                Admission.id == admission_id,
                Admission.hospital_id == hospital_id
            ).first()
            
            if not admission:
                return {"success": False, "error": "Admission not found"}
            
            admission.actual_discharge_date = date.today()
            admission.status = AdmissionStatus.DISCHARGED
            admission.discharge_reason = DischargeReason[discharge_data["discharge_reason"].upper()]
            admission.discharge_notes = discharge_data.get("discharge_notes")
            admission.final_diagnosis = discharge_data.get("final_diagnosis")
            
            # Calculate total stay days
            if admission.admission_date:
                admission.total_stay_days = (admission.actual_discharge_date - admission.admission_date.date()).days + 1
            
            self.db.commit()
            
            return {
                "success": True,
                "message": "Patient discharged successfully",
                "total_stay_days": admission.total_stay_days
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_admissions(self, hospital_id: int, status: str = None, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List admissions.
        
        Args:
            hospital_id: Hospital ID
            status: Filter by status
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of admissions
        """
        try:
            query = self.db.query(Admission).filter(Admission.hospital_id == hospital_id)
            
            if status:
                query = query.filter(Admission.status == AdmissionStatus[status.upper()])
            
            total = query.count()
            admissions = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "admissions": [
                    {
                        "id": a.id,
                        "admission_number": a.admission_number,
                        "patient_id": a.patient_id,
                        "admission_date": a.admission_date,
                        "status": a.status.value,
                        "is_critical": a.is_critical
                    }
                    for a in admissions
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class PrescriptionController:
    """Prescription management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_prescription(self, admission_id: int, prescription_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new prescription.
        
        Args:
            admission_id: Admission ID
            prescription_data: Prescription data
            
        Returns:
            Created prescription data
        """
        try:
            # Generate prescription number
            prescription_number = generate_prescription_number("HOS")
            
            prescription = Prescription(
                admission_id=admission_id,
                prescription_number=prescription_number,
                prescription_date=date.today(),
                prescribed_by=prescription_data["prescribed_by"],
                notes=prescription_data.get("notes")
            )
            
            self.db.add(prescription)
            self.db.commit()
            self.db.refresh(prescription)
            
            # Add medicines
            for medicine in prescription_data.get("medicines", []):
                item = PrescriptionItem(
                    prescription_id=prescription.id,
                    medicine_name=medicine["medicine_name"],
                    medicine_code=medicine.get("medicine_code"),
                    dosage=medicine["dosage"],
                    frequency=medicine["frequency"],
                    duration_days=medicine["duration_days"],
                    route=medicine.get("route"),
                    instructions=medicine.get("instructions"),
                    warning=medicine.get("warning")
                )
                self.db.add(item)
            
            self.db.commit()
            
            return {
                "success": True,
                "message": "Prescription created successfully",
                "prescription_id": prescription.id,
                "prescription_number": prescription.prescription_number
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}
