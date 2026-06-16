"""Service management controllers."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.service import Service, SubService, ServiceRate, Package, PackageItem, PackageRate, ServiceCategory
from models.consultant import ConsultationCharge
from datetime import datetime
from decimal import Decimal


class ServiceController:
    """Service management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_service(self, hospital_id: int, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new service.
        
        Args:
            hospital_id: Hospital ID
            service_data: Service data dictionary
            
        Returns:
            Created service data
        """
        try:
            service = Service(
                hospital_id=hospital_id,
                name=service_data["name"],
                code=service_data["code"],
                category=ServiceCategory[service_data["category"].upper()],
                description=service_data.get("description"),
                hsncode=service_data.get("hsncode"),
                icd_code=service_data.get("icd_code"),
                is_billable=service_data.get("is_billable", True),
                requires_approval=service_data.get("requires_approval", False)
            )
            
            self.db.add(service)
            self.db.commit()
            self.db.refresh(service)
            
            return {
                "success": True,
                "message": "Service created successfully",
                "service_id": service.id
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def create_sub_service(self, service_id: int, sub_service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create sub-service.
        
        Args:
            service_id: Service ID
            sub_service_data: Sub-service data
            
        Returns:
            Created sub-service data
        """
        try:
            sub_service = SubService(
                service_id=service_id,
                name=sub_service_data["name"],
                code=sub_service_data["code"],
                description=sub_service_data.get("description"),
                is_billable=sub_service_data.get("is_billable", True)
            )
            
            self.db.add(sub_service)
            self.db.commit()
            self.db.refresh(sub_service)
            
            return {
                "success": True,
                "message": "Sub-service created successfully",
                "sub_service_id": sub_service.id
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def set_service_rate(self, service_id: int, rate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Set service rate for panel/billing type.
        
        Args:
            service_id: Service ID
            rate_data: Rate data
            
        Returns:
            Result
        """
        try:
            rate = ServiceRate(
                service_id=service_id,
                sub_service_id=rate_data.get("sub_service_id"),
                panel_id=rate_data.get("panel_id"),
                rate_type=rate_data["rate_type"],
                amount=Decimal(str(rate_data["amount"])),
                is_negotiable=rate_data.get("is_negotiable", False)
            )
            
            self.db.add(rate)
            self.db.commit()
            
            return {"success": True, "message": "Service rate set successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def get_service_rate(self, service_id: int, panel_id: Optional[int] = None, rate_type: str = "cash") -> Optional[Dict[str, Any]]:
        """Get service rate.
        
        Args:
            service_id: Service ID
            panel_id: Panel ID (None for cash)
            rate_type: Rate type
            
        Returns:
            Service rate or None
        """
        try:
            query = self.db.query(ServiceRate).filter(
                ServiceRate.service_id == service_id,
                ServiceRate.rate_type == rate_type
            )
            
            if panel_id:
                query = query.filter(ServiceRate.panel_id == panel_id)
            else:
                query = query.filter(ServiceRate.panel_id.is_(None))
            
            rate = query.first()
            if rate:
                return {
                    "service_id": rate.service_id,
                    "rate_type": rate.rate_type,
                    "amount": float(rate.amount),
                    "is_negotiable": rate.is_negotiable
                }
            return None
        except Exception:
            return None

    def list_services(self, hospital_id: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List services.
        
        Args:
            hospital_id: Hospital ID
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of services
        """
        try:
            query = self.db.query(Service).filter(
                Service.hospital_id == hospital_id,
                Service.is_active == True
            )
            total = query.count()
            services = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "services": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "code": s.code,
                        "category": s.category.value,
                        "is_billable": s.is_billable
                    }
                    for s in services
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class PackageController:
    """Package management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_package(self, hospital_id: int, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new package.
        
        Args:
            hospital_id: Hospital ID
            package_data: Package data
            
        Returns:
            Created package data
        """
        try:
            package = Package(
                hospital_id=hospital_id,
                name=package_data["name"],
                code=package_data["code"],
                description=package_data.get("description"),
                category=package_data.get("category"),
                base_price=Decimal(str(package_data["base_price"])),
                discount_percentage=Decimal(str(package_data.get("discount_percentage", 0))),
                number_of_days=package_data.get("number_of_days")
            )
            
            self.db.add(package)
            self.db.commit()
            self.db.refresh(package)
            
            # Add package items
            for item in package_data.get("items", []):
                package_item = PackageItem(
                    package_id=package.id,
                    service_id=item["service_id"],
                    quantity=item.get("quantity", 1),
                    sequence=item.get("sequence")
                )
                self.db.add(package_item)
            
            self.db.commit()
            
            return {
                "success": True,
                "message": "Package created successfully",
                "package_id": package.id
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def set_package_rate(self, package_id: int, rate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Set package rate for panel/billing type.
        
        Args:
            package_id: Package ID
            rate_data: Rate data
            
        Returns:
            Result
        """
        try:
            rate = PackageRate(
                package_id=package_id,
                panel_id=rate_data.get("panel_id"),
                rate_type=rate_data["rate_type"],
                amount=Decimal(str(rate_data["amount"]))
            )
            
            self.db.add(rate)
            self.db.commit()
            
            return {"success": True, "message": "Package rate set successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_packages(self, hospital_id: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List packages.
        
        Args:
            hospital_id: Hospital ID
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of packages
        """
        try:
            query = self.db.query(Package).filter(
                Package.hospital_id == hospital_id,
                Package.is_active == True
            )
            total = query.count()
            packages = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "packages": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "code": p.code,
                        "base_price": float(p.base_price),
                        "discount_percentage": float(p.discount_percentage),
                        "category": p.category
                    }
                    for p in packages
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
