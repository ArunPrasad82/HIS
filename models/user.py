"""User and authentication models."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models import BaseModel
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    CONSULTANT = "consultant"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"
    BILLING_STAFF = "billing_staff"
    ACCOUNTANT = "accountant"


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, nullable=True)

    # Relationships
    hospital = relationship("Hospital", back_populates="users")
    permissions = relationship("UserPermission", back_populates="user", cascade="all, delete-orphan")

    def get_full_name(self):
        """Get full name."""
        return f"{self.first_name} {self.last_name}"


class UserPermission(BaseModel):
    """User permission model."""

    __tablename__ = "user_permissions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_name = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=True)  # e.g., 'ipd', 'opd', 'billing'
    can_create = Column(Boolean, default=False)
    can_read = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    can_export = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="permissions")


class AuditLog(BaseModel):
    """Audit log for tracking changes."""

    __tablename__ = "audit_logs"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # CREATE, READ, UPDATE, DELETE
    entity_type = Column(String(50), nullable=False)  # Model name
    entity_id = Column(Integer, nullable=False)
    old_values = Column(Text, nullable=True)  # JSON format
    new_values = Column(Text, nullable=True)  # JSON format
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    user = relationship("User")
