import os

import pytest

from selenium import webdriver


BROWSERS = [
        {
            'browserName': 'chrome',
            'platform': 'macOS 10.12',
        },
        {
            'browserName': 'MicrosoftEdge',
            'platform': 'Windows 10',
        },
        {
            'browserName': 'firefox',
            'platform': 'Linux',
        },
        {
            'browserName': 'safari',
            'platform': 'macOS 10.12',
        },
        {
            'browserName': 'Android',
            'deviceName': 'Google Nexus 7 HD Emulator',
            'deviceOrientation': 'portrait',
        },
]


def pytest_addoption(parser):
    """Add command line option to select webdriver capabilities.

    These options can be used to choose the webdriver capabilites
    as such:

    browser_name = request.config.getoption('--webdriver')
    """
    parser.addoption(
        '--browsername',
        action="store",
        default='firefox',
        choices=['chrome', 'firefox', 'safari', 'Android', 'MicrosoftEdge']
        help="Specify the web browser to use for the automation."
    )
    parser.addoption(
        '--platform',
        action="store",
        default='macOS 10.12',
        choices=['macOS 10.12', 'Windows 10', 'Linux']
        help="Specify the platform to use for the automation."
    )


def test_id(fixture_value):
    """Return a human readable ID for a parameterized fixture."""
    return '{browserName}'.format(**fixture_value)


@pytest.yield_fixture(
    scope='function',
    params=BROWSERS,
    ids=test_id,
)
def browser(request):
    """Fixture to create a web browser."""
    sauce_username = os.environ.get('SAUCE_USERNAME', None)
    sauce_key = os.environ.get('SAUCE_KEY', None)

    # Skip tests if credentials cannot be found
    if sauce_username is None and sauce_key is None:
            pytest.skip('Skipping SauceLabs tests: missing username')

    URL = 'http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(
            sauce_username,
            sauce_key
    )
    request.param['build'] = 'Web UI Automation with Selenium for Beginners'
    browser = webdriver.Remote(
            command_executor=URL,
            desired_capabilities=request.param
    )

    def close_browser():
        """Handle closing browser object."""
        browser.quit()

    def update_saucelabs():
        """Add build info for easy viewing on SauceLabs."""
        browser.execute_script(
            "sauce:job-result={}".format(
                str(not request.node.rep_call.failed).lower()))
        browser.execute_script(
            "sauce:job-name={}".format(request.node.rep_call.nodeid))

    request.addfinalizer(update_saucelabs)
    request.addfinalizer(close_browser)

    return browser


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for SauceLabs reporting.
    # execute all other hooks to obtain the report object
    #
    # Borrowed from https://github.com/saucelabs-sample-test-frameworks/
    #                       Python-Pytest-Selenium/blob/master/conftest.py
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
