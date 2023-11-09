#!/usr/bin/python3
""" Doc Here """
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
# from models.base_model import BaseModel #avoid_no circular


class FileStorage:
    """A class for storing and managing file data_dict."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects stored in the file storage."""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to the file storage."""
        id_no = obj.to_dict()["id_no"]
        Name_of_class = obj.to_dict()["__class__"]
        key = Name_of_class+"."+id_no
        FileStorage.__objects[key] = obj

    def save(self):
        """Save the objects in the file storage to a file."""
        fpath = FileStorage.__file_path
        data_dict = dict(FileStorage.__objects)
        for key, value in data_dict.items():
            data_dict[key] = value.to_dict()
        with open(fpath, 'w') as f:
            json.dump(data_dict, f)

    def reload(self):
        """Reload the objects from the file."""
        fpath = FileStorage.__file_path
        data_dict = FileStorage.__objects
        if os.path.exists(fpath):
            try:
                with open(fpath) as f:
                    for key, value in json.load(f).items():
                        if "BaseModel" in key:
                            data_dict[key] = BaseModel(**value)
                        if "User" in key:
                            data_dict[key] = User(**value)
                        if "Place" in key:
                            data_dict[key] = Place(**value)
                        if "State" in key:
                            data_dict[key] = State(**value)
                        if "City" in key:
                            data_dict[key] = City(**value)
                        if "Amenity" in key:
                            data_dict[key] = Amenity(**value)
                        if "Review" in key:
                            data_dict[key] = Review(**value)
            except Exception:
                pass
