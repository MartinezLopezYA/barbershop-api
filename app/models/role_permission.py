from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.database import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"

    roluuid = Column(UUID(as_uuid=True), ForeignKey("roles.roluuid"), primary_key=True)
    permissionuuid = Column(UUID(as_uuid=True), ForeignKey("permissions.permissionuuid"), primary_key=True)

    role = relationship("Role", back_populates="role_permissions", overlaps="permissions,roles")
    permission = relationship("Permission", back_populates="role_permissions", overlaps="permissions,roles")