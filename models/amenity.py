#!/usr/bin/python3

class Amenity:
    """
    Represents an Amenity object.
    """

    def __init__(self, name=""):
        """
        Initializes a new Amenity object.

        Args:
            name (str): The name of the Amenity.
        """
        self.name = name

    def save(self):
        """
        Saves the Amenity object to the database.
        """
        pass

    def delete(self):
        """
        Deletes the Amenity object from the database.
        """
        pass

    @staticmethod
    def get_all():
        """
        Retrieves all Amenity objects from the database.

        Returns:
            list: A list of Amenity objects.
        """
        pass

    @staticmethod
    def get_by_id(id):
        """
        Retrieves an Amenity object by its ID from the database.

        Args:
            id (int): The ID of the Amenity.

        Returns:
            Amenity: The Amenity object with the specified ID.
        """
        pass