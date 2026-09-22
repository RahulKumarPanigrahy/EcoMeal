from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./ecomeal.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)
    preference = Column(String) # Veg or Non-Veg
    latest_meal_id = Column(String, nullable=True)
    latest_response = Column(String, default="EATING")

class FoodMenu(Base):
    __tablename__ = "food_menu"
    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(String, unique=True, index=True) # e.g. WED-DINNER
    day_of_week = Column(String)
    meal_type = Column(String) # Breakfast, Lunch, Snacks, Dinner
    menu_description = Column(String)

class NGO(Base):
    __tablename__ = "ngos"
    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(String, unique=True, index=True)
    name = Column(String)
    contact_person = Column(String)
    phone_number = Column(String)

class WasteLog(Base):
    __tablename__ = "waste_logs"
    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String, unique=True, index=True)
    hostel_id = Column(String)
    uploaded_by = Column(String)
    meal_type = Column(String)
    portions_diverted = Column(Integer)
    co2_saved_kg = Column(Float)
    log_time = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)
