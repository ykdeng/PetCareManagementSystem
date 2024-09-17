from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
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
    age = Column(Integer)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    
    owner = relationship("Owner", back_populates="pets")

class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pets = relationship("Pet", back_populates="owner")

engine = create_engine(DATABASE_URI)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()