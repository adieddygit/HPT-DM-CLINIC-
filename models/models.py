from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime
from typing import Optional
from sqlalchemy import Enum as SQLAlchemyEnum
import enum

# class UrineKetones(enum.Enum):
#     NILL = 'Nill'
#     ONE_PLUS  = '1+'
#     TWO_PLUS  = '2+'
#     THREE_PLUS = '3+'
#     NO_TEST = 'no test'

# class Choices(enum.Enum):
#     YES = 'yes'
#     NO  = 'no'
#     NA  = 'na'
#     UNKNOWN = 'unknown'

# class Purpose(enum.Enum):
#     CONSULTATION = 'Consultation'
#     HEALTH_CHECKUP  = 'Health Checkup'
#     FOLLOW_UP  = 'Follow-up'
#     OTHER = 'Other'

# class Diet(enum.Enum):
#     NORMAL = 'normal'
#     LOW_SALT  = 'low salt'
#     LOW_FAT  = 'low fat'
#     VEGETARIAN = 'vegetarian' 

# class Diagnosis(enum.Enum):
#     HPT = 'hpt'
#     DM  = 'dm'  
#     BOTH = 'both' 

# class Gender(enum.Enum):
#     MALE = 'male'
#     FEMALE  = 'female'
       

class Base(DeclarativeBase):
    pass

class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
class Role(enum.Enum):
    ADMIN = 'admin'
    CLIENT = 'client'
    CLINICAL = 'clinical'
    
class User(Base, BaseModel):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(200), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    role: Mapped[Role] = mapped_column(SQLAlchemyEnum(Role))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    
class ClientProfile(Base, BaseModel):
    __tablename__ = 'client_profile'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    created_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", ondelete="CASCADE", onupdate="CASCADE"))
    updated_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", ondelete="CASCADE", onupdate="CASCADE"))
    unique_id: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    middle_name:Mapped[Optional[str]] = mapped_column(String(100))
    last_name:Mapped[str] = mapped_column(String(100))
    dob:Mapped[datetime] = mapped_column(DateTime)
    cob:Mapped[str] = mapped_column(String(100))
    gender: Mapped[str] = mapped_column(String(100))
    marital_status:Mapped[str] = mapped_column(String(100))
    occupation:Mapped[str] = mapped_column(String(100))
    phone:Mapped[Optional[str]] = mapped_column(String(100))
    email:Mapped[Optional[str]] = mapped_column(String(100))
    address:Mapped[Optional[str]] = mapped_column(String(100))
    city:Mapped[Optional[str]] = mapped_column(String(100))
    state:Mapped[Optional[str]] = mapped_column(String(100))
    zip_code:Mapped[Optional[str]] = mapped_column(String(100))
    country:Mapped[Optional[str]] = mapped_column(String(100))
    ethnicity:Mapped[Optional[str]] = mapped_column(String(100))
    race:Mapped[Optional[str]] = mapped_column(String(100))
    emergency_contact_name:Mapped[Optional[str]] = mapped_column(String(100))
    emergency_contact_number:Mapped[Optional[str]] = mapped_column(String(100))
    emergency_contact_relation:Mapped[Optional[str]] = mapped_column(String(100))
    emergency_contact_address:Mapped[Optional[str]] = mapped_column(String(100))
   
class RiskAssessment(Base, BaseModel):
    __tablename__ = 'risk_assessment'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    created_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    updated_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id:Mapped[str] = mapped_column(String(100), ForeignKey('client_profile.unique_id', ondelete='CASCADE', onupdate='CASCADE'))
    family_has_history_of_hpt_dm:Mapped[str] = mapped_column(String(100))
    has_underlying_medical_condition:Mapped[str] = mapped_column(String(100))
    alcohol_intake:Mapped[str] = mapped_column(String(100))
    smoking_tobacco_use:Mapped[str] = mapped_column(String(100))
    type_of_diet:Mapped[str] = mapped_column(String(100))
    bmi:Mapped[str] = mapped_column(String(100))
    dose_exercise:Mapped[str] = mapped_column(String(100))

class Appointment(Base, BaseModel):
    __tablename__ = 'appointment'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    created_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    updated_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id:Mapped[str] = mapped_column(String(100), ForeignKey('client_profile.unique_id', ondelete='CASCADE', onupdate='CASCADE'))
    username:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100))
    phone:Mapped[str] = mapped_column(String(100))
    provider_type:Mapped[str] = mapped_column(String(200))
    purpose:Mapped[str] = mapped_column(String(100))
    message:Mapped[Optional[str]] = mapped_column(String(100))
    appointment_date:Mapped[datetime] = mapped_column(DateTime)
    appointment_time:Mapped[datetime] = mapped_column(DateTime)
    appointment_status:Mapped[str] = mapped_column(String(200))
    last_appointment_date:Mapped[datetime] = mapped_column(DateTime, default=func.now())


class HealthMetrics(Base, BaseModel):
    __tablename__ = 'health_metrics'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    created_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    updated_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id:Mapped[str] = mapped_column(String(100), ForeignKey('client_profile.unique_id', ondelete='CASCADE', onupdate='CASCADE'))
    recorded_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    health_care_facility:Mapped[str] = mapped_column(String(100))
    provider_name:Mapped[str] = mapped_column(String(100))
    provider_contact:Mapped[str] = mapped_column(String(100))
    weight:Mapped[str] = mapped_column(String(100))
    height:Mapped[str] = mapped_column(String(100))
    blood_pressure:Mapped[str] = mapped_column(String(100))
    blood_suger:Mapped[str] = mapped_column(String(100))
    temperature:Mapped[str] = mapped_column(String(100))
    respiration:Mapped[str] = mapped_column(String(100))
    pulse:Mapped[str] = mapped_column(String(100))
    spo2:Mapped[str] = mapped_column(String(100))
    urine_ketones: Mapped[str] = mapped_column(String(100))
    lab_investigation_type:Mapped[Optional[str]] = mapped_column(String(100))
    lab_investigation_result_:Mapped[Optional[str]] = mapped_column(String(100)) 
    radiograph_investigation_type:Mapped[Optional[str]] = mapped_column(String(100))
    radiograph_investigation_result:Mapped[Optional[str]] = mapped_column(String(255))
    metric_notes:Mapped[Optional[str]] = mapped_column(String(255))
    heart_conditions:Mapped[str] = mapped_column(String(255))
    diagnosis:Mapped[str] = mapped_column(String(100))    
    hospitalized_for_hpt_dm:Mapped[str] = mapped_column(String(100))
    complications:Mapped[str] = mapped_column(String(100))
    

class Treatment(Base, BaseModel):
    __tablename__ = 'treatment'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    created_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    updated_by: Mapped[str] = mapped_column(String(200), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id:Mapped[str] = mapped_column(String(100), ForeignKey('client_profile.unique_id', ondelete='CASCADE', onupdate='CASCADE'))
    date_of_treatment:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    treatment_type:Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    defaulted_treatment:Mapped[str] = mapped_column(String(100))
    health_care_facility:Mapped[Optional[str]] = mapped_column(String(100))
    provider_type:Mapped[Optional[str]] = mapped_column(String(100))
    provider_contact:Mapped[Optional[str]] = mapped_column(String(100))
    treatment_plan:Mapped[Optional[str]] = mapped_column(String(100))
    treatment_notes:Mapped[Optional[str]] = mapped_column(String(255))  