"""ID and code generators."""

import uuid
from datetime import datetime
from typing import Optional


def generate_uhid(hospital_code: str, year: Optional[int] = None) -> str:
    """Generate unique UHID (Universal Health ID) for patient.
    
    Format: HOSP_CODE_YYYYMMDD_XXXX (where XXXX is sequential number)
    
    Args:
        hospital_code: Hospital identifier code
        year: Optional year override
        
    Returns:
        Generated UHID
    """
    if year is None:
        year = datetime.now().year
    
    timestamp = datetime.now().strftime("%Y%m%d")
    random_part = str(uuid.uuid4().int)[:4]
    uhid = f"{hospital_code}_{year}{random_part}"
    return uhid.upper()


def generate_abha_id(aadhar: str, name: str, dob: str) -> str:
    """Generate ABHA ID (Ayushman Bharat Health Account ID).
    
    Format: XX-XXXX-XXXX-XXXX (14 digits)
    
    Args:
        aadhar: Aadhar number
        name: Patient name
        dob: Date of birth (YYYY-MM-DD)
        
    Returns:
        Generated ABHA ID
    """
    # This is a placeholder implementation
    # In production, integrate with NDHM ABHA API
    import hashlib
    
    combined = f"{aadhar}{name}{dob}"
    hash_obj = hashlib.sha256(combined.encode())
    hash_hex = hash_obj.hexdigest()[:12]
    
    # Format as XX-XXXX-XXXX-XXXX
    abha_id = f"{hash_hex[:2]}-{hash_hex[2:6]}-{hash_hex[6:10]}-{hash_hex[10:14]}"
    return abha_id.upper()


def generate_invoice_number(hospital_code: str, invoice_type: str = "INV") -> str:
    """Generate invoice number.
    
    Format: INV_YYYYMMDD_XXXX
    
    Args:
        hospital_code: Hospital code
        invoice_type: Type of invoice (default: INV)
        
    Returns:
        Generated invoice number
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = str(uuid.uuid4().int)[:4]
    invoice_num = f"{hospital_code}_{invoice_type}_{timestamp}_{random_part}"
    return invoice_num.upper()


def generate_admission_number(hospital_code: str, ward_code: str) -> str:
    """Generate admission/registration number.
    
    Args:
        hospital_code: Hospital code
        ward_code: Ward/Department code
        
    Returns:
        Generated admission number
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = str(uuid.uuid4().int)[:3]
    admission_num = f"{hospital_code}{ward_code}{timestamp}{random_part}"
    return admission_num.upper()


def generate_prescription_number(hospital_code: str) -> str:
    """Generate prescription number.
    
    Args:
        hospital_code: Hospital code
        
    Returns:
        Generated prescription number
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = str(uuid.uuid4().int)[:3]
    prescription_num = f"{hospital_code}RX{timestamp}{random_part}"
    return prescription_num.upper()


def generate_reference_number(prefix: str = "REF") -> str:
    """Generate unique reference number.
    
    Args:
        prefix: Reference prefix
        
    Returns:
        Generated reference number
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = str(uuid.uuid4().int)[:6]
    ref_num = f"{prefix}_{timestamp}_{random_part}"
    return ref_num.upper()
