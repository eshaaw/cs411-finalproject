import pytest
from weather_app.models.favorites_model import FavoritesModel
from weather_app.models.location_model import Location


@pytest.fixture
def favorites_model():
    """Fixture to provide a new instance of FavoritesModel for each test."""
    return FavoritesModel(user_id=1)


"""Fixtures providing sample locations for the tests."""
@pytest.fixture
def sample_location1():
    return Location(id=1, city="Los Angeles", latitude=34.0522, longitude=-118.2437)

@pytest.fixture
def sample_location2():
    return Location(id=2, city="New York", latitude=40.7128, longitude=-74.0060)

@pytest.fixture
def sample_favorites(sample_location1, sample_location2):
    return [sample_location1, sample_location2]


##################################################
# Add Location Management Test Cases
##################################################

def test_add_location_to_favorites(favorites_model, sample_location1):
    """Test adding a location to favorites."""
    favorites_model.add_location_to_favorites(sample_location1)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites[0].city == "Los Angeles"

def test_add_duplicate_location_to_favorites(favorites_model, sample_location1):
    """Test error when adding a duplicate location to favorites by ID."""
    favorites_model.add_location_to_favorites(sample_location1)
    with pytest.raises(ValueError, match="Location with ID 1 already exists in favorites"):
        favorites_model.add_location_to_favorites(sample_location1)


##################################################
# Remove Location Management Test Cases
##################################################

def test_remove_location_by_location_id(favorites_model, sample_favorites):
    """Test removing a location from favorites by location ID."""
    favorites_model.favorites.extend(sample_favorites)
    assert len(favorites_model.favorites) == 2

    favorites_model.remove_location_by_location_id(1)
    assert len(favorites_model.favorites) == 1, f"Expected 1 location, but got {len(favorites_model.favorites)}"
    assert favorites_model.favorites[0].id == 2, "Expected location with ID 2 to remain"

def test_remove_location_by_city_name(favorites_model, sample_favorites):
    """Test removing a location from favorites by city name."""
    favorites_model.favorites.extend(sample_favorites)
    assert len(favorites_model.favorites) == 2

    favorites_model.remove_location_by_city_name("Los Angeles")
    assert len(favorites_model.favorites) == 1, f"Expected 1 location, but got {len(favorites_model.favorites)}"
    assert favorites_model.favorites[0].city == "New York", "Expected location to be New York"


##################################################
# Favorites Retrieval Test Cases
##################################################

def test_get_all_favorites(favorites_model, sample_favorites):
    """Test successfully retrieving all favorite locations."""
    favorites_model.favorites.extend(sample_favorites)

    all_favorites = favorites_model.get_all_favorites()
    assert len(all_favorites) == 2
    assert all_favorites[0].id == 1
    assert all_favorites[1].id == 2

def test_get_favorite_by_id(favorites_model, sample_location1):
    """Test successfully retrieving a favorite by location ID."""
    favorites_model.add_location_to_favorites(sample_location1)

    retrieved_location = favorites_model.get_favorite_by_id(1)

    assert retrieved_location.id == 1
    assert retrieved_location.city == "Los Angeles"
    assert retrieved_location.latitude == 34.0522
    assert retrieved_location.longitude == -118.2437


##################################################
# Utility Function Test Cases
##################################################

def test_check_if_empty_non_empty_favorites(favorites_model, sample_location1):
    """Test check_if_empty does not raise error if favorites list is not empty."""
    favorites_model.add_location_to_favorites(sample_location1)
    try:
        favorites_model.check_if_empty()
    except ValueError:
        pytest.fail("check_if_empty raised ValueError unexpectedly on non-empty favorites list")

def test_check_if_empty_empty_favorites(favorites_model):
    """Test check_if_empty raises error when favorites list is empty."""
    with pytest.raises(ValueError, match="Favorites list is empty"):
        favorites_model.check_if_empty()

def test_validate_location_id(favorites_model, sample_location1):
    """Test validate_location_id does not raise error for valid location ID."""
    favorites_model.add_location_to_favorites(sample_location1)
    try:
        favorites_model.validate_location_id(1)
    except ValueError:
        pytest.fail("validate_location_id raised ValueError unexpectedly for valid location ID")

def test_validate_location_id_invalid_id(favorites_model):
    """Test validate_location_id raises error for invalid location ID."""
    with pytest.raises(ValueError, match="Invalid location ID: -1"):
        favorites_model.validate_location_id(-1)

    with pytest.raises(ValueError, match="Invalid location ID: invalid"):
        favorites_model.validate_location_id("invalid")
