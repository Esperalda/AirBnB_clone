#!/usr/bin/python3
"""
This module contains the BaseModel class that defines common
attributes and methods for other classes.
It takes care of the initialization, serialization, and
deserialization of future instances.
"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    The BaseModel class defines common attributes and methods
    for other classes.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initializes an instance of the BaseModel class."""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                elif key != "__class__":
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def __str__(self) -> str:
        """Returns a string representation of the instance."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self) -> None:
        """Updates the public instance's updated_at attribute and
        saves the instance."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        fin_dict = dict(self.__dict__)
        fin_dict["__class__"] = self.__class__.__name__
        if not isinstance(fin_dict["created_at"], str):
            fin_dict["created_at"] = fin_dict["created_at"].isoformat()
        if not isinstance(fin_dict["updated_at"], str):
            fin_dict["updated_at"] = fin_dict["updated_at"].isoformat()
        return fin_dict
