"""Patient management models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from models import BaseModel
import enum


class PatientStatus(str, enum.Enum):
    """Patient status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DECEASED = "deceased"


class Patient(BaseModel):
    """Patient master data model."""

    __tablename__ = "patients"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    uhid = Column(String(30), unique=True, nullable=False, index=True)  # Universal Health ID
    abha_id = Column(String(20), unique=True, nullable=True, index=True)  # Ayushman Bharat ID
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)  # Male, Female, Other
    blood_group = Column(String(5), nullable=True)
    aadhar_number = Column(String(12), nullable=True)
    mobile_primary = Column(String(20), nullable=False, index=True)
    mobile_secondary = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=True)
    country = Column(String(50), nullable=True, default="India")
    occupation = Column(String(50), nullable=True)
    education = Column(String(50), nullable=True)
    marital_status = Column(String(20), nullable=True)  # Single, Married, Divorced, Widowed
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    status = Column(Enum(PatientStatus), default=PatientStatus.ACTIVE)
    registration_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)

    # Relationships
    hospital = relationship("Hospital", back_populates="patients")
    medical_history = relationship("PatientMedicalHistory", back_populates="patient", cascade="all, delete-orphan")
    allergies = relationship("PatientAllergy", back_populates="patient", cascade="all, delete-orphan")
    admissions = relationship("Admission", back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    billings = relationship("Billing", back_populates="patient", cascade="all, delete-orphan")

    def get_full_name(self):
        """Get full name."""
        name = self.first_name
        if self.middle_name:
            name += f" {self.middle_name}"
        if self.last_name:
            name += f" {self.last_name}"
        return name


class PatientMedicalHistory(BaseModel):
    """Patient medical history model."""

    __tablename__ = "patient_medical_history"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    condition_name = Column(String(100), nullable=False)
    icd_code = Column(String(10), nullable=True)  # ICD-10 code
    diagnosis_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=True)  # Active, Resolved, Chronic
    notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="medical_history")


class PatientAllergy(BaseModel):
    """Patient allergy model."""

    __tablename__ = "patient_allergies"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    allergen = Column(String(100), nullable=False)
    reaction = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=True)  # Mild, Moderate, Severe
    notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="allergies")


class PatientPanel(BaseModel):
    """Patient panel/insurance linking model."""

    __tablename__ = "patient_panels"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=False, index=True)
    member_id = Column(String(50), nullable=False)  # Insurance/Panel member ID
    policy_number = Column(String(50), nullable=True)
    policy_start_date = Column(Date, nullable=True)
    policy_end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    patient = relationship("Patient")
    panel = relationship("Panel")
