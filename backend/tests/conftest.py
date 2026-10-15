import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# A throwaway in-memory SQLite database, used only by the tests.
# StaticPool keeps a single shared connection so every request in a test
# sees the same data. The real database (SQLite dev / PostgreSQL prod) is
# never touched.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tell the app to use the test database instead of the real one.
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    # Each test starts with empty, freshly created tables.
    Base.metadata.create_all(bind=test_engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=test_engine)
