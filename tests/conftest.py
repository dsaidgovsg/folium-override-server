import pytest

from app import create_app


@pytest.fixture(scope="session")
def app(request):
    a = create_app()
    with a.app_context():
        yield a
