import pytest
from weather_app.models.location_model import Location

@pytest.fixture
def valid_location():
    """Provides a valid location object for testing."""
    return Location(id=1, city="New York", latitude=40.7128, longitude=-74.0060)

@pytest.fixture
def invalid_location_lat():
    """Provides an invalid location object with an invalid latitude."""
    return Location(id=2, city="Invalid Lat", latitude=100.0, longitude=-74.0060)

@pytest.fixture
def invalid_location_lon():
    """Provides an invalid location object with an invalid longitude."""
    return Location(id=3, city="Invalid Lon", latitude=40.7128, longitude=-190.0)

def test_valid_location_initialization(valid_location):
    """Test initializing a valid location."""
    assert valid_location.city == "New York"
    assert valid_location.latitude == 40.7128
    assert valid_location.longitude == -74.0060

def test_invalid_latitude_initialization():
    """Test initializing a location with invalid latitude."""
    with pytest.raises(ValueError, match="Invalid latitude or longitude"):
        Location(id=2, city="Invalid Lat", latitude=100.0, longitude=-74.0060)

def test_invalid_longitude_initialization():
    """Test initializing a location with invalid longitude."""
    with pytest.raises(ValueError, match="Invalid latitude or longitude"):
        Location(id=3, city="Invalid Lon", latitude=40.7128, longitude=-190.0)

def test_to_dict_method(valid_location):
    """Test converting a location to a dictionary."""
    location_dict = valid_location.to_dict()
    expected = {
        "id": 1,
        "city": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
    }
    assert location_dict == expected
