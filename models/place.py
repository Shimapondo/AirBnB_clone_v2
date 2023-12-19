#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.i\
d'), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    user = relationship('User', back_populates='places')
    cities = relationship('City', back_populates='places')

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', back_populates='place',
                               cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False,
                                 back_populates='place_amenities')
    else:
        @property
        def reviews(self):
            from models import storage
            from models.review import Review

            my_list = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    my_list.append(value)
            return my_list

        @property
        def amenities(self):
            from models import storage
            from models.amenity import Amenity

            my_list = []
            for value in storage.all(Amenity).values():
                if value.amenity_id == self.id:
                    my_list.append(value)
            return my_list

        @ammenities_id.setter
        def append(self, obj=None):
            if obj is not None and type(obj) is Amenity:
                self.amenity_id = obj.id
