#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', back_populates='state\
', cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """getter function to get the cities related to a state"""
            from models import storage
            from models.city import City
            my_list = []
            city_dict = storage.all(City)  # contains all the city objects
            for value in city_dict.values():
                if value.state_id == self.id:
                    my_list.append(value)
            return my_list
