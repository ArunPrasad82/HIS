"""Consultant and staff models."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from models import BaseModel
import enum


class ConsultantSpecialty(str, enum.Enum):
    """Consultant specialty enumeration."""
    GENERAL_MEDICINE = "general_medicine"
    SURGERY = "surgery"
    PEDIATRICS = "pediatrics"
    GYNECOLOGY = "gynecology"
    ORTHOPEDICS = "orthopedics"
    CARDIOLOGY = "cardiology"
    NEUROLOGY = "neurology"
    PSYCHIATRY = "psychiatry"
    DERMATOLOGY = "dermatology"
    OTHER = "other"


class Consultant(BaseModel):
    """Consultant master data model."""

    __tablename__ = "consultants"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    registration_number = Column(String(50), nullable=False)  # Medical council registration
    qualification = Column(String(100), nullable=True)
    specialty = Column(Enum(ConsultantSpecialty), nullable=False)
    experience_years = Column(Integer, nullable=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    gender = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    consultation_fee = Column(Numeric(10, 2), nullable=True)
    follow_up_fee = Column(Numeric(10, 2), nullable=True)
    procedure_fee = Column(Numeric(10, 2), nullable=True)
    is_available = Column(Boolean, default=True)
    availability_schedule = Column(Text, nullable=True)  # JSON format
    bio = Column(Text, nullable=True)

    # Relationships
    hospital = relationship("Hospital", back_populates="consultants")
    department = relationship("Department", back_populates="consultants")
    appointments = relationship("Appointment", back_populates="consultant")
    admissions = relationship("Admission", back_populates="consultant")
    consultation_charges = relationship("ConsultationCharge", back_populates="consultant", cascade="all, delete-orphan")


class ConsultationCharge(BaseModel):
    """Consultation charge for consultant per panel/billing type."""

    __tablename__ = "consultation_charges"

    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=True, index=True)  # NULL for cash
    charge_type = Column(String(50), nullable=False)  # consultation, follow_up, procedure
    amount = Column(Numeric(10, 2), nullable=False)
    effective_from = Column(DateTime, default=datetime.utcnow)
    effective_to = Column(DateTime, nullable=True)

    # Relationships
    consultant = relationship("Consultant", back_populates="consultation_charges")
    panel = relationship("Panel")
