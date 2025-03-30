from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    useruuid = Column(UUID(as_uuid=True), ForeignKey("users.useruuid"), primary_key=True)
    roluuid = Column(UUID(as_uuid=True), ForeignKey("roles.roluuid"), primary_key=True)

    user = relationship("User", backref="user_roles")
    role = relationship("Role", backref="user_roles")