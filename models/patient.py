from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column,scoped_session, sessionmaker, relationship, Mapped
from datetime import datetime
from typing import Optional
from sqlalchemy import Enum as SQLAlchemyEnum
import enum

class UrineKetones(enum.Enum):
    NILL = 'Nill'
    ONE_PLUS  = '1+'
    TWO_PLUS  = '2+'
    THREE_PLUS = '3+'
    NO_TEST = 'no test'

class Choices(enum.Enum):
    YES = 'yes'
    NO  = 'no'
    NA  = 'na'
    UNKNOWN = 'unknown'

class Diet(enum.Enum):
    NORMAL = 'normal'
    LOW_SALT  = 'low salt'
    LOW_FAT  = 'low fat'
    VEGETARIAN = 'vegetarian' 

class Diagnosis(enum.Enum):
    HPT = 'hpt'
    DM  = 'dm'  
    BOTH = 'both' 

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE  = 'female'
       

class Base(DeclarativeBase):
    pass

class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    
class Role(enum.Enum):
    ADMIN = 'admin'
    CLIENT = 'client'
    CLINICAL = 'clinical'
    
class Users(Base, BaseModel):
    __tablename__ = 'users'
    username:Mapped[str] = mapped_column(String(200))
    email:Mapped[str] = mapped_column(String(100), unique=True)
    password:Mapped[str] = mapped_column(String(200))
    role:Mapped[Role] = mapped_column(SQLAlchemyEnum(Role))
    created_at:Mapped[str] = mapped_column(DateTime, default=func.now())

    
class PatientReg(Base, BaseModel):
    __tablename__ = 'patient_reg'
    created_by:Mapped[str] = mapped_column(String(200))
    upated_by:Mapped[str] = mapped_column(String(200))
    patient_id:Mapped[str] = mapped_column(String(100), unique=True)
    first_name:Mapped[str] = mapped_column(String(100))
    middle_name:Mapped[str] = mapped_column(String(100))
    last_name:Mapped[str] = mapped_column(String(100))
    date_of_birth:Mapped[datetime] = mapped_column(DateTime)
    country_of_birth:Mapped[str] = mapped_column(String(100))
    gender: Mapped[Gender] = mapped_column(SQLAlchemyEnum(Gender))
    marital_status:Mapped[str] = mapped_column(String(100))
    occupation:Mapped[str] = mapped_column(String(100))
    phone_number:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    city:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    zip_code:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ethnicity:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emergency_contact_name:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emergency_contact_number:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emergency_contact_ralation:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emergency_contact_address:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    health_metrics = relationship("PatientHealthMetrics", backref="patient", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", backref="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", backref="patient", cascade="all, delete-orphan")

class RiskAssessment(Base, BaseModel):
    __tablename__ = 'risk_assessment'
    patient_id:Mapped[str] = mapped_column(String(100), ForeignKey('patient_reg.patient_id', ondelete='CASCADE', onupdate='CASCADE'))
    family_has_history_of_hpt_dm:Mapped[str] = mapped_column(String(100))
    has_underlying_medical_condition:Mapped[str] = mapped_column(String(100))
    heavy_alcohol_intake:Mapped[str] = mapped_column(String(100))
    smoking_tobacco_use:Mapped[str] = mapped_column(String(100))
    type_of_diet:Mapped[str] = mapped_column(String(100))
    overweight_obese:Mapped[str] = mapped_column(String(100))
    dose_exercise:Mapped[str] = mapped_column(String(100))

class Appointment(Base, BaseModel):
    __tablename__ = 'appointment'
    patient_id:Mapped[str] = mapped_column(String(100), ForeignKey('patient_reg.patient_id', ondelete='CASCADE', onupdate='CASCADE'))
    provider_id:Mapped[str] = mapped_column(String(200))
    appointment_date:Mapped[datetime] = mapped_column(DateTime)
    appointment_status:Mapped[str] = mapped_column(String(200))
    last_appointment_date:Mapped[datetime] = mapped_column(DateTime, default=func.now())

class PatientHealthMetrics(Base, BaseModel):
    __tablename__ = 'patient_health_metrics'
    patient_id:Mapped[str] = mapped_column(String(100), ForeignKey('patient_reg.patient_id', ondelete='CASCADE', onupdate='CASCADE'))
    recorded_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    health_care_facility:Mapped[str] = mapped_column(String(100))
    provider_name:Mapped[str] = mapped_column(String(100))
    provider_contact:Mapped[str] = mapped_column(String(100))
    weight:Mapped[int] = mapped_column(Integer())
    height:Mapped[int] = mapped_column(Integer())
    blood_pressure:Mapped[int] = mapped_column(Integer())
    blood_suger:Mapped[int] = mapped_column(Integer())
    temperature:Mapped[int] = mapped_column(Integer())
    respiration:Mapped[int] = mapped_column(Integer())
    pulse:Mapped[int] = mapped_column(Integer())
    spo2:Mapped[int] = mapped_column(Integer())
    urine_ketones: Mapped[UrineKetones] = mapped_column(SQLAlchemyEnum(UrineKetones))
    lab_investigation_type:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    lab_investigation_result:Mapped[Optional[str]] = mapped_column(String(100), nullable=True) 
    radiograph_investigation_type:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    radiograph_investigation_result:Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metric_notes:Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    heart_conditions:Mapped[str] = mapped_column(String(255))
    diagnosis: Mapped[Diagnosis] = mapped_column(SQLAlchemyEnum(Diagnosis))    
    hospitalized_for_hpt_dm:Mapped[Choices] = mapped_column(SQLAlchemyEnum(Choices))
    complications:Mapped[Choices] = mapped_column(SQLAlchemyEnum(Choices))
    complications_type:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

class PatientTreatment(Base, BaseModel):
    __tablename__ = 'patient_treatment'
    patient_id:Mapped[str] = mapped_column(String(100), ForeignKey('patient_reg.patient_id', ondelete='CASCADE', onupdate='CASCADE'))
    date_of_treatment:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    treatment_type:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    defaulted_treatment:Mapped[Choices] = mapped_column(SQLAlchemyEnum(Choices))
    health_care_facility:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    provider_name:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    provider_contact:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    treatment_plan:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    treatment_notes:Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
   