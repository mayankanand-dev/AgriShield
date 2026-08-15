import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

from db.session import Base
import enum

class FarmStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    UNAVAILABLE = "UNAVAILABLE"

class PolicyStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    language = Column(String, default="hi")
    hashed_password = Column(String)
    
    farms = relationship("Farm", back_populates="owner")

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String, nullable=False)
    crop = Column(String, nullable=True)
    sowing_date = Column(DateTime, nullable=True)
    area_m2 = Column(Float)
    
    # PostGIS Polygon column
    boundary = Column(Geometry(geometry_type='POLYGON', srid=4326))
    
    status = Column(SQLEnum(FarmStatus), default=FarmStatus.PENDING)
    
    owner = relationship("User", back_populates="farms")
    claims = relationship("Claim", back_populates="farm")

class ClaimStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    AI_ASSESSED = "AI_ASSESSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id"))
    policy_id = Column(UUID(as_uuid=True)) # Simulating policy linking
    incident_date = Column(DateTime)
    event_type = Column(String)
    description = Column(Text)
    status = Column(SQLEnum(ClaimStatus), default=ClaimStatus.SUBMITTED)
    damage_pct = Column(Float, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    canonical_hash = Column(String, nullable=True)
    tx_hash = Column(String, nullable=True)
    
    farm = relationship("Farm", back_populates="claims")

class InsurancePolicy(Base):
    __tablename__ = "insurance_policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id"))
    
    premium_amount = Column(Float)
    coverage_amount = Column(Float)
    
    canonical_hash = Column(String, nullable=True)
    tx_hash = Column(String, nullable=True)
    
    status = Column(SQLEnum(PolicyStatus), default=PolicyStatus.ACTIVE)
    
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User")
    farm = relationship("Farm")
