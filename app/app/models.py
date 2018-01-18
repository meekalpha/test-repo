from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base

class TimeSlot(Base):
    __tablename__ = 'timeslots'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    duration = Column(Integer)
    available = Column(Boolean)
    room_id  = Column(String(10))
    title = Column(String(999))

    def __init__(self, startTime, duration, available, title, room_id):
        self.start_time = startTime
        self.duration = duration
        self.available = available
        self.room_id = room_id
        self.title = title

    def update_from(self, timeslot):
        self.start_time = timeslot.start_time
        self.duration = timeslot.duration
        self.available = timeslot.available
        self.room_id = timeslot.room_id
        self.title = timeslot.title

    def __str__(self):
        return '{} {} {} {}'.format(self.start_time, self.duration, self.available, self.room_id)
