import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    useruuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    userpass = Column(String, nullable=False)  # Se guardará como hash
    useremail = Column(String(80), unique=True, index=True, nullable=False)
    userfirstname = Column(String(50), nullable=False)
    userlastname = Column(String(50), nullable=False)
    userphone = Column(String(10), nullable=True)
    userstatus = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())