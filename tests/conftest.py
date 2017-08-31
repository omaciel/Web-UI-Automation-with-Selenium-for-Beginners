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


@pytest.yield_fixture(scope='function', params=BROWSERS)
def browser(request):
    """Fixture to create a web browser."""
    # Let's use latest Chrome on MacOS 10.12
    sauce_username = os.environ.get('SAUCE_USERNAME', None)
    sauce_key = os.environ.get('SAUCE_KEY', None)

    # Skip tests if credentials cannot be found
    if sauce_username is None and sauce_key is None:
            pytest.skip('Skipping SauceLabs tests: missing username')

    URL = 'http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(
            sauce_username,
            sauce_key
    )
    # Add build info for easy viewing on SauceLabs
    request.param['build'] = 'Web UI Automation with Selenium for Beginners'
    browser = webdriver.Remote(
            command_executor=URL,
            desired_capabilities=request.param
    )
    yield browser
    # Update SauceLabs test result
    browser.execute_script(
        "sauce:job-result=%s" % str(not request.node.rep_call.failed).lower())
    browser.execute_script(
        "sauce:job-name={}".format(request.node.rep_call.nodeid))
    browser.quit()


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
