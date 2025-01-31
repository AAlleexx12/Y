import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from PhotoShare.app.models.base import Base
from PhotoShare.app.core.database import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {"login": "deadpool", "email": "deadpool@example.com", "password_checksum": "123456789"}


@pytest.fixture(scope="module")
def user_moder():
    return {"login": "dead2pool", "email": "dead2pool@example.com", "password_checksum": "123456789"}


@pytest.fixture(scope="module")
def user_user():
    return {"login": "dead1pool", "email": "dead1pool@example.com", "password_checksum": "123456789"}
