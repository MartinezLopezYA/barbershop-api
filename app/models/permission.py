import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    permissionuuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permissionname = Column(String(50), unique=True, index=True, nullable=False)
    permissiondesc = Column(String(80), nullable=True)

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions", overlaps="role_permissions")
    role_permissions = relationship("RolePermission", back_populates="permission", overlaps="permissions")