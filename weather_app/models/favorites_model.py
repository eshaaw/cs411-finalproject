import logging
from typing import List
from weather_app.models.location_model import Location
from weather_app.utils.sql_utils import get_db_connection
from weather_app.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


class FavoritesModel:
    """
    A class to manage a user's collection of favorite locations.

    Attributes:
        user_id (int): The ID of the user whose favorites are being managed.
        favorites (List[Location]): The list of the user's favorite locations.
    """

    def __init__(self, user_id: int):
        """
        Initializes the FavoritesModel with an empty list for the user's favorites.
        
        Args:
            user_id (int): The ID of the user whose favorites are being managed.
        """
        self.user_id = user_id
        self.favorites: List[Location] = []

    ##################################################
    # Favorite Management Functions
    ##################################################

    def add_location_to_favorites(self, location: Location) -> None:
        """
        Adds a location to the favorites.

        Args:
            location (Location): The location to add to the favorites.

        Raises:
            TypeError: If the location is not a valid Location instance.
            ValueError: If a location with the same 'id' already exists.
        """
        logger.info("Adding new location to favorites")
        if not isinstance(location, Location):
            logger.error("Location is not a valid Location instance")
            raise TypeError("Location is not a valid Location instance")

        location_id = self.validate_location_id(location.id, check_in_favorites=False)
        if location_id in [favorite.id for favorite in self.favorites]:
            logger.error("Location with ID %d already exists in favorites", location.id)
            raise ValueError(f"Location with ID {location.id} already exists in favorites")

        self.favorites.append(location)

    def remove_location_by_location_id(self, location_id: int) -> None:
        """
        Removes a location from favorites by its location ID.

        Args:
            location_id (int): The ID of the location to remove from favorites.

        Raises:
            ValueError: If the favorites list is empty or the location ID is invalid.
        """
        logger.info("Removing location with ID %d from favorites", location_id)
        self.check_if_empty()
        location_id = self.validate_location_id(location_id)
        self.favorites = [
            location for location in self.favorites if location.id != location_id
        ]
        logger.info("Location with ID %d has been removed", location_id)

    def remove_location_by_city_name(self, city: str) -> None:
        """
        Removes a location from favorites by its city name.

        Args:
            city (str): The city name of the location to remove from favorites.

        Raises:
            ValueError: If the favorites list is empty or the city is not found in favorites.
        """
        logger.info("Removing location with city '%s' from favorites", city)
        self.check_if_empty()

        # Validate the city name exists in favorites
        matching_locations = [location for location in self.favorites if location.city == city]
        if not matching_locations:
            logger.error("City '%s' is not in favorites", city)
            raise ValueError(f"City '{city}' is not in favorites")

        # Remove all locations matching the city name
        self.favorites = [
            location for location in self.favorites if location.city != city
        ]
        logger.info("Location(s) with city '%s' have been removed", city)

    ##################################################
    # Favorites Retrieval Functions
    ##################################################

    def get_all_favorites(self) -> List[Location]:
        """
        Returns a list of all favorite locations for the user.

        Returns:
            List[Location]: The user's favorite locations.
        """
        self.check_if_empty()
        logger.info("Getting all favorite locations for user ID %d", self.user_id)
        return self.favorites

    def get_favorite_by_id(self, location_id: int) -> Location:
        """
        Retrieves a favorite location by its ID.

        Args:
            location_id (int): The ID of the location to retrieve.

        Raises:
            ValueError: If the location is not found in the user's favorites.

        Returns:
            Location: The requested favorite location.
        """
        self.check_if_empty()
        logger.info("Getting location with ID %d", location_id)
        return next((location for location in self.favorites if location.id == location_id), None)

    ##################################################
    # Utility Functions
    ##################################################

    def check_if_empty(self) -> None:
        """
        Checks if the favorites list is empty, logs an error, and raises a ValueError if it is.

        Raises:
            ValueError: If the favorites list is empty.
        """
        if not self.favorites:
            logger.error("Favorites list is empty")
            raise ValueError("Favorites list is empty")

    def validate_location_id(self, location_id: int, check_in_favorites: bool = True) -> int:
        """
        Validates the given location ID, ensuring it is a non-negative integer.

        Args:
            location_id (int): The location ID to validate.
            check_in_favorites (bool, optional): If True, checks if the location ID exists in the favorites.
                                                 If False, skips the check. Defaults to True.

        Raises:
            ValueError: If the location ID is not valid or not found in favorites.
        """
        try:
            location_id = int(location_id)
            if location_id < 0:
                logger.error("Invalid location ID %d", location_id)
                raise ValueError(f"Invalid location ID: {location_id}")
        except ValueError:
            logger.error("Invalid location ID %s", location_id)
            raise ValueError(f"Invalid location ID: {location_id}")

        if check_in_favorites:
            if location_id not in [location.id for location in self.favorites]:
                logger.error("Location with ID %d not found in favorites", location_id)
                raise ValueError(f"Location with ID {location_id} not found in favorites")

        return location_id
