#!/usr/bin/python3
class City:
    """
    Represents a city.
    """

    def __init__(self, state_id="", name=""):
        """
        Initializes a new City object.

        Args:
            state_id (str): The state ID of the city.
            name (str): The name of the city.
        """
        self.state_id = state_id
        self.name = name

    def save(self):
        """
        Saves the city to the database.
        """
        pass

    def delete(self):
        """
        Deletes the city from the database.
        """
        pass

    @classmethod
    def find_by_state_id(cls, state_id):
        """
        Finds cities by state ID.

        Args:
            state_id (str): The state ID to search for.

        Returns:
            List[City]: A list of cities matching the state ID.
        """
        pass

    @classmethod
    def find_by_name(cls, name):
        """
        Finds cities by name.

        Args:
            name (str): The name to search for.

        Returns:
            List[City]: A list of cities matching the name.
        """
        pass
