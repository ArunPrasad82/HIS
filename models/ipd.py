"""IPD (Inpatient Department) models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from models import BaseModel
import enum


class AdmissionStatus(str, enum.Enum):
    """Admission status enumeration."""
    PLANNED = "planned"
    ADMITTED = "admitted"
    DISCHARGED = "discharged"
    TRANSFERRED = "transferred"
    ABSCONDED = "absconded"
    DECEASED = "deceased"


class DischargeReason(str, enum.Enum):
    """Discharge reason enumeration."""
    CURED = "cured"
    IMPROVED = "improved"
    NOT_IMPROVED = "not_improved"
    AGAINST_ADVICE = "against_advice"
    LAMA = "lama"  # Left Against Medical Advice
    REFERRAL = "referral"
    DECEASED = "deceased"


class Admission(BaseModel):
    """IPD Admission model."""

    __tablename__ = "admissions"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    admission_number = Column(String(30), unique=True, nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False, index=True)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True, index=True)
    admission_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    admission_time = Column(String(10), nullable=True)  # HH:MM format
    estimated_discharge_date = Column(Date, nullable=True)
    actual_discharge_date = Column(Date, nullable=True)
    chief_complaint = Column(Text, nullable=False)
    preliminary_diagnosis = Column(Text, nullable=True)
    final_diagnosis = Column(Text, nullable=True)
    billing_type = Column(String(50), nullable=False)  # cash, credit, insurance, panel
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=True, index=True)
    status = Column(Enum(AdmissionStatus), default=AdmissionStatus.ADMITTED, index=True)
    discharge_reason = Column(Enum(DischargeReason), nullable=True)
    discharge_notes = Column(Text, nullable=True)
    is_critical = Column(Boolean, default=False)
    total_stay_days = Column(Integer, nullable=True)
    reference_number = Column(String(50), nullable=True)
    referral_from = Column(String(100), nullable=True)

    # Relationships
    hospital = relationship("Hospital")
    patient = relationship("Patient", back_populates="admissions")
    department = relationship("Department", back_populates="admissions")
    consultant = relationship("Consultant", back_populates="admissions")
    bed = relationship("Bed", back_populates="admissions")
    room = relationship("Room")
    panel = relationship("Panel")
    treatments = relationship("Treatment", back_populates="admission", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="admission", cascade="all, delete-orphan")
    vitals = relationship("PatientVital", back_populates="admission", cascade="all, delete-orphan")
    notes = relationship("AdmissionNote", back_populates="admission", cascade="all, delete-orphan")
    surgeries = relationship("Surgery", back_populates="admission", cascade="all, delete-orphan")


class Treatment(BaseModel):
    """Treatment/Procedure during admission."""

    __tablename__ = "treatments"

    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False, index=True)
    treatment_date = Column(Date, nullable=False)
    treatment_time = Column(String(10), nullable=True)  # HH:MM format
    treatment_type = Column(String(100), nullable=False)  # Medication, Procedure, etc.
    description = Column(Text, nullable=False)
    provider_name = Column(String(100), nullable=True)  # Doctor/Nurse name
    outcome = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    admission = relationship("Admission", back_populates="treatments")


class Prescription(BaseModel):
    """Prescription model."""

    __tablename__ = "prescriptions"

    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False, index=True)
    prescription_number = Column(String(50), unique=True, nullable=False, index=True)
    prescription_date = Column(Date, nullable=False)
    prescribed_by = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    admission = relationship("Admission", back_populates="prescriptions")
    medicines = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan")


class PrescriptionItem(BaseModel):
    """Individual medicine in prescription."""

    __tablename__ = "prescription_items"

    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False, index=True)
    medicine_name = Column(String(150), nullable=False)
    medicine_code = Column(String(20), nullable=True)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)  # Once, Twice, etc.
    duration_days = Column(Integer, nullable=False)
    route = Column(String(50), nullable=True)  # Oral, IV, IM, etc.
    instructions = Column(Text, nullable=True)
    warning = Column(Text, nullable=True)

    # Relationships
    prescription = relationship("Prescription", back_populates="medicines")


class PatientVital(BaseModel):
    """Patient vital signs recording."""

    __tablename__ = "patient_vitals"

    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False, index=True)
    recorded_date = Column(Date, nullable=False)
    recorded_time = Column(String(10), nullable=False)  # HH:MM format
    temperature = Column(Numeric(5, 2), nullable=True)  # Celsius
    pulse_rate = Column(Integer, nullable=True)  # beats per minute
    respiratory_rate = Column(Integer, nullable=True)  # breaths per minute
    systolic_bp = Column(Integer, nullable=True)  # Systolic blood pressure
    diastolic_bp = Column(Integer, nullable=True)  # Diastolic blood pressure
    oxygen_saturation = Column(Numeric(5, 2), nullable=True)  # Percentage
    blood_glucose = Column(Numeric(7, 2), nullable=True)  # mg/dL
    recorded_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    admission = relationship("Admission", back_populates="vitals")


class AdmissionNote(BaseModel):
    """Progress notes during admission."""

    __tablename__ = "admission_notes"

    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False, index=True)
    note_date = Column(Date, nullable=False)
    note_time = Column(String(10), nullable=False)  # HH:MM format
    note_type = Column(String(50), nullable=False)  # Progress Note, Clinical Note, etc.
    written_by = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    is_confidential = Column(Boolean, default=False)

    # Relationships
    admission = relationship("Admission", back_populates="notes")


class Surgery(BaseModel):
    """Surgical procedure during admission."""

    __tablename__ = "surgeries"

    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False, index=True)
    surgery_date = Column(Date, nullable=False)
    surgery_time = Column(String(10), nullable=False)  # HH:MM format
    surgery_name = Column(String(150), nullable=False)
    icd_code = Column(String(10), nullable=True)  # ICD-10 code
    surgeon_name = Column(String(100), nullable=False)
    anesthetist_name = Column(String(100), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    anesthesia_type = Column(String(50), nullable=True)
    procedure_notes = Column(Text, nullable=True)
    post_operative_notes = Column(Text, nullable=True)
    complications = Column(Text, nullable=True)
    blood_transfusion_required = Column(Boolean, default=False)
    blood_units_transfused = Column(Integer, nullable=True)
    implants_used = Column(Text, nullable=True)  # JSON format

    # Relationships
    admission = relationship("Admission", back_populates="surgeries")
