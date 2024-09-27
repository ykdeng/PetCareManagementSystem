from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///pets.db")

Base = declarative_base()

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    breed = Column(String)
    age = Column(Integer)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    
    owner = relationship("Owner", back_populates="pets")

class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String)
    pets = relationship("Pet", back_populates="owner")

engine = create_engine(DATABASE_URI)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_owner(name, phone_number):
    owner = Owner(name=name, phone_number=phone_number)
    session.add(owner)
    session.commit()

def add_pet(name, type, breed, age, owner_id):
    pet = Pet(name=name, type=type, breed=breed, age=age, owner_id=owner_id)
    session.add(pet)
    session.commit()

def find_pet_by_name(name):
    return session.query(Pet).filter(Pet.name == name).all()

def find_owner_by_name(name):
    return session.query(Owner).filter(Owner.name == name).all()