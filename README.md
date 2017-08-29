# Web UI Automation with Selenium for Beginners

## Objective

* Cover Web UI automation using Selenium with a focus on the Python programming language
* Learn how to easily gather Web UI information, record their actions and play them back via Selenium IDE or Scirocco
* Write Python code to perform the same actions
* Run your code with py.test
* Use **SauceLabs** to execute automated tests on multiple types of operating systems and web browser combinations.
* Use **Travis** for a Continuous Integration/Delivery process

## Using Selenium IDE

### What is it?

* It is a plugin
* Only works for Firefox
  * Can be tricky to install
  * Does not seem to work with Firefox > 50.0
* Let's you record your actions while interacting with web browser and reply them
* Requires creativity to ensure that playing back activities will wait for web elements to be present

### How to install it

* Make sure that you're using an older version of **Firefox**
  * I recommend version [45](https://ftp.mozilla.org/pub/firefox/releases/45.0/)
* Install [Selenium IDE](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/) on your system

### How to use it - Quick demo


## Using Selenium with Python

### Install the selenium python module

```shell
mkvirtualenv -p $(which python3) -i selenium selenium-talk
pip install bpython
```

### Install web driver

You will need to install a valid webdriver:

* Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
* Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
* Firefox:	https://github.com/mozilla/geckodriver/releases
* Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

For this tutorial I have chosen to use the web driver for the chrome web browser.

**NOTE**: Make sure to include the ChromeDriver location in your PATH environment variable

### Interact with Chrome via Python Selenium

```python
>>> from selenium import webdriver
>>> from selenium.webdriver.common.keys import Keys
>>> browser = webdriver.Chrome()
>>> browser.get('https://www.google.com')

>>> element = browser.find_element_by_id('lst-ib')
>>> assert element is not None
>>> element.send_keys('Red Hat' + Keys.RETURN)
>>> assert browser.title.startswith('Red Hat')

>>> element = browser.find_element_by_id('hplogo')
>>> assert element is not None
>>> browser.execute_script("arguments[0].setAttribute('srcset', 'https://omaciel.fedorapeople
.org/ogmaciel.png')", element)
>>> browser.execute_script("arguments[0].setAttribute('height', '100%')", element)
```

## Using Python Selenium with Unittest

File: test_SeleniumUnittest.py

```python
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GoogleTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def testPageTitle(self):
        self.browser.get('http://www.google.com')
        self.assertIn('Google', self.browser.title)

    def testSearchPageTitle(self):
        self.browser.get('http://www.google.com')
        self.assertIn('Google', self.browser.title)
        element = self.browser.find_element_by_id('lst-ib')
        assert element is not None
        element.send_keys('Red Hat' + Keys.RETURN)
        assert self.browser.title.startswith('Red Hat')


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

Now, execute it:

```shell
python tests/test_SeleniumUnittest.py
testPageTitle (__main__.GoogleTestCase) ... ok
testSearchPageTitle (__main__.GoogleTestCase) ... ok

----------------------------------------------------------------------
Ran 2 tests in 9.557s

OK
```

## Using Python Selenium with Pytest

### Install pytest

```shell
pip install pytest
```

File: test_SeleniumPytest.py

```python
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
```

Now, execute it:

```shell
pytest -v tests/test_SeleniumPytest.py
================================ test session starts =================================
platform darwin -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /Users/omaciel/.virtualenvs/selenium-talk/bin/python3.6
cachedir: .cache
rootdir: /Users/omaciel/Dropbox/Work/pythontalk, inifile:
plugins: xdist-1.20.0, forked-0.2
collected 2 items

tests/test_SeleniumPytest.py::test_PageTitle PASSED
tests/test_SeleniumPytest.py::test_SearchPageTitle PASSED

============================== 2 passed in 5.86 seconds ==============================

```

## Running All Tests Simultaneously

### Install python-xdist

```shell
pip install python-xdist
```

### Execute All Tests

```shell
pytest -n 4 
```

## Using Python Selenium with Pytest and SauceLabs

Assuming that you have an account at [SauceLabs]() and that you have exported your credentials via your system's environmental variables:

File: test_SeleniumSauce.py

```python
import os

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope='session')
def browser():
        desired_cap = {
                'browserName': "chrome",
                'platform': "macOS 10.12",
                }
        sauce_username = os.environ.get('SAUCE_USERNAME', None)
        sauce_key = os.environ.get('SAUCE_KEY', None)
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
    browser.get('http://www.google.com')
    assert 'Google' in browser.title


def test_SearchPageTitle(browser):
    browser.get('http://www.google.com')
    assert 'Google' in browser.title
    element = browser.find_element_by_id('lst-ib')
    assert element is not None
    element.send_keys('Red Hat' + Keys.RETURN)
    assert browser.title.startswith('Red Hat')
```

Now, execute it:

```shell
pytest -v tests/test_SeleniumSauce.py
pytest -v tests/test_SeleniumSauce.py
================================ test session starts =================================
platform darwin -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /Users/omaciel/.virtualenvs/selenium-talk/bin/python3.6
cachedir: .cache
rootdir: /Users/omaciel/Dropbox/Work/pythontalk, inifile:
plugins: xdist-1.20.0, forked-0.2
collected 2 items

tests/test_SeleniumSauce.py::test_PageTitle PASSED
tests/test_SeleniumSauce.py::test_SearchPageTitle PASSED

============================= 2 passed in 15.89 seconds ==============================
```
