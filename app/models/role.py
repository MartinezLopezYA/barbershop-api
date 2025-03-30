import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.database import Base

class Role(Base):
    __tablename__ = "roles"

    roluuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rolname = Column(String(50), unique=True, index=True, nullable=False)
    roldesc = Column(String(80), nullable=True)
    rolstatus = Column(Boolean, default=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")