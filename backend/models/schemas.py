"""Pydantic schemas for API serialization and database models."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from backend.models.database import Base


# ==================== Database Models ====================

class Client(Base):
    """Client database model."""
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    company_name = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default=dict)
    
    campaigns = relationship("Campaign", back_populates="client")
    tasks = relationship("Task", back_populates="client")


class Campaign(Base):
    """Campaign database model."""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    name = Column(String(255), nullable=False)
    campaign_type = Column(String(100))
    budget = Column(Float)
    status = Column(String(50), default="draft")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    objectives = Column(JSON, default=list)
    channels = Column(JSON, default=list)
    target_audience = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, default=dict)
    
    client = relationship("Client", back_populates="campaigns")
    tasks = relationship("Task", back_populates="campaign")


class Task(Base):
    """Task/Job database model."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    agent_type = Column(String(100), nullable=False)
    status = Column(String(50), default="pending")
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    
    client = relationship("Client", back_populates="tasks")
    campaign = relationship("Campaign", back_populates="tasks")


class AgentExecution(Base):
    """Agent execution log database model."""
    __tablename__ = "agent_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String(100), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    execution_time_ms = Column(Integer)
    token_usage = Column(JSON, default=dict)
    status = Column(String(50), default="completed")
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalyticsData(Base):
    """Analytics data database model."""
    __tablename__ = "analytics_data"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    source = Column(String(100))
    date = Column(DateTime, nullable=False)
    metrics = Column(JSON, default=dict)
    dimensions = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        {"comment": "Stores aggregated analytics data"}
    )


# ==================== Pydantic Schemas ====================

class ClientBase(BaseModel):
    """Base client schema."""
    name: str
    email: EmailStr
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class ClientCreate(ClientBase):
    """Client creation schema."""
    pass


class ClientUpdate(BaseModel):
    """Client update schema."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class ClientResponse(ClientBase):
    """Client response schema."""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class CampaignBase(BaseModel):
    """Base campaign schema."""
    name: str
    campaign_type: Optional[str] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    objectives: List[str] = Field(default_factory=list)
    channels: List[str] = Field(default_factory=list)
    target_audience: Dict[str, Any] = Field(default_factory=dict)


class CampaignCreate(CampaignBase):
    """Campaign creation schema."""
    client_id: int


class CampaignResponse(CampaignBase):
    """Campaign response schema."""
    id: int
    client_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """Base task schema."""
    agent_type: str
    input_data: Dict[str, Any] = Field(default_factory=dict)


class TaskCreate(TaskBase):
    """Task creation schema."""
    client_id: Optional[int] = None
    campaign_id: Optional[int] = None


class TaskResponse(TaskBase):
    """Task response schema."""
    id: int
    client_id: Optional[int]
    campaign_id: Optional[int]
    status: str
    output_data: Dict[str, Any]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AgentExecutionResponse(BaseModel):
    """Agent execution response schema."""
    id: int
    agent_type: str
    task_id: Optional[int]
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    execution_time_ms: Optional[int]
    token_usage: Dict[str, Any]
    status: str
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
