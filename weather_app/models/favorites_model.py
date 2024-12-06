import logging
from typing import List
from location_model import LocationModel
from utils.sql_utils import get_db_connection
from utils.logger import configure_logger

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
        self.favorites: List[Location] = self._load_favorites()

    ##################################################
    # Favorite Management Functions
    ##################################################

    def add_favorite(self, location: Location) -> None:
        """
        Adds a location to the user's favorites.

        Args:
            location (Location): The location to add to the favorites.

        Raises:
            ValueError: If the location is already in the user's favorites.
        """
        logger.info("Adding location %s to favorites", location.city)
        if location.id in [fav.id for fav in self.favorites]:
            logger.error("Location %s is already in favorites", location.city)
            raise ValueError(f"Location {location.city} is already in favorites.")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO favorite_locations (user_id, city, latitude, longitude)
                VALUES (?, ?, ?, ?)
            """, (self.user_id, location.city, location.latitude, location.longitude))
            conn.commit()
            location.id = cursor.lastrowid

        self.favorites.append(location)

    def remove_favorite(self, location_id: int) -> None:
        """
        Removes a location from the user's favorites by its ID.

        Args:
            location_id (int): The ID of the location to remove.

        Raises:
            ValueError: If the location is not found in the user's favorites.
        """
        logger.info("Removing location with ID %d from favorites", location_id)
        if location_id not in [fav.id for fav in self.favorites]:
            logger.error("Location with ID %d not found in favorites", location_id)
            raise ValueError(f"Location with ID {location_id} not found in favorites.")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM favorite_locations
                WHERE id = ? AND user_id = ?
            """, (location_id, self.user_id))
            conn.commit()

        self.favorites = [fav for fav in self.favorites if fav.id != location_id]

    ##################################################
    # Favorites Retrieval Functions
    ##################################################

    def get_all_favorites(self) -> List[Location]:
        """
        Returns a list of all favorite locations for the user.

        Returns:
            List[Location]: The user's favorite locations.
        """
        logger.info("Retrieving all favorites for user ID %d", self.user_id)
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
        logger.info("Retrieving favorite location with ID %d", location_id)
        for location in self.favorites:
            if location.id == location_id:
                return location

        logger.error("Location with ID %d not found in favorites", location_id)
        raise ValueError(f"Location with ID {location_id} not found in favorites.")

    ##################################################
    # Utility Functions
    ##################################################

    def load_favorites(self) -> List[Location]:
        """
        Loads the user's favorite locations from the database.

        Returns:
            List[Location]: The user's favorite locations.
        """
        logger.info("Loading favorites for user ID %d", self.user_id)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, city, latitude, longitude
                FROM favorite_locations
                WHERE user_id = ?
            """, (self.user_id,))
            rows = cursor.fetchall()

        return [Location(id=row[0], city=row[1], latitude=row[2], longitude=row[3]) for row in rows]
