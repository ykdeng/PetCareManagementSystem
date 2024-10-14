from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.exc import SQLAlchemyError
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
    try:
        owner = Owner(name=name, phone_number=phone_number)
        session.add(owner)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()  # Rollback the changes on error
        print(f"An error occurred while adding an owner: {e}")
    except Exception as e:
        session.rollback()  # Rollback the changes on any other unexpected error
        print(f"Unexpected error: {e}")
    else:
        print(f"Owner {name} added successfully.")


def add_pet(name, type, breed, age, owner_id):
    try:
        pet = Pet(name=name, type=type, breed=breed, age=age, owner_id=owner_id)
        session.add(pet)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()  # Rollback the changes on error
        print(f"An error occurred while adding a pet: {e}")
    except Exception as e:
        session.rollback()  # Rollback the changes on any other unexpected error
        print(f"Unexpected error: {e}")
    else:
        print(f"Pet {name} added successfully.")


def find_pet_by_name(name):
    try:
        pets = session.query(Pet).filter(Pet.name == name).all()
        return pets
    except SQLAlchemyError as e:
        print(f"An error occurred while fetching pets: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def find_owner_by_name(name):
    try:
        owners = session.query(Owner).filter(Owner.name == name).all()
        return owners
    except SQLAlchemyError as e:
        print(f"An error occurred while fetching owners: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")