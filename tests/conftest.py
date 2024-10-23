import pytest
from app import create_app
from app.models import db

from app.config import TestingConfig


@pytest.fixture(scope='session')
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the tables in the test DB
            yield client  # The tests will run here
            db.drop_all()  # Drop the tables after tests