import os
import pytest
import time
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from main import app
from database import get_db
from settings import Settings
from alembic.command import upgrade, downgrade
from alembic.config import Config


@pytest.fixture(autouse=True)
def slow_down_tests():
    yield
    time.sleep(1)


@pytest.fixture(scope="session")
def apply_migrations():
    config = Config("alembic.ini")
    upgrade(config, "head")
    yield
    downgrade(config, "base")


@pytest.fixture(name="session")
def session_fixture(apply_migrations: None):
    settings = Settings()
    engine = create_engine(
        settings.db_uri_test, connect_args={"check_same_thread": False}
    )
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """

    pytest.access_token = None


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """

    # Delete DB file
    db_file = os.path.join('.', 'test.db')
    if os.path.exists(db_file):
        os.remove(db_file)
