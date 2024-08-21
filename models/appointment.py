from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///./test.db')

engine = create_engine(DATABASE_URI)
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    appointments = relationship('Appointment', back_populates='patient')

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    appointment_time = Column(DateTime, default=datetime.utcnow)
    details = Column(String)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', back_populates='appointments')

def init_db():
    Base.metadata.create_all(engine)

def add_new_patient(session, name):
    new_patient = Patient(name=name)
    session.add(new_patient)
    return new_patient

def add_new_appointment(session, details, patient):
    new_appointment = Appointment(details=details, patient=patient)
    session.add(new_appointment)
    return new_appointment

def print_patient_appointments(session, patient_id):
    patient_appointments = session.query(Appointment).filter_by(patient_id=patient_id).all()
    for appointment in patient_appointments:
        print(f"Appointment ID: {appointment.id}, Time: {appointment.appointment_time}, Details: {appointment.details}")

if __name__ == "__main__":
    init_db()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        new_patient = add_new_patient(session, "John Doe")
        session.commit()

        add_new_appointment(session, "General Checkup", new_patient)
        session.commit()

        print_patient_appointments(session, new_patient.id)
    
    finally:
        session.close()