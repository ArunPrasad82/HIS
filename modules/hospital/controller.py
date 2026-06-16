"""Hospital management controllers."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.hospital import Hospital, Department, Floor, Room, Bed, BillingSettings
from datetime import datetime


class HospitalController:
    """Hospital management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_hospital(self, hospital_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new hospital.
        
        Args:
            hospital_data: Hospital data dictionary
            
        Returns:
            Created hospital data
        """
        try:
            # Check if hospital code already exists
            existing = self.db.query(Hospital).filter(
                Hospital.code == hospital_data["code"]
            ).first()
            
            if existing:
                return {"success": False, "error": "Hospital with this code already exists"}
            
            hospital = Hospital(
                name=hospital_data["name"],
                code=hospital_data["code"],
                registration_number=hospital_data.get("registration_number"),
                address=hospital_data["address"],
                city=hospital_data["city"],
                state=hospital_data["state"],
                postal_code=hospital_data.get("postal_code"),
                country=hospital_data.get("country", "India"),
                phone=hospital_data.get("phone"),
                email=hospital_data.get("email"),
                website=hospital_data.get("website"),
                license_number=hospital_data.get("license_number"),
                bed_strength=hospital_data.get("bed_strength"),
                database_name=hospital_data.get("database_name"),
                database_host=hospital_data.get("database_host"),
                database_port=hospital_data.get("database_port"),
                established_date=hospital_data.get("established_date")
            )
            
            self.db.add(hospital)
            self.db.commit()
            self.db.refresh(hospital)
            
            # Create default billing settings
            billing_settings = BillingSettings(hospital_id=hospital.id)
            self.db.add(billing_settings)
            self.db.commit()
            
            return {
                "success": True,
                "message": "Hospital created successfully",
                "hospital_id": hospital.id,
                "hospital_name": hospital.name
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def get_hospital(self, hospital_id: int) -> Optional[Dict[str, Any]]:
        """Get hospital by ID.
        
        Args:
            hospital_id: Hospital ID
            
        Returns:
            Hospital data or None
        """
        try:
            hospital = self.db.query(Hospital).filter(Hospital.id == hospital_id).first()
            if hospital:
                return {
                    "id": hospital.id,
                    "name": hospital.name,
                    "code": hospital.code,
                    "registration_number": hospital.registration_number,
                    "address": hospital.address,
                    "city": hospital.city,
                    "state": hospital.state,
                    "postal_code": hospital.postal_code,
                    "country": hospital.country,
                    "phone": hospital.phone,
                    "email": hospital.email,
                    "website": hospital.website,
                    "license_number": hospital.license_number,
                    "bed_strength": hospital.bed_strength,
                    "timezone": hospital.timezone
                }
            return None
        except Exception:
            return None

    def update_hospital(self, hospital_id: int, hospital_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update hospital.
        
        Args:
            hospital_id: Hospital ID
            hospital_data: Updated hospital data
            
        Returns:
            Update result
        """
        try:
            hospital = self.db.query(Hospital).filter(Hospital.id == hospital_id).first()
            
            if not hospital:
                return {"success": False, "error": "Hospital not found"}
            
            # Update fields
            for key, value in hospital_data.items():
                if hasattr(hospital, key) and value is not None:
                    setattr(hospital, key, value)
            
            self.db.commit()
            
            return {"success": True, "message": "Hospital updated successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_hospitals(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List all hospitals.
        
        Args:
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of hospitals
        """
        try:
            query = self.db.query(Hospital).filter(Hospital.is_active == True)
            total = query.count()
            hospitals = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "hospitals": [
                    {
                        "id": h.id,
                        "name": h.name,
                        "code": h.code,
                        "city": h.city,
                        "state": h.state,
                        "bed_strength": h.bed_strength,
                        "email": h.email,
                        "phone": h.phone
                    }
                    for h in hospitals
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class DepartmentController:
    """Department management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_department(self, hospital_id: int, dept_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new department.
        
        Args:
            hospital_id: Hospital ID
            dept_data: Department data
            
        Returns:
            Created department data
        """
        try:
            department = Department(
                hospital_id=hospital_id,
                name=dept_data["name"],
                code=dept_data["code"],
                description=dept_data.get("description"),
                department_type=dept_data.get("department_type"),
                head_consultant_id=dept_data.get("head_consultant_id"),
                phone=dept_data.get("phone"),
                email=dept_data.get("email")
            )
            
            self.db.add(department)
            self.db.commit()
            self.db.refresh(department)
            
            return {
                "success": True,
                "message": "Department created successfully",
                "department_id": department.id
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_departments(self, hospital_id: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List departments by hospital.
        
        Args:
            hospital_id: Hospital ID
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of departments
        """
        try:
            query = self.db.query(Department).filter(
                Department.hospital_id == hospital_id,
                Department.is_active == True
            )
            total = query.count()
            departments = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "departments": [
                    {
                        "id": d.id,
                        "name": d.name,
                        "code": d.code,
                        "description": d.description,
                        "department_type": d.department_type,
                        "phone": d.phone,
                        "email": d.email
                    }
                    for d in departments
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class FloorController:
    """Floor/Wing management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_floor(self, hospital_id: int, floor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new floor.
        
        Args:
            hospital_id: Hospital ID
            floor_data: Floor data
            
        Returns:
            Created floor data
        """
        try:
            floor = Floor(
                hospital_id=hospital_id,
                name=floor_data["name"],
                floor_number=floor_data["floor_number"],
                description=floor_data.get("description")
            )
            
            self.db.add(floor)
            self.db.commit()
            self.db.refresh(floor)
            
            return {
                "success": True,
                "message": "Floor created successfully",
                "floor_id": floor.id
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_floors(self, hospital_id: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List floors by hospital.
        
        Args:
            hospital_id: Hospital ID
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of floors
        """
        try:
            query = self.db.query(Floor).filter(
                Floor.hospital_id == hospital_id,
                Floor.is_active == True
            )
            total = query.count()
            floors = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "floors": [
                    {
                        "id": f.id,
                        "name": f.name,
                        "floor_number": f.floor_number,
                        "total_rooms": f.total_rooms,
                        "total_beds": f.total_beds
                    }
                    for f in floors
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
