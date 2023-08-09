import pytest
from app import create_app, db

@pytest.fixture
def app():
    # app = create_app('test')
    # yield app
    app = create_app('test')
    app.app_context().push()
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture
def client(app):
    with app.app_context():
        with app.test_client() as client:
            yield client