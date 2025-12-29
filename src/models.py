from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    schedule = Column(String, nullable=True)
    max_participants = Column(Integer, default=30)
    image_url = Column(String, nullable=True)
    price = Column(String, nullable=True)

    participants = relationship("Participant", back_populates="activity", cascade="all, delete-orphan")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    email = Column(String, index=True, nullable=False)
    name = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    college = Column(String, nullable=True)
    branch = Column(String, nullable=True)

    activity = relationship("Activity", back_populates="participants")
