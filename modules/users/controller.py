"""User management controllers."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.user import User, UserRole, UserPermission
from utils.auth import hash_password, verify_password, create_token
from datetime import datetime


class UserController:
    """User management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new user.
        
        Args:
            user_data: User data dictionary
            
        Returns:
            Created user data
        """
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(
                (User.username == user_data["username"]) |
                (User.email == user_data["email"])
            ).first()
            
            if existing_user:
                return {
                    "success": False,
                    "error": "User with this username or email already exists"
                }
            
            # Hash password
            password_hash = hash_password(user_data["password"])
            
            # Create user
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=password_hash,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data.get("phone"),
                role=UserRole[user_data["role"].upper()],
                hospital_id=user_data.get("hospital_id"),
                is_verified=False
            )
            
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            
            return {
                "success": True,
                "message": "User created successfully",
                "user_id": new_user.id,
                "username": new_user.username
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            Authentication result with token
        """
        try:
            user = self.db.query(User).filter(User.username == username).first()
            
            if not user:
                return {"success": False, "error": "Invalid username or password"}
            
            if user.is_locked:
                return {"success": False, "error": "User account is locked"}
            
            if not verify_password(password, user.password_hash):
                return {"success": False, "error": "Invalid username or password"}
            
            # Create token
            token = create_token(
                user.id,
                {
                    "username": user.username,
                    "role": user.role.value,
                    "hospital_id": user.hospital_id
                }
            )
            
            # Update last login
            user.last_login = datetime.utcnow()
            self.db.commit()
            
            return {
                "success": True,
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
                "role": user.role.value,
                "hospital_id": user.hospital_id,
                "token": token
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User data or None
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "role": user.role.value,
                    "hospital_id": user.hospital_id,
                    "is_verified": user.is_verified,
                    "is_locked": user.is_locked,
                    "last_login": user.last_login
                }
            return None
        except Exception:
            return None

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user.
        
        Args:
            user_id: User ID
            user_data: Updated user data
            
        Returns:
            Update result
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Update fields
            if "first_name" in user_data:
                user.first_name = user_data["first_name"]
            if "last_name" in user_data:
                user.last_name = user_data["last_name"]
            if "phone" in user_data:
                user.phone = user_data["phone"]
            if "email" in user_data:
                user.email = user_data["email"]
            if "role" in user_data:
                user.role = UserRole[user_data["role"].upper()]
            
            self.db.commit()
            
            return {"success": True, "message": "User updated successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password.
        
        Args:
            user_id: User ID
            old_password: Old password
            new_password: New password
            
        Returns:
            Change password result
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            if not verify_password(old_password, user.password_hash):
                return {"success": False, "error": "Current password is incorrect"}
            
            user.password_hash = hash_password(new_password)
            user.password_changed_at = datetime.utcnow()
            self.db.commit()
            
            return {"success": True, "message": "Password changed successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def reset_password(self, user_id: int, new_password: str) -> Dict[str, Any]:
        """Reset user password (admin function).
        
        Args:
            user_id: User ID
            new_password: New password
            
        Returns:
            Reset password result
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            user.password_hash = hash_password(new_password)
            user.password_changed_at = datetime.utcnow()
            self.db.commit()
            
            return {"success": True, "message": "Password reset successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_users(self, hospital_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List users.
        
        Args:
            hospital_id: Filter by hospital ID
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of users
        """
        try:
            query = self.db.query(User).filter(User.is_active == True)
            
            if hospital_id:
                query = query.filter(User.hospital_id == hospital_id)
            
            total = query.count()
            users = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "users": [
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role.value,
                        "hospital_id": user.hospital_id,
                        "is_verified": user.is_verified
                    }
                    for user in users
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_user_permissions(self, user_id: int, permissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Set user permissions.
        
        Args:
            user_id: User ID
            permissions: List of permission dictionaries
            
        Returns:
            Permission setting result
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Clear existing permissions
            self.db.query(UserPermission).filter(UserPermission.user_id == user_id).delete()
            
            # Add new permissions
            for perm in permissions:
                new_perm = UserPermission(
                    user_id=user_id,
                    permission_name=perm["permission_name"],
                    resource_type=perm.get("resource_type"),
                    can_create=perm.get("can_create", False),
                    can_read=perm.get("can_read", False),
                    can_update=perm.get("can_update", False),
                    can_delete=perm.get("can_delete", False),
                    can_export=perm.get("can_export", False)
                )
                self.db.add(new_perm)
            
            self.db.commit()
            
            return {"success": True, "message": "Permissions updated successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def deactivate_user(self, user_id: int) -> Dict[str, Any]:
        """Deactivate user.
        
        Args:
            user_id: User ID
            
        Returns:
            Deactivation result
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            user.is_active = False
            self.db.commit()
            
            return {"success": True, "message": "User deactivated successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def lock_user(self, user_id: int) -> Dict[str, Any]:
        """Lock user account.
        
        Args:
            user_id: User ID
            
        Returns:
            Lock result
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            user.is_locked = True
            self.db.commit()
            
            return {"success": True, "message": "User locked successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def unlock_user(self, user_id: int) -> Dict[str, Any]:
        """Unlock user account.
        
        Args:
            user_id: User ID
            
        Returns:
            Unlock result
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            user.is_locked = False
            self.db.commit()
            
            return {"success": True, "message": "User unlocked successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}
