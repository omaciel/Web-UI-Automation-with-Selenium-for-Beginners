from selenium.webdriver.common.keys import Keys


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
