"""Billing and payment models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from models import BaseModel
import enum


class BillingType(str, enum.Enum):
    """Billing type enumeration."""
    CASH = "cash"
    CREDIT = "credit"
    INSURANCE = "insurance"
    PANEL = "panel"
    COMBINED = "combined"  # Mix of above


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"
    REFUNDED = "refunded"


class PaymentMode(str, enum.Enum):
    """Payment mode enumeration."""
    CASH = "cash"
    CHEQUE = "cheque"
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"
    NEFT = "neft"
    RTGS = "rtgs"
    UPI = "upi"
    ONLINE = "online"


class Billing(BaseModel):
    """Billing/Invoice model."""

    __tablename__ = "billings"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    invoice_number = Column(String(30), unique=True, nullable=False, index=True)
    invoice_date = Column(Date, nullable=False, index=True)
    invoice_time = Column(String(10), nullable=True)  # HH:MM format
    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=True, index=True)  # For IPD
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True, index=True)  # For OPD
    billing_type = Column(Enum(BillingType), nullable=False)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=True, index=True)
    consultation_fee = Column(Numeric(10, 2), default=0)
    procedures_cost = Column(Numeric(10, 2), default=0)
    medicines_cost = Column(Numeric(10, 2), default=0)
    investigation_cost = Column(Numeric(10, 2), default=0)
    bed_charge = Column(Numeric(10, 2), default=0)
    accommodation_charge = Column(Numeric(10, 2), default=0)
    miscellaneous_charge = Column(Numeric(10, 2), default=0)
    subtotal = Column(Numeric(15, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0)
    discount_reason = Column(String(100), nullable=True)
    tax_amount = Column(Numeric(10, 2), default=0)
    tax_percentage = Column(Numeric(5, 2), default=0)
    total_amount = Column(Numeric(15, 2), nullable=False)
    amount_paid = Column(Numeric(15, 2), default=0)
    balance_amount = Column(Numeric(15, 2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    due_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    insurance_claim_submitted = Column(Boolean, default=False)
    insurance_claim_date = Column(Date, nullable=True)
    insurance_claim_amount = Column(Numeric(15, 2), nullable=True)
    insurance_approved_amount = Column(Numeric(15, 2), nullable=True)
    reference_number = Column(String(50), nullable=True)
    cancellation_date = Column(Date, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    cancelled_by = Column(String(100), nullable=True)

    # Relationships
    hospital = relationship("Hospital")
    patient = relationship("Patient", back_populates="billings")
    admission = relationship("Admission")
    appointment = relationship("Appointment")
    panel = relationship("Panel")
    billing_items = relationship("BillingItem", back_populates="billing", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="billing", cascade="all, delete-orphan")
    tax_details = relationship("BillingTax", back_populates="billing", cascade="all, delete-orphan")


class BillingItem(BaseModel):
    """Individual items in a billing/invoice."""

    __tablename__ = "billing_items"

    billing_id = Column(Integer, ForeignKey("billings.id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True, index=True)
    item_description = Column(String(200), nullable=False)
    item_code = Column(String(20), nullable=True)
    quantity = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)
    panel_rate = Column(Numeric(10, 2), nullable=True)  # If different from unit price
    discount_amount = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    notes = Column(Text, nullable=True)
    bill_date = Column(Date, nullable=False)

    # Relationships
    billing = relationship("Billing", back_populates="billing_items")
    service = relationship("Service", back_populates="billing_items")


class Payment(BaseModel):
    """Payment transactions against billing."""

    __tablename__ = "payments"

    billing_id = Column(Integer, ForeignKey("billings.id"), nullable=False, index=True)
    payment_date = Column(Date, nullable=False, index=True)
    payment_time = Column(String(10), nullable=True)  # HH:MM format
    payment_mode = Column(Enum(PaymentMode), nullable=False)
    amount_paid = Column(Numeric(15, 2), nullable=False)
    receipt_number = Column(String(30), unique=True, nullable=False, index=True)
    reference_number = Column(String(50), nullable=True)  # Cheque no, Transaction ID, etc.
    remarks = Column(Text, nullable=True)
    received_by = Column(String(100), nullable=True)
    bank_name = Column(String(50), nullable=True)  # For cheque payments
    cheque_number = Column(String(20), nullable=True)
    cheque_date = Column(Date, nullable=True)
    transaction_id = Column(String(50), nullable=True)  # For online payments
    is_reversed = Column(Boolean, default=False)
    reversal_date = Column(Date, nullable=True)
    reversal_reason = Column(Text, nullable=True)

    # Relationships
    billing = relationship("Billing", back_populates="payments")


class BillingTax(BaseModel):
    """Tax details for billing."""

    __tablename__ = "billing_taxes"

    billing_id = Column(Integer, ForeignKey("billings.id"), nullable=False, index=True)
    tax_type = Column(String(50), nullable=False)  # SGST, CGST, IGST, VAT, etc.
    tax_rate = Column(Numeric(5, 2), nullable=False)
    taxable_amount = Column(Numeric(15, 2), nullable=False)
    tax_amount = Column(Numeric(15, 2), nullable=False)
    tax_number = Column(String(50), nullable=True)  # GST number, VAT number, etc.

    # Relationships
    billing = relationship("Billing", back_populates="tax_details")


class CreditNote(BaseModel):
    """Credit note for billing adjustments."""

    __tablename__ = "credit_notes"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    billing_id = Column(Integer, ForeignKey("billings.id"), nullable=False, index=True)
    credit_note_number = Column(String(30), unique=True, nullable=False, index=True)
    credit_note_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    notes = Column(Text, nullable=True)
    authorized_by = Column(String(100), nullable=True)

    hospital = relationship("Hospital")
    billing = relationship("Billing")


class DebitNote(BaseModel):
    """Debit note for billing adjustments."""

    __tablename__ = "debit_notes"

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    billing_id = Column(Integer, ForeignKey("billings.id"), nullable=False, index=True)
    debit_note_number = Column(String(30), unique=True, nullable=False, index=True)
    debit_note_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    notes = Column(Text, nullable=True)
    authorized_by = Column(String(100), nullable=True)

    hospital = relationship("Hospital")
    billing = relationship("Billing")
