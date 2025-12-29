"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.orm import Session
import os
from pathlib import Path

from .db import SessionLocal, engine, Base
from .models import Activity, Participant

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Return activities with their participants"""
    activities = db.query(Activity).all()
    result = {}
    for a in activities:
        result[a.name] = {
            "description": a.description,
            "schedule": a.schedule,
            "max_participants": a.max_participants,
            "participants": [p.email for p in a.participants]
        }
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if already signed up
    existing = db.query(Participant).filter(Participant.activity_id == activity.id, Participant.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Check capacity
    count = db.query(Participant).filter(Participant.activity_id == activity.id).count()
    if count >= activity.max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    participant = Participant(activity_id=activity.id, email=email)
    db.add(participant)
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    participant = db.query(Participant).filter(Participant.activity_id == activity.id, Participant.email == email).first()
    if not participant:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    db.delete(participant)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}
