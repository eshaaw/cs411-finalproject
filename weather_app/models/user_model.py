from dataclasses import dataclass
import logging
from utils.sql_utils import get_db_connection
from utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class User:
    id: int
    username: str
    password_hash: str  # Store hashed passwords, not plain text
    email: str
    created_at: str

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }

    @staticmethod
    def create_user(username: str, password_hash: str, email: str) -> 'User':
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the user.
            password_hash (str): The hashed password of the user.
            email (str): The email of the user.

        Returns:
            User: The created User object with its ID populated.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, email, created_at)
                VALUES (?, ?, ?, datetime('now'))
            """, (username, password_hash, email))
            conn.commit()
            user_id = cursor.lastrowid
            logger.info("Created new user: %s with ID %d", username, user_id)
            return User(id=user_id, username=username, password_hash=password_hash, email=email, created_at="now")

    @staticmethod
    def get_user_by_id(user_id: int) -> 'User':
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The user corresponding to the given ID.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, password_hash, email, created_at
                FROM users
                WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password_hash=row[2], email=row[3], created_at=row[4])
            else:
                logger.error("User with ID %d not found", user_id)
                raise ValueError(f"User with ID {user_id} not found")

    @staticmethod
    def authenticate_user(username: str, password_hash: str) -> 'User':
        """
        Authenticates a user by their username and password hash.

        Args:
            username (str): The username of the user.
            password_hash (str): The hashed password of the user.

        Returns:
            User: The authenticated user object.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, password_hash, email, created_at
                FROM users
                WHERE username = ? AND password_hash = ?
            """, (username, password_hash))
            row = cursor.fetchone()
            if row:
                logger.info("Authenticated user: %s", username)
                return User(id=row[0], username=row[1], password_hash=row[2], email=row[3], created_at=row[4])
            else:
                logger.warning("Authentication failed for username: %s", username)
                raise ValueError("Invalid username or password")

    @staticmethod
    def delete_user(user_id: int):
        """
        Deletes a user from the database.

        Args:
            user_id (int): The ID of the user to delete.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM users WHERE id = ?
            """, (user_id,))
            conn.commit()
            logger.info("Deleted user with ID %d", user_id)
