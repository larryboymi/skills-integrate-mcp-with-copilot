"""Seed the SQLite database with initial activities."""
from src.db import engine, Base, SessionLocal
from src.models import Activity, Participant


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(Participant).delete()
    db.query(Activity).delete()
    db.commit()

    activities = [
        Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments",
                 schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12),
        Activity(name="Programming Class", description="Learn programming fundamentals and build software projects",
                 schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20),
        Activity(name="Gym Class", description="Physical education and sports activities",
                 schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30),
    ]

    db.add_all(activities)
    db.commit()

    # Add a sample participant to Chess Club
    chess = db.query(Activity).filter(Activity.name == "Chess Club").first()
    p = Participant(activity_id=chess.id, email="michael@mergington.edu")
    db.add(p)
    db.commit()
    db.close()


if __name__ == "__main__":
    seed()
    print("Seeded database.")
