"""General testing fixures."""
import os

import pytest

from booking.config import get_database_connection, get_openai_client


APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@pytest.fixture(scope="session", name="set_environment_variables")
def load_environment_variables() -> None:
    """Set the environment variables from the .env file."""
    env_path = os.path.join(APP_DIR, "app", ".env")

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            kv = line.strip().split("=", maxsplit=1)
            os.environ[kv[0]] = kv[1]


@pytest.fixture(name="db_session")
def create_db_session(
    set_environment_variables,
):
    """Fixture to provide a database session for testing."""
    connection = get_database_connection()

    yield connection
    connection.close()


@pytest.fixture()
def clear_db(db_session) -> None:
    """Clear the database."""
    script_path = os.path.join(APP_DIR, "app/tests/scripts", "clear_db.sql")

    with open(script_path, "r", encoding="utf-8") as f:
        query = f.read()

        with db_session.cursor() as cursor:
            cursor.execute(query)
            db_session.commit()


@pytest.fixture(name="openai_client")
def create_openai_client(set_environment_variables):
    """Create an OpenAI client."""

    openai_client = get_openai_client()

    yield openai_client
