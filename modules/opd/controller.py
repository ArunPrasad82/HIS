"""OPD (Outpatient Department) controllers."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.opd import Appointment, Consultation, ConsultationPrescription, ConsultationInvestigation, WaitingQueue, OPDVital, AppointmentStatus, ConsultationType
from datetime import datetime, date
import math


class AppointmentController:
    """Appointment management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_appointment(self, hospital_id: int, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new appointment.
        
        Args:
            hospital_id: Hospital ID
            appointment_data: Appointment data dictionary
            
        Returns:
            Created appointment data
        """
        try:
            appointment = Appointment(
                hospital_id=hospital_id,
                patient_id=appointment_data["patient_id"],
                department_id=appointment_data["department_id"],
                consultant_id=appointment_data["consultant_id"],
                appointment_date=appointment_data["appointment_date"],
                appointment_time=appointment_data["appointment_time"],
                consultation_type=ConsultationType[appointment_data.get("consultation_type", "NEW").upper()],
                chief_complaint=appointment_data["chief_complaint"],
                billing_type=appointment_data["billing_type"],
                panel_id=appointment_data.get("panel_id"),
                is_emergency=appointment_data.get("is_emergency", False),
                notes=appointment_data.get("notes")
            )
            
            self.db.add(appointment)
            self.db.commit()
            self.db.refresh(appointment)
            
            return {
                "success": True,
                "message": "Appointment created successfully",
                "appointment_id": appointment.id,
                "appointment_date": appointment.appointment_date.isoformat(),
                "appointment_time": appointment.appointment_time
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def get_appointment(self, hospital_id: int, appointment_id: int) -> Optional[Dict[str, Any]]:
        """Get appointment by ID.
        
        Args:
            hospital_id: Hospital ID
            appointment_id: Appointment ID
            
        Returns:
            Appointment data or None
        """
        try:
            appointment = self.db.query(Appointment).filter(
                Appointment.id == appointment_id,
                Appointment.hospital_id == hospital_id
            ).first()
            
            if appointment:
                return {
                    "id": appointment.id,
                    "patient_id": appointment.patient_id,
                    "appointment_date": appointment.appointment_date,
                    "appointment_time": appointment.appointment_time,
                    "consultant_id": appointment.consultant_id,
                    "department_id": appointment.department_id,
                    "chief_complaint": appointment.chief_complaint,
                    "status": appointment.status.value,
                    "billing_type": appointment.billing_type,
                    "is_emergency": appointment.is_emergency
                }
            return None
        except Exception:
            return None

    def list_appointments(self, hospital_id: int, appointment_date: date = None, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List appointments.
        
        Args:
            hospital_id: Hospital ID
            appointment_date: Filter by date
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of appointments
        """
        try:
            query = self.db.query(Appointment).filter(Appointment.hospital_id == hospital_id)
            
            if appointment_date:
                query = query.filter(Appointment.appointment_date == appointment_date)
            
            total = query.count()
            appointments = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "appointments": [
                    {
                        "id": a.id,
                        "patient_id": a.patient_id,
                        "appointment_date": a.appointment_date,
                        "appointment_time": a.appointment_time,
                        "status": a.status.value,
                        "is_emergency": a.is_emergency
                    }
                    for a in appointments
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cancel_appointment(self, hospital_id: int, appointment_id: int, reason: str) -> Dict[str, Any]:
        """Cancel appointment.
        
        Args:
            hospital_id: Hospital ID
            appointment_id: Appointment ID
            reason: Cancellation reason
            
        Returns:
            Cancellation result
        """
        try:
            appointment = self.db.query(Appointment).filter(
                Appointment.id == appointment_id,
                Appointment.hospital_id == hospital_id
            ).first()
            
            if not appointment:
                return {"success": False, "error": "Appointment not found"}
            
            appointment.status = AppointmentStatus.CANCELLED
            appointment.cancellation_reason = reason
            appointment.cancellation_date = datetime.utcnow()
            
            self.db.commit()
            
            return {"success": True, "message": "Appointment cancelled successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}


class ConsultationController:
    """Consultation management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_consultation(self, appointment_id: int, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create consultation record.
        
        Args:
            appointment_id: Appointment ID
            consultation_data: Consultation data
            
        Returns:
            Created consultation data
        """
        try:
            consultation = Consultation(
                appointment_id=appointment_id,
                consultation_notes=consultation_data.get("consultation_notes"),
                diagnosis=consultation_data.get("diagnosis"),
                examination_findings=consultation_data.get("examination_findings"),
                investigations_advised=consultation_data.get("investigations_advised"),
                treatment_plan=consultation_data.get("treatment_plan"),
                follow_up_date=consultation_data.get("follow_up_date"),
                follow_up_days=consultation_data.get("follow_up_days"),
                referred_to_specialist=consultation_data.get("referred_to_specialist", False),
                referral_department=consultation_data.get("referral_department"),
                referral_reason=consultation_data.get("referral_reason"),
                is_admission_recommended=consultation_data.get("is_admission_recommended", False),
                admission_reason=consultation_data.get("admission_reason"),
                consultation_fee=consultation_data.get("consultation_fee"),
                discount_amount=consultation_data.get("discount_amount", 0)
            )
            
            self.db.add(consultation)
            self.db.commit()
            self.db.refresh(consultation)
            
            # Update appointment status
            appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
            if appointment:
                appointment.status = AppointmentStatus.COMPLETED
                self.db.commit()
            
            return {
                "success": True,
                "message": "Consultation created successfully",
                "consultation_id": consultation.id
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def add_prescription(self, consultation_id: int, medicine_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add prescription medicine to consultation.
        
        Args:
            consultation_id: Consultation ID
            medicine_data: Medicine data
            
        Returns:
            Result
        """
        try:
            prescription = ConsultationPrescription(
                consultation_id=consultation_id,
                prescription_number=f"RX-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                medicine_name=medicine_data["medicine_name"],
                medicine_code=medicine_data.get("medicine_code"),
                dosage=medicine_data["dosage"],
                frequency=medicine_data["frequency"],
                duration_days=medicine_data["duration_days"],
                route=medicine_data.get("route"),
                instructions=medicine_data.get("instructions"),
                generic_name=medicine_data.get("generic_name"),
                warning=medicine_data.get("warning")
            )
            
            self.db.add(prescription)
            self.db.commit()
            
            return {"success": True, "message": "Medicine added to prescription"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def add_investigation(self, consultation_id: int, investigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add investigation to consultation.
        
        Args:
            consultation_id: Consultation ID
            investigation_data: Investigation data
            
        Returns:
            Result
        """
        try:
            investigation = ConsultationInvestigation(
                consultation_id=consultation_id,
                investigation_name=investigation_data["investigation_name"],
                investigation_code=investigation_data.get("investigation_code"),
                category=investigation_data.get("category"),
                priority=investigation_data.get("priority", "Routine"),
                instructions=investigation_data.get("instructions"),
                estimated_cost=investigation_data.get("estimated_cost")
            )
            
            self.db.add(investigation)
            self.db.commit()
            
            return {"success": True, "message": "Investigation added successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}
