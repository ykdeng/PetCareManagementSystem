from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

# Setup database URI with fallback to local SQLite if not specified
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///./test.db')

# Create engine and base
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Define Patient model
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    appointments = relationship('Appointment', back_populates='patient')

# Define Appointment model
class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    appointment_time = Column(DateTime, default=datetime.utcnow)
    details = Column(String)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', back_populates='appointments')

# Initialize the database
def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    
    # Create a session
    with sessionmaker(bind=engine)() as session:
        new_patient = Patient(name="John Doe")
        session.add(new_patient)
        session.commit()  # Committing after each transaction can be optimized as needed

        new_appointment = Appointment(details="General Checkup", patient=new_patient)
        session.add(new_appointment)
        session.commit()  # Committing here again; batching could be more efficient depending on the use case

        # Querying patient appointments
        patient_appointments = session.query(Appointment).filter_by(patient_id=new_patient.id).all()
        for appointment in patient_appointments:
            print(f"Appointment ID: {appointment.id}, Time: {appointment.appointment_time}, Details: {appointment.details}")