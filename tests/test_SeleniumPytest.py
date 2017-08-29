import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope='session')
def browser():
        browser = webdriver.Chrome()
        yield browser
        browser.quit()


def test_PageTitle(browser):
    browser.get('http://www.google.com')
    assert 'Google' in browser.title


def test_SearchPageTitle(browser):
    browser.get('http://www.google.com')
    assert 'Google' in browser.title
    element = browser.find_element_by_id('lst-ib')
    assert element is not None
    element.send_keys('Red Hat' + Keys.RETURN)
    assert browser.title.startswith('Red Hat')
