"""
database.py  –  London Uncovered
Handles all MySQL connection and query helpers.
"""

import mysql.connector
from mysql.connector import Error
import bcrypt

# ─────────────────────────────────────────────
#  Database configuration  –  edit these values
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "YourNewPassword123!",
    "database": "london_uncovered",
    "charset":  "utf8mb4",
    "autocommit": True,
}


# ══════════════════════════════════════════════
#  Low-level helpers
# ══════════════════════════════════════════════

def get_connection():
    """Return a live MySQL connection, or raise on failure."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as exc:
        raise ConnectionError(
            f"Cannot connect to MySQL.\n"
            f"Please check that MySQL is running and the credentials in database.py are correct.\n"
            f"Details: {exc}"
        ) from exc


def execute_query(query: str, params: tuple = (), fetch: bool = False):
    """
    Run a parameterised query.

    Parameters
    ----------
    query  : SQL string with %s placeholders
    params : tuple of values
    fetch  : True  → return list[dict] rows
             False → return lastrowid (for INSERT) or rowcount (for others)
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
    except Error as exc:
        raise RuntimeError(f"Database error: {exc}") from exc
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ══════════════════════════════════════════════
#  Password helpers
# ══════════════════════════════════════════════

def hash_password(plain: str) -> str:
    """Return bcrypt hash of *plain* as a UTF-8 string."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(plain: str, hashed: str) -> bool:
    """Return True if *plain* matches *hashed*."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# ══════════════════════════════════════════════
#  User operations
# ══════════════════════════════════════════════

def register_user(name: str, email: str, password: str) -> bool:
    """
    Insert a new user.  Returns True on success, raises on duplicate email.
    """
    hashed = hash_password(password)
    try:
        execute_query(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name.strip(), email.strip().lower(), hashed),
        )
        return True
    except RuntimeError as exc:
        if "Duplicate entry" in str(exc):
            raise ValueError("An account with that email already exists.") from exc
        raise


def login_user(email: str, password: str):
    """
    Verify credentials.
    Returns the user dict on success, or None if not found / wrong password.
    """
    rows = execute_query(
        "SELECT * FROM users WHERE email = %s",
        (email.strip().lower(),),
        fetch=True,
    )
    if not rows:
        return None
    user = rows[0]
    if check_password(password, user["password"]):
        return user
    return None


# ══════════════════════════════════════════════
#  Attraction operations
# ══════════════════════════════════════════════

def get_all_attractions(search: str = ""):
    """Return attractions, optionally filtered by *search* (name LIKE)."""
    if search:
        return execute_query(
            "SELECT * FROM attractions WHERE name LIKE %s ORDER BY name",
            (f"%{search}%",),
            fetch=True,
        )
    return execute_query(
        "SELECT * FROM attractions ORDER BY name",
        fetch=True,
    )


def get_attraction_by_id(attraction_id: int):
    rows = execute_query(
        "SELECT * FROM attractions WHERE attraction_id = %s",
        (attraction_id,),
        fetch=True,
    )
    return rows[0] if rows else None


def count_attractions() -> int:
    rows = execute_query("SELECT COUNT(*) AS cnt FROM attractions", fetch=True)
    return rows[0]["cnt"] if rows else 0


# ══════════════════════════════════════════════
#  Restaurant operations
# ══════════════════════════════════════════════

def get_all_restaurants(search: str = ""):
    if search:
        return execute_query(
            "SELECT * FROM restaurants WHERE name LIKE %s OR cuisine LIKE %s ORDER BY name",
            (f"%{search}%", f"%{search}%"),
            fetch=True,
        )
    return execute_query("SELECT * FROM restaurants ORDER BY name", fetch=True)


def count_restaurants() -> int:
    rows = execute_query("SELECT COUNT(*) AS cnt FROM restaurants", fetch=True)
    return rows[0]["cnt"] if rows else 0


# ══════════════════════════════════════════════
#  Hotel operations
# ══════════════════════════════════════════════

def get_all_hotels(search: str = ""):
    if search:
        return execute_query(
            "SELECT * FROM hotels WHERE name LIKE %s OR location LIKE %s ORDER BY name",
            (f"%{search}%", f"%{search}%"),
            fetch=True,
        )
    return execute_query("SELECT * FROM hotels ORDER BY name", fetch=True)


def count_hotels() -> int:
    rows = execute_query("SELECT COUNT(*) AS cnt FROM hotels", fetch=True)
    return rows[0]["cnt"] if rows else 0


# ══════════════════════════════════════════════
#  Favourites operations
# ══════════════════════════════════════════════

def add_favourite(user_id: int, attraction_id: int) -> bool:
    """Add to favourites. Returns True on success, False if already exists."""
    try:
        execute_query(
            "INSERT INTO favourites (user_id, attraction_id) VALUES (%s, %s)",
            (user_id, attraction_id),
        )
        return True
    except RuntimeError as exc:
        if "Duplicate entry" in str(exc):
            return False          # already a favourite
        raise


def remove_favourite(user_id: int, attraction_id: int):
    execute_query(
        "DELETE FROM favourites WHERE user_id = %s AND attraction_id = %s",
        (user_id, attraction_id),
    )


def get_favourites(user_id: int):
    """Return list of attraction dicts for this user's favourites."""
    return execute_query(
        """
        SELECT a.*
        FROM   favourites f
        JOIN   attractions a ON a.attraction_id = f.attraction_id
        WHERE  f.user_id = %s
        ORDER  BY a.name
        """,
        (user_id,),
        fetch=True,
    )


def is_favourite(user_id: int, attraction_id: int) -> bool:
    rows = execute_query(
        "SELECT 1 FROM favourites WHERE user_id = %s AND attraction_id = %s",
        (user_id, attraction_id),
        fetch=True,
    )
    return bool(rows)


# ══════════════════════════════════════════════
#  Trip operations
# ══════════════════════════════════════════════

def create_trip(user_id: int, trip_name: str, start_date: str, end_date: str) -> int:
    """Insert a trip and return its new trip_id."""
    return execute_query(
        "INSERT INTO trips (user_id, trip_name, start_date, end_date) VALUES (%s, %s, %s, %s)",
        (user_id, trip_name.strip(), start_date, end_date),
    )


def get_trips(user_id: int):
    return execute_query(
        "SELECT * FROM trips WHERE user_id = %s ORDER BY start_date",
        (user_id,),
        fetch=True,
    )


def delete_trip(trip_id: int, user_id: int):
    """Delete only if the trip belongs to the requesting user."""
    execute_query(
        "DELETE FROM trips WHERE trip_id = %s AND user_id = %s",
        (trip_id, user_id),
    )


def add_attraction_to_trip(trip_id: int, attraction_id: int) -> bool:
    """Returns True on success, False if already added."""
    try:
        execute_query(
            "INSERT INTO trip_attractions (trip_id, attraction_id) VALUES (%s, %s)",
            (trip_id, attraction_id),
        )
        return True
    except RuntimeError as exc:
        if "Duplicate entry" in str(exc):
            return False
        raise


def get_trip_attractions(trip_id: int):
    return execute_query(
        """
        SELECT a.*
        FROM   trip_attractions ta
        JOIN   attractions a ON a.attraction_id = ta.attraction_id
        WHERE  ta.trip_id = %s
        ORDER  BY a.name
        """,
        (trip_id,),
        fetch=True,
    )


def remove_attraction_from_trip(trip_id: int, attraction_id: int):
    execute_query(
        "DELETE FROM trip_attractions WHERE trip_id = %s AND attraction_id = %s",
        (trip_id, attraction_id),
    )
