from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import datetime
import uuid

import database
from database import SessionLocal, Student, FoodMenu, NGO, WasteLog

import os
from pathlib import Path

app = FastAPI(title="EcoMeal AI Backend", description="Local backend for EcoMeal without AWS SAM")

BASE_DIR = Path(__file__).resolve().parent

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = BASE_DIR / "templates" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/student", response_class=HTMLResponse)
def read_student():
    html_path = BASE_DIR / "templates" / "student.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------
# Pydantic Models
# -----------------
class PollDispatchRequest(BaseModel):
    meal_id: str

class PollRespondRequest(BaseModel):
    student_id: str
    meal_id: str
    response: str # EATING or SKIPPING

class NGODispatchRequest(BaseModel):
    hostel_id: str = "Main_Campus_Hostel"
    uploaded_by: str = "Manager"
    meal_type: str
    food_category: str = "Cooked Meals"
    portions: int
    packaging_status: str = "Unpackaged"
    menu_items: str
    cook_time: str
    expiration_timestamp: str

# -----------------
# Utility: Mock Messaging
# -----------------
def mock_send_message(message: str, subject: str = "Alert"):
    print("\n" + "="*50)
    print(f"📡 MOCK MESSAGE SENT: {subject}")
    print("-" * 50)
    print(message)
    print("="*50 + "\n")

# -----------------
# Endpoints
# -----------------

class FlashClaimRequest(BaseModel):
    meal_id: str
    student_id: str

@app.get("/kitchen/predict")
def predictive_portioning(meal_id: str, db: Session = Depends(get_db)):
    # Count students opting to eat (or defaulting to EATING)
    eating_count = db.query(Student).filter(Student.latest_response == "EATING").count()
    skipping_count = db.query(Student).filter(Student.latest_response == "SKIPPING").count()
    
    # Safety buffer of 5%
    safety_buffer = 0.05
    total_portions_to_cook = int(eating_count * (1 + safety_buffer))
    
    return {
        "status": "PREP_DIRECTIVE_ISSUED",
        "meal_id": meal_id,
        "attendance_metrics": {
            "explicit_eating_and_defaults": eating_count,
            "explicit_skips": skipping_count
        },
        "kitchen_instructions": {
            "safety_buffer_percentage": safety_buffer * 100,
            "total_portions_to_cook": total_portions_to_cook
        },
        "instruction": f"Cook strictly for {total_portions_to_cook} portions."
    }

@app.post("/flash-claim/dispatch")
def flash_claim_dispatch(request: NGODispatchRequest, db: Session = Depends(get_db)):
    # This happens BEFORE NGO dispatch.
    # It sends an alert to campus students for discounted/free surplus.
    
    alert_broadcast = (
        f"🚨 **CAMPUS FLASH CLAIM** 🚨\n"
        f"Surplus {request.meal_type} available at {request.hostel_id}!\n"
        f"Food: {request.food_category} ({request.menu_items})\n"
        f"Portions available: {request.portions}\n"
        f"Cost: ZERO\n"
        f"Window: NEXT 30 MINUTES ONLY!"
    )
    
    mock_send_message(alert_broadcast, "Tier 1 Flash Claim")
    
    return {
        "status": "FLASH_CLAIM_TRIGGERED",
        "broadcast_preview": alert_broadcast
    }
@app.post("/poll/dispatch")
def dispatch_poll(request: PollDispatchRequest, db: Session = Depends(get_db)):
    menu = db.query(FoodMenu).filter(FoodMenu.meal_id == request.meal_id).first()
    menu_desc = menu.menu_description if menu else "Standard Meal"
    
    message = (
        f"🔔 EcoMeal Alert: {request.meal_id}\n"
        f"Menu: {menu_desc}\n\n"
        f"Will you be eating in the mess? Reply [EATING] or [SKIPPING].\n"
        f"Note: Default is EATING if no reply by cutoff."
    )
    
    mock_send_message(message, f"Poll for {request.meal_id}")
    
    return {
        "status": "POLL_DISPATCHED",
        "meal_id": request.meal_id,
        "message_preview": message
    }

@app.post("/poll/respond")
def process_response(request: PollRespondRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    student.latest_meal_id = request.meal_id
    student.latest_response = request.response
    db.commit()
    
    return {
        "status": "RESPONSE_RECORDED",
        "student_id": request.student_id,
        "meal_id": request.meal_id,
        "response": request.response
    }

@app.post("/ngo/dispatch")
def ngo_dispatch(request: NGODispatchRequest, db: Session = Depends(get_db)):
    if request.portions <= 0:
        raise HTTPException(status_code=400, detail="Portions must be greater than 0")
        
    # Sustainability Metrics
    total_surplus_diverted_kg = round(request.portions * 0.35, 1)
    co2_saved_kg = round(total_surplus_diverted_kg * 2.26, 1)
    
    log_time = datetime.datetime.now().strftime("%I:%M %p")
    record_id = str(uuid.uuid4())
    
    # Log to DB
    new_log = WasteLog(
        record_id=record_id,
        hostel_id=request.hostel_id,
        uploaded_by=request.uploaded_by,
        meal_type=request.meal_type,
        portions_diverted=request.portions,
        co2_saved_kg=co2_saved_kg,
        log_time=log_time
    )
    db.add(new_log)
    db.commit()
    
    alert_broadcast = (
        f"🚨 **URGENT: FOOD RESCUE DISPATCH** 🚨\n"
        f"**From:** EcoMeal AI ({request.uploaded_by})\n\n"
        f"**Location & Gate Access:** {request.hostel_id}\n\n"
        f"📦 **Inventory Details:**\n"
        f"- **Food Category:** {request.food_category} ({request.menu_items})\n"
        f"- **Portion Count:** ~{request.portions} portions\n"
        f"- **Packaging Status:** {request.packaging_status}\n\n"
        f"⏳ **Food Safety Window:**\n"
        f"- **Cook Time:** {request.cook_time}\n"
        f"- **Log Time:** {log_time}\n"
        f"- **Expiration Timestamp:** STRICTLY {request.expiration_timestamp}\n\n"
        f"🌱 **Sustainability Impact:**\n"
        f"- **Waste Diverted:** {total_surplus_diverted_kg} kg\n"
        f"- **CO2 Saved:** {co2_saved_kg} kg CO2e\n\n"
        f"Reply 'CLAIM' to accept."
    )
    
    mock_send_message(alert_broadcast, "Food Rescue Dispatch")
    
    return {
        "status": "NGO_DISPATCH_TRIGGERED",
        "record_id": record_id,
        "broadcast_preview": alert_broadcast
    }
