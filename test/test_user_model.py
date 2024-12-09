import pytest
from unittest.mock import patch, MagicMock
from weather_app.utils.db import db
from weather_app.models.user_model import Users

@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    with patch("weather_app.utils.db.db.session", autospec=True) as mock_session:
        yield mock_session

def test_create_user_success(mock_db_session):
    """Test successful user creation."""
    username = "newuser"
    password = "securepassword"
    
    with patch("weather_app.models.user_model.Users._generate_hashed_password", return_value=("salt123", "hashedpassword123")):
        Users.create_user(username, password)
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

def test_create_user_duplicate_username(mock_db_session):
    """Test user creation with a duplicate username."""
    mock_db_session.commit.side_effect = IntegrityError("Duplicate entry", {}, None)

    with pytest.raises(ValueError, match="User with username 'existinguser' already exists"):
        Users.create_user("existinguser", "password123")
    mock_db_session.rollback.assert_called_once()

def test_check_password_success():
    """Test password validation for an existing user."""
    user = MagicMock()
    user.salt = "salt123"
    user.password = "hashedpassword123"
    
    with patch("weather_app.models.user_model.Users.query.filter_by") as mock_query, \
         patch("hashlib.sha256") as mock_hash:
        mock_query.return_value.first.return_value = user
        mock_hash.return_value.hexdigest.return_value = "hashedpassword123"
        
        result = Users.check_password("testuser", "securepassword")
        assert result is True

def test_check_password_failure():
    """Test password validation with incorrect password."""
    user = MagicMock()
    user.salt = "salt123"
    user.password = "hashedpassword123"
    
    with patch("weather_app.models.user_model.Users.query.filter_by") as mock_query, \
         patch("hashlib.sha256") as mock_hash:
        mock_query.return_value.first.return_value = user
        mock_hash.return_value.hexdigest.return_value = "wronghashedpassword"
        
        result = Users.check_password("testuser", "wrongpassword")
        assert result is False

def test_check_password_user_not_found():
    """Test password validation when user is not found."""
    with patch("weather_app.models.user_model.Users.query.filter_by") as mock_query:
        mock_query.return_value.first.return_value = None
        
        with pytest.raises(ValueError, match="User testuser not found"):
            Users.check_password("testuser", "securepassword")

def test_delete_user_success(mock_db_session):
    """Test successful deletion of a user."""
    user = MagicMock()
    
    with patch("weather_app.models.user_model.Users.query.filter_by") as mock_query:
        mock_query.return_value.first.return_value = user
        Users.delete_user("testuser")
        mock_db_session.delete.assert_called_once_with(user)
        mock_db_session.commit.assert_called_once()

def test_delete_user_not_found():
    """Test user deletion when user does not exist."""
    with patch("weather_app.models.user_model.Users.query.filter_by") as mock_query:
        mock_query.return_value.first.return_value = None
        
        with pytest.raises(ValueError, match="User testuser not found"):
            Users.delete_user("testuser")

def test_update_password_success(mock_db_session):
    """Test successful password update."""
    user = MagicMock()
    
    with patch("weather_app.models.user_model.Users.query.filter_by") as mock_query, \
         patch("weather_app.models.user_model.Users._generate_hashed_password", return_value=("newsalt", "newhashedpassword")):
        mock_query.return_value.first.return_value = user
        Users.update_password("testuser", "newpassword")
        assert user.salt == "newsalt"
        assert user.password == "newhashedpassword"
        mock_db_session.commit.assert_called_once()

def test_update_password_user_not_found():
    """Test password update when user does not exist."""
    with patch("weather_app.models.user_model.Users.query.filter_by") as mock_query:
        mock_query.return_value.first.return_value = None
        
        with pytest.raises(ValueError, match="User testuser not found"):
            Users.update_password("testuser", "newpassword")
