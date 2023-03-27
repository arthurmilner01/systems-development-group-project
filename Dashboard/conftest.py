from main import *

import pytest

# @pytest.fixture()
# def app():
#     app = app()
#     app.config.update({
#         "TESTING": True,
#     })

#         # other setup can go here

#     yield app

#         # clean up / reset resources here


# @pytest.fixture()
# def client(app):
#     return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()

@pytest.fixture()
def app():
    app = app("sqlite://")

    with app.app_context():
        sqlite3.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()