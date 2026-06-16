"""Panel and insurance models."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from models import BaseModel
import enum


class PanelType(str, enum.Enum):
    """Panel type enumeration."""
    INSURANCE = "insurance"
    CORPORATE = "corporate"
    GOVERNMENT = "government"
    NGO = "ngo"


class Panel(BaseModel):
    """Panel/Insurance master data model."""

    __tablename__ = "panels"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), nullable=False)
    panel_type = Column(Enum(PanelType), nullable=False)
    registration_number = Column(String(50), nullable=True)
    contact_person = Column(String(100), nullable=True)
    contact_email = Column(String(100), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    postal_code = Column(String(10), nullable=True)
    website = Column(String(100), nullable=True)
    agreement_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)

    # Relationships
    hospital = relationship("Hospital", back_populates="panels")
    panel_documents = relationship("PanelDocument", back_populates="panel", cascade="all, delete-orphan")


class PanelDocument(BaseModel):
    """Panel related documents (agreements, etc.)."""

    __tablename__ = "panel_documents"

    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=False, index=True)
    document_type = Column(String(50), nullable=False)  # Agreement, Rate Card, etc.
    document_name = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=False)
    version = Column(Integer, default=1)
    uploaded_date = Column(DateTime, default=datetime.utcnow)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)

    # Relationships
    panel = relationship("Panel", back_populates="panel_documents")
