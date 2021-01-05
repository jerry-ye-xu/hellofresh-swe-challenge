"""
Authors note:

The majority of paths have been covered in the Postman collections.

Both here and in 'test_models.py', we showcase the basic functionality of
pytest and include a few examples.
"""

import pytest

from backend_api import create_app

@pytest.fixture(scope='module')
def test_client():
    app = create_app(test_config=None)

    with app.test_client() as testing_client:
        # We don't initialise the database.
        # The Postman collection already tests the application's
        # ability to handle requests.
        with app.app_context():
            yield testing_client

def test_home_path(test_client):
    rv = test_client.get('/')

    assert rv.status_code == 200
    assert b"Welcome to the HelloFresh SWE Challenge Backend API." == rv.data

def test_bp_recipe_home_path(test_client):
    rv = test_client.get('/recipes/')
    rv_post = test_client.post('/recipes/', json=None)
    rv_post_json = test_client.post('/recipes/', json={"fk_recipe": "testing"})

    assert rv.status_code == 200
    assert rv_post.status_code == 415
    assert rv_post_json.status_code == 400