"""Service and package models."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from models import BaseModel
import enum


class ServiceCategory(str, enum.Enum):
    """Service category enumeration."""
    CONSULTATION = "consultation"
    PROCEDURE = "procedure"
    INVESTIGATION = "investigation"
    PACKAGE = "package"
    ACCOMMODATION = "accommodation"
    MEDICINE = "medicine"


class Service(BaseModel):
    """Service master data model."""

    __tablename__ = "services"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), nullable=False, unique=True)
    category = Column(Enum(ServiceCategory), nullable=False)
    description = Column(Text, nullable=True)
    hsncode = Column(String(20), nullable=True)  # For billing/GST
    icd_code = Column(String(10), nullable=True)  # ICD-10 code
    is_billable = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=False)

    # Relationships
    hospital = relationship("Hospital", back_populates="services")
    sub_services = relationship("SubService", back_populates="service", cascade="all, delete-orphan")
    service_rates = relationship("ServiceRate", back_populates="service", cascade="all, delete-orphan")
    billing_items = relationship("BillingItem", back_populates="service")


class SubService(BaseModel):
    """Sub-service master data model."""

    __tablename__ = "sub_services"

    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    is_billable = Column(Boolean, default=True)

    # Relationships
    service = relationship("Service", back_populates="sub_services")
    service_rates = relationship("ServiceRate", back_populates="sub_service", cascade="all, delete-orphan")


class ServiceRate(BaseModel):
    """Service rate configuration by panel/billing type."""

    __tablename__ = "service_rates"

    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    sub_service_id = Column(Integer, ForeignKey("sub_services.id"), nullable=True, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=True, index=True)  # NULL for cash
    rate_type = Column(String(50), nullable=False)  # cash, credit, insurance
    amount = Column(Numeric(10, 2), nullable=False)
    effective_from = Column(DateTime, default=datetime.utcnow)
    effective_to = Column(DateTime, nullable=True)
    is_negotiable = Column(Boolean, default=False)

    # Relationships
    service = relationship("Service", back_populates="service_rates")
    sub_service = relationship("SubService", back_populates="service_rates")
    panel = relationship("Panel")


class Package(BaseModel):
    """Package master data model (bundled services)."""

    __tablename__ = "packages"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # Surgery, Investigation, etc.
    base_price = Column(Numeric(10, 2), nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    number_of_days = Column(Integer, nullable=True)  # For packages spanning multiple days
    is_active = Column(Boolean, default=True)

    # Relationships
    hospital = relationship("Hospital", back_populates="packages")
    package_items = relationship("PackageItem", back_populates="package", cascade="all, delete-orphan")
    package_rates = relationship("PackageRate", back_populates="package", cascade="all, delete-orphan")


class PackageItem(BaseModel):
    """Items included in a package."""

    __tablename__ = "package_items"

    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    quantity = Column(Integer, default=1)
    sequence = Column(Integer, nullable=True)  # Order of services in package

    # Relationships
    package = relationship("Package", back_populates="package_items")
    service = relationship("Service")


class PackageRate(BaseModel):
    """Package rate configuration by panel/billing type."""

    __tablename__ = "package_rates"

    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=True, index=True)  # NULL for cash
    rate_type = Column(String(50), nullable=False)  # cash, credit, insurance
    amount = Column(Numeric(10, 2), nullable=False)
    effective_from = Column(DateTime, default=datetime.utcnow)
    effective_to = Column(DateTime, nullable=True)

    # Relationships
    package = relationship("Package", back_populates="package_rates")
    panel = relationship("Panel")
