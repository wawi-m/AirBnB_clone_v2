#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    if models.storage_t == 'db':
        cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """Returns the list of City instances with state_id equals to the current State.id"""
            return [city for city in models.storage.all(City).values() if city.state_id == self.id]
