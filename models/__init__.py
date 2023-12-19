#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.user import User
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    print("here")
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
