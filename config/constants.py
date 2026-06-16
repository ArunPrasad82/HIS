"""Application constants."""

# User Roles
ROLES = {
    "SUPER_ADMIN": "super_admin",
    "ADMIN": "admin",
    "CONSULTANT": "consultant",
    "DOCTOR": "doctor",
    "NURSE": "nurse",
    "RECEPTIONIST": "receptionist",
    "BILLING_STAFF": "billing_staff",
    "ACCOUNTANT": "accountant",
}

# User Types
USER_TYPES = {
    "INTERNAL": "internal",
    "EXTERNAL": "external",
}

# Billing Types
BILLING_TYPES = {
    "CASH": "cash",
    "CREDIT": "credit",
    "INSURANCE": "insurance",
    "PANEL": "panel",
}

# Patient Status
PATIENT_STATUS = {
    "ACTIVE": "active",
    "INACTIVE": "inactive",
    "DECEASED": "deceased",
}

# Admission Status
ADMISSION_STATUS = {
    "PLANNED": "planned",
    "ADMITTED": "admitted",
    "DISCHARGED": "discharged",
    "TRANSFERRED": "transferred",
    "ABSCONDED": "absconded",
}

# Discharge Reason
DISCHARGE_REASON = {
    "CURED": "cured",
    "IMPROVED": "improved",
    "NOT_IMPROVED": "not_improved",
    "AGAINST_ADVICE": "against_advice",
    "LAMA": "lama",  # Left Against Medical Advice
    "REFERRAL": "referral",
    "DECEASED": "deceased",
}

# Gender
GENDER = {
    "MALE": "male",
    "FEMALE": "female",
    "OTHER": "other",
}

# Appointment Status
APPOINTMENT_STATUS = {
    "SCHEDULED": "scheduled",
    "COMPLETED": "completed",
    "CANCELLED": "cancelled",
    "NO_SHOW": "no_show",
}

# Service Categories
SERVICE_CATEGORY = {
    "CONSULTATION": "consultation",
    "PROCEDURE": "procedure",
    "INVESTIGATION": "investigation",
    "PACKAGE": "package",
    "ACCOMMODATION": "accommodation",
}

# Panel Types
PANEL_TYPE = {
    "INSURANCE": "insurance",
    "CORPORATE": "corporate",
    "GOVERNMENT": "government",
}

# Payment Status
PAYMENT_STATUS = {
    "PENDING": "pending",
    "PARTIAL": "partial",
    "PAID": "paid",
    "OVERDUE": "overdue",
}

# Room Types
ROOM_TYPE = {
    "GENERAL": "general",
    "SEMI_PRIVATE": "semi_private",
    "PRIVATE": "private",
    "ICU": "icu",
}

# Bed Status
BED_STATUS = {
    "AVAILABLE": "available",
    "OCCUPIED": "occupied",
    "MAINTENANCE": "maintenance",
    "BLOCKED": "blocked",
}
