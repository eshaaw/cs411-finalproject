import pytest
from unittest.mock import patch, Mock
from weather_app.models.favorites_model import FavoritesModel
from weather_app.models.location_model import Location

@pytest.fixture
@patch("weather_app.utils.sql_utils.get_db_connection")
def favorites_model(mock_get_db_connection):
    """Provides a mocked FavoritesModel."""
    mock_get_db_connection.return_value.__enter__.return_value.cursor.return_value.fetchall.return_value = []
    return FavoritesModel(user_id=1)

@pytest.fixture
def sample_location():
    """Provides a sample valid location."""
    return Location(id=1, city="Los Angeles", latitude=34.0522, longitude=-118.2437)

def test_add_favorite(favorites_model, sample_location):
    """Test adding a location to favorites."""
    favorites_model.add_favorite(sample_location)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites[0].city == "Los Angeles"

def test_add_duplicate_favorite(favorites_model, sample_location):
    """Test adding a duplicate location to favorites."""
    favorites_model.add_favorite(sample_location)
    with pytest.raises(ValueError, match="already in favorites"):
        favorites_model.add_favorite(sample_location)

def test_remove_favorite(favorites_model, sample_location):
    """Test removing a location from favorites."""
    favorites_model.add_favorite(sample_location)
    favorites_model.remove_favorite(sample_location.id)
    assert len(favorites_model.favorites) == 0

def test_remove_nonexistent_favorite(favorites_model):
    """Test removing a location that doesn't exist in favorites."""
    with pytest.raises(ValueError, match="not found in favorites"):
        favorites_model.remove_favorite(location_id=999)
