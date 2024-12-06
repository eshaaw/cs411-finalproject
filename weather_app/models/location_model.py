from dataclasses import dataclass
import logging
from utils.api_utils import fetch_air_quality_data, fetch_historical_data, fetch_forecast
from utils.sql_utils import get_db_connection
from utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class Location:
    id: int
    city: str
    latitude: float
    longitude: float

    def __post_init__(self):
        # Validate latitude and longitude values
        if not (-90 <= self.latitude <= 90) or not (-180 <= self.longitude <= 180):
            raise ValueError(f"Invalid latitude or longitude: {self.latitude}, {self.longitude}")

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    def get_air_quality(self):
        """
        Fetches the current air quality for this location from an external API.
        """
        try:
            air_quality = fetch_air_quality_data(self.latitude, self.longitude)
            return air_quality
        except Exception as e:
            logger.error("Error fetching air quality for %s: %s", self.city, str(e))
            raise e

    def get_historical_weather(self):
        """
        Fetches historical weather data for this location from an external API.
        """
        try:
            historical_data = fetch_historical_data(self.latitude, self.longitude)
            return historical_data
        except Exception as e:
            logger.error("Error fetching historical weather for %s: %s", self.city, str(e))
            raise e

    def get_forecast(self):
        """
        Fetches a weather forecast for this location from an external API.
        """
        try:
            forecast_data = fetch_forecast(self.latitude, self.longitude)
            return forecast_data
        except Exception as e:
            logger.error("Error fetching forecast for %s: %s", self.city, str(e))
            raise e

    @staticmethod
    def create_location(city: str, latitude: float, longitude: float) -> 'Location':
        """
        Adds a new location to the database.

        Args:
            city (str): The city of the location.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            Location: The created Location object with its ID populated.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO locations (city, latitude, longitude)
                VALUES (?, ?, ?)
            """, (city, latitude, longitude))
            conn.commit()
            location_id = cursor.lastrowid
            logger.info("Created new location: %s with ID %d", city, location_id)
            return Location(id=location_id, city=city, latitude=latitude, longitude=longitude)

    @staticmethod
    def get_location_by_id(location_id: int) -> 'Location':
        """
        Retrieves a location by its ID.

        Args:
            location_id (int): The ID of the location.

        Returns:
            Location: The location corresponding to the given ID.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, city, latitude, longitude
                FROM locations
                WHERE id = ?
            """, (location_id,))
            row = cursor.fetchone()
            if row:
                return Location(id=row[0], city=row[1], latitude=row[2], longitude=row[3])
            else:
                logger.error("Location with ID %d not found", location_id)
                raise ValueError(f"Location with ID {location_id} not found")
