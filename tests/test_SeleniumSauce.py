import os

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope='session')
def browser():
    """Fixture to create a web browser."""
    # Let's use latest Chrome on MacOS 10.12
    desired_cap = {
            'browserName': "chrome",
            'platform': "macOS 10.12",
    }
    sauce_username = os.environ.get('SAUCE_USERNAME', None)
    sauce_key = os.environ.get('SAUCE_KEY', None)

    # Skip tests if credentials cannot be found
    if sauce_username is None and sauce_key is None:
            pytest.skip('Skipping SauceLabs tests: missing username')

    URL = 'http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(
            sauce_username,
            sauce_key
    )
    browser = webdriver.Remote(
            command_executor=URL,
            desired_capabilities=desired_cap
    )
    yield browser
    browser.quit()


def test_PageTitle(browser):
    """Assert that title of page says 'Google'."""
    browser.get('http://www.google.com')
    assert 'Google' in browser.title


def test_SearchPageTitle(browser):
    """Assert that Google search returns data for Red Hat."""
    browser.get('http://www.google.com')
    assert 'Google' in browser.title
    element = browser.find_element_by_id('lst-ib')
    assert element is not None
    element.send_keys('Red Hat' + Keys.RETURN)
    assert browser.title.startswith('Red Hat')
