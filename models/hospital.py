"""Hospital and configuration models."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from models import BaseModel


class Hospital(BaseModel):
    """Hospital master data model."""

    __tablename__ = "hospitals"

    name = Column(String(150), nullable=False, unique=True)
    code = Column(String(20), nullable=False, unique=True, index=True)
    registration_number = Column(String(50), nullable=True)
    address = Column(Text, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=True)
    country = Column(String(50), nullable=True, default="India")
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(100), nullable=True)
    license_number = Column(String(50), nullable=True)
    bed_strength = Column(Integer, nullable=True)
    database_name = Column(String(100), nullable=True)  # For multi-database support
    database_host = Column(String(100), nullable=True)
    database_port = Column(Integer, nullable=True)
    logo_path = Column(String(255), nullable=True)
    established_date = Column(DateTime, nullable=True)
    timezone = Column(String(50), default="Asia/Kolkata")

    # Relationships
    users = relationship("User", back_populates="hospital", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="hospital", cascade="all, delete-orphan")
    consultants = relationship("Consultant", back_populates="hospital", cascade="all, delete-orphan")
    patients = relationship("Patient", back_populates="hospital", cascade="all, delete-orphan")
    panels = relationship("Panel", back_populates="hospital", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="hospital", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="hospital", cascade="all, delete-orphan")
    beds = relationship("Bed", back_populates="hospital", cascade="all, delete-orphan")
    packages = relationship("Package", back_populates="hospital", cascade="all, delete-orphan")
    floors = relationship("Floor", back_populates="hospital", cascade="all, delete-orphan")
    billing_settings = relationship("BillingSettings", back_populates="hospital", cascade="all, delete-orphan")


class Department(BaseModel):
    """Department master data model."""

    __tablename__ = "departments"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    department_type = Column(String(50), nullable=True)  # IPD, OPD, etc.
    head_consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    is_operational = Column(Boolean, default=True)

    # Relationships
    hospital = relationship("Hospital", back_populates="departments")
    consultants = relationship("Consultant", back_populates="department")
    admissions = relationship("Admission", back_populates="department")
    appointments = relationship("Appointment", back_populates="department")


class Floor(BaseModel):
    """Floor/Wing master data model."""

    __tablename__ = "floors"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    floor_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    total_rooms = Column(Integer, default=0)
    total_beds = Column(Integer, default=0)

    # Relationships
    hospital = relationship("Hospital", back_populates="floors")
    rooms = relationship("Room", back_populates="floor")


class Room(BaseModel):
    """Room master data model."""

    __tablename__ = "rooms"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    floor_id = Column(Integer, ForeignKey("floors.id"), nullable=False, index=True)
    room_number = Column(String(20), nullable=False)
    room_type = Column(String(50), nullable=False)  # General, Semi-private, Private, ICU
    total_beds = Column(Integer, default=1)
    available_beds = Column(Integer, default=1)
    daily_rate = Column(Numeric(10, 2), nullable=True)
    description = Column(Text, nullable=True)
    amenities = Column(Text, nullable=True)  # JSON format

    # Relationships
    hospital = relationship("Hospital", back_populates="rooms")
    floor = relationship("Floor", back_populates="rooms")
    beds = relationship("Bed", back_populates="room")


class Bed(BaseModel):
    """Bed master data model."""

    __tablename__ = "beds"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, index=True)
    bed_number = Column(String(20), nullable=False)
    status = Column(String(50), default="available")  # available, occupied, maintenance, blocked
    is_icu_bed = Column(Boolean, default=False)
    is_critical_care = Column(Boolean, default=False)

    # Relationships
    hospital = relationship("Hospital", back_populates="beds")
    room = relationship("Room", back_populates="beds")
    admissions = relationship("Admission", back_populates="bed")


class BillingSettings(BaseModel):
    """Hospital billing configuration model."""

    __tablename__ = "billing_settings"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, unique=True, index=True)
    default_currency = Column(String(3), default="INR")
    tax_percentage = Column(Numeric(5, 2), default=0)
    discount_allowed = Column(Boolean, default=True)
    max_discount_percentage = Column(Numeric(5, 2), default=10)
    payment_terms = Column(Integer, nullable=True)  # Days
    auto_generate_invoice = Column(Boolean, default=True)
    invoice_prefix = Column(String(20), nullable=True)
    enable_credit_limit = Column(Boolean, default=True)
    default_credit_limit = Column(Numeric(15, 2), nullable=True)
    gst_number = Column(String(50), nullable=True)
    financial_year_start = Column(String(10), default="01-04")  # DD-MM

    # Relationships
    hospital = relationship("Hospital", back_populates="billing_settings")
