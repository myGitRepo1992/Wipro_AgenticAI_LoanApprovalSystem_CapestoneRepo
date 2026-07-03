from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, JSON
from datetime import datetime
import os

DATABASE_URL = "sqlite:///./loan_applications.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ApplicationRecord(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, index=True)
    applicant_id = Column(String, index=True)
    applicant_name = Column(String)
    applicant_email = Column(String)
    annual_income = Column(Float)
    credit_score = Column(Integer)
    loan_amount = Column(Float)
    employment_type = Column(String)
    employment_years = Column(Integer)
    existing_debt = Column(Float)
    loan_tenure = Column(Integer)
    location = Column(String)
    applicant_profile = Column(JSON)
    financial_risk = Column(JSON)
    loan_decision = Column(JSON)
    compliance_action = Column(JSON)
    overall_reasoning = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ApplicantCacheRecord(Base):
    __tablename__ = "applicant_cache"

    id = Column(String, primary_key=True, index=True)
    applicant_id = Column(String, unique=True, index=True)
    income_stability_score = Column(Float)
    employment_risk = Column(String)
    credit_history_summary = Column(Text)
    application_completeness_flags = Column(JSON)
    cached_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RiskAssessmentRecord(Base):
    __tablename__ = "risk_assessments"

    id = Column(String, primary_key=True, index=True)
    applicant_id = Column(String, index=True)
    debt_to_income_ratio = Column(Float)
    credit_score_risk_level = Column(String)
    loan_amount_risk = Column(String)
    anomaly_detection = Column(JSON)
    reasoning = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class DecisionRecord(Base):
    __tablename__ = "decisions"

    id = Column(String, primary_key=True, index=True)
    applicant_id = Column(String, index=True)
    classification = Column(String)
    risk_score = Column(Float)
    confidence_level = Column(Float)
    key_decision_factors = Column(JSON)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class NotificationRecord(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True)
    applicant_id = Column(String, index=True)
    action_taken = Column(String)
    notification_sent = Column(String)
    summary = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
