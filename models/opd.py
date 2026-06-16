"""OPD (Outpatient Department) models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from models import BaseModel
import enum


class AppointmentStatus(str, enum.Enum):
    """Appointment status enumeration."""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class ConsultationType(str, enum.Enum):
    """Consultation type enumeration."""
    NEW = "new"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"


class Appointment(BaseModel):
    """OPD Appointment model."""

    __tablename__ = "appointments"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False, index=True)
    appointment_date = Column(Date, nullable=False, index=True)
    appointment_time = Column(String(10), nullable=False)  # HH:MM format
    appointment_number = Column(String(30), nullable=True)  # Token number
    consultation_type = Column(Enum(ConsultationType), default=ConsultationType.NEW)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, index=True)
    billing_type = Column(String(50), nullable=False)  # cash, credit, insurance, panel
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=True, index=True)
    chief_complaint = Column(Text, nullable=False)
    estimated_consultation_time = Column(Integer, nullable=True)  # in minutes
    is_emergency = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    cancellation_date = Column(DateTime, nullable=True)
    check_in_time = Column(DateTime, nullable=True)
    consultation_start_time = Column(DateTime, nullable=True)
    consultation_end_time = Column(DateTime, nullable=True)

    # Relationships
    hospital = relationship("Hospital")
    patient = relationship("Patient", back_populates="appointments")
    department = relationship("Department", back_populates="appointments")
    consultant = relationship("Consultant", back_populates="appointments")
    panel = relationship("Panel")
    consultation = relationship("Consultation", back_populates="appointment", uselist=False, cascade="all, delete-orphan")


class Consultation(BaseModel):
    """OPD Consultation details."""

    __tablename__ = "consultations"

    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False, unique=True, index=True)
    consultation_notes = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    examination_findings = Column(Text, nullable=True)
    investigations_advised = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    follow_up_days = Column(Integer, nullable=True)
    referred_to_specialist = Column(Boolean, default=False)
    referral_department = Column(String(100), nullable=True)
    referral_reason = Column(Text, nullable=True)
    is_admission_recommended = Column(Boolean, default=False)
    admission_reason = Column(Text, nullable=True)
    consultation_fee = Column(Numeric(10, 2), nullable=True)
    discount_amount = Column(Numeric(10, 2), default=0)

    # Relationships
    appointment = relationship("Appointment", back_populates="consultation")
    consultation_prescriptions = relationship("ConsultationPrescription", back_populates="consultation", cascade="all, delete-orphan")
    consultation_investigations = relationship("ConsultationInvestigation", back_populates="consultation", cascade="all, delete-orphan")


class ConsultationPrescription(BaseModel):
    """OPD Consultation prescription."""

    __tablename__ = "consultation_prescriptions"

    consultation_id = Column(Integer, ForeignKey("consultations.id"), nullable=False, index=True)
    prescription_number = Column(String(50), unique=True, nullable=False, index=True)
    medicine_name = Column(String(150), nullable=False)
    medicine_code = Column(String(20), nullable=True)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)  # Once, Twice, Three times, etc.
    duration_days = Column(Integer, nullable=False)
    route = Column(String(50), nullable=True)  # Oral, IV, IM, etc.
    instructions = Column(Text, nullable=True)
    generic_name = Column(String(150), nullable=True)
    warning = Column(Text, nullable=True)
    is_printed = Column(Boolean, default=False)

    # Relationships
    consultation = relationship("Consultation", back_populates="consultation_prescriptions")


class ConsultationInvestigation(BaseModel):
    """OPD Consultation investigations advised."""

    __tablename__ = "consultation_investigations"

    consultation_id = Column(Integer, ForeignKey("consultations.id"), nullable=False, index=True)
    investigation_name = Column(String(150), nullable=False)
    investigation_code = Column(String(20), nullable=True)
    category = Column(String(50), nullable=True)  # Pathology, Radiology, etc.
    priority = Column(String(20), nullable=True)  # Routine, Urgent
    status = Column(String(50), default="advised")  # advised, ordered, completed, results_available
    ordered_date = Column(Date, nullable=True)
    specimen_collected_date = Column(Date, nullable=True)
    result_date = Column(Date, nullable=True)
    instructions = Column(Text, nullable=True)
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    actual_cost = Column(Numeric(10, 2), nullable=True)

    # Relationships
    consultation = relationship("Consultation", back_populates="consultation_investigations")


class WaitingQueue(BaseModel):
    """Waiting queue management for OPD."""

    __tablename__ = "waiting_queues"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False, unique=True, index=True)
    queue_number = Column(Integer, nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    called_time = Column(DateTime, nullable=True)
    consultation_time = Column(DateTime, nullable=True)
    status = Column(String(50), default="waiting")  # waiting, called, consulting, completed, cancelled
    wait_duration_minutes = Column(Integer, nullable=True)

    hospital = relationship("Hospital")
    appointment = relationship("Appointment")


class OPDVital(BaseModel):
    """OPD Vital signs recording."""

    __tablename__ = "opd_vitals"

    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False, index=True)
    recorded_date = Column(Date, nullable=False)
    recorded_time = Column(String(10), nullable=False)  # HH:MM format
    height = Column(Numeric(5, 2), nullable=True)  # cm
    weight = Column(Numeric(5, 2), nullable=True)  # kg
    bmi = Column(Numeric(5, 2), nullable=True)  # Body Mass Index
    temperature = Column(Numeric(5, 2), nullable=True)  # Celsius
    pulse_rate = Column(Integer, nullable=True)  # beats per minute
    respiratory_rate = Column(Integer, nullable=True)  # breaths per minute
    systolic_bp = Column(Integer, nullable=True)  # Systolic blood pressure
    diastolic_bp = Column(Integer, nullable=True)  # Diastolic blood pressure
    oxygen_saturation = Column(Numeric(5, 2), nullable=True)  # Percentage
    blood_glucose = Column(Numeric(7, 2), nullable=True)  # mg/dL
    recorded_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    appointment = relationship("Appointment")
