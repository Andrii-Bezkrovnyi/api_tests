import os
from datetime import datetime

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.superheroapi.com/api.php"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


@pytest.fixture
def session():
    """Fixture for HTTP requests to the Superhero API."""
    with requests.Session() as api_session:
        yield api_session


@pytest.fixture(scope="session")
def base_url():
    """Fixture for the base URL of the Superhero API."""
    return BASE_URL


@pytest.fixture(scope="session")
def access_token():
    """Fixture for the access token for the Superhero API."""
    return ACCESS_TOKEN


def pytest_configure(config):
    """Add a timestamp to the HTML report filename if not set."""
    if not config.getoption("htmlpath"):  # if no custom path is set
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = f"reports/report_{timestamp}.html"
        config.option.htmlpath = report_file
