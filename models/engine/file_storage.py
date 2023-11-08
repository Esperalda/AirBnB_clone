#!/usr/bin/python3

import json
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User

class FileStorage:
    """
    This class represents a file storage system for storing objects in JSON format.
    """

    def __init__(self, file_path="file.json"):
        """
        Initializes a new instance of the FileStorage class.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path
        self.objects = {}

    def all(self):
        """
        Returns all objects stored in the file storage.

        Returns:
            dict: A dictionary containing all objects.
        """
        return self.objects

    def new(self, obj):
        """
        Adds a new object to the file storage.

        Args:
            obj: The object to be added.
        """
        class_name = obj.__class__.__name__
        self.objects[f"{class_name}.{obj.id}"] = obj

    def save(self):
        """
        Saves the objects in the file storage to the JSON file.
        """
        obj_dict = {key: obj.to_dict() for key, obj in self.objects.items()}
        with open(self.file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Reloads the objects from the JSON file into the file storage.
        """
        try:
            with open(self.file_path, "r") as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name, obj_id = key.split(".")
                    self.objects[key] = globals()[class_name](**value)
        except FileNotFoundError:
            pass