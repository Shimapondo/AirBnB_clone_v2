#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.user import User
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'file':
    storage = FileStorage()
    storage.reload()
else:
    storage = DBStorage()
    storage.reload()
