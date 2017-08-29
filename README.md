# Web UI Automation with Selenium for Beginners

## Objective

* Cover Web UI automation using Selenium with a focus on the Python programming language
* Learn how to easily gather Web UI information, record their actions and play them back via **Selenium IDE** or **Scirocco**
* Write Python code to perform the same actions interactively
* Run your code with **py.test**
* Use **SauceLabs** to execute automated tests on multiple types of operating systems and web browser combinations.
* Use **Travis** for a Continuous Integration/Delivery process

## Follow Along

You can get a copy of all files used in this tutorial by cloning this repository!

```shell
git clone https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners.git
```

Then, make sure to install all the required Python modules using `pip`:

```shell
pip install -r requirements.txt
```

From this point onward you can follow along :)


## Using Selenium IDE

### Overview
* Firefox plugin ONLY
* Can be tricky to install
* Requires Firefox == 45 or older :/
* Records all interactions with browser
* Can replay all recordings
* Allows for multiple tests to be recorded
* **GREAT IDE** with tons of useful features
* Exports test cases into Python code (and other formats)
* Requires creativity to ensure that playing back activities will wait for web elements to be present

### How to install it

* Make sure that you're using an older version of **Firefox**
  * I recommend version [45](https://ftp.mozilla.org/pub/firefox/releases/45.0/)
* Install [Selenium IDE](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/) on your system

![Selenium IDE](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/images/selenium_ide.png)

### Demo
[Selenium IDE demo](https://youtu.be/e1jrrg39V_k)

### Export
Selenium IDE will let you export your recording into Python code.

![Selenium IDE export](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/images/selenium_ide_export.png)

## Using Scirocco Recorder for Chrome

### Overview
* Easier to install
* Works with latest Chrome browser
* Records all interactions with browser
* Can replay all recordings
* Not as full fledged IDE as Selenium IDE
* Limited range of commands
* Limited options for exporting test cases (Python is NOT supported)

### How to install it
* Install [Scirocco](https://chrome.google.com/webstore/detail/scirocco-recorder-for-chr/ibclajljffeaafooicpmkcjdnkbaoiih) from the **Google Web Store**

![Scirocco Recorder for Chrome](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/images/scirocco.png)

### Demo
[Scirocco demo](https://youtu.be/zEL6-pt9hoM)

### Export
Scirocco will let you export your recording.

![Scirocco export](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/images/scirocco_export.png)

## Using Selenium with Python

Now we will write actual python code to interact with a web browser.

### Install the selenium python module

**NOTE**: This step can be skipped if you've cloned the repository and install all Python dependencies.

```shell
pip install selenium
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

Open a python shell:

```python
>>> from selenium import webdriver
>>> from selenium.webdriver.common.keys import Keys
>>> browser = webdriver.Chrome()
>>> browser.get('https://www.google.com')

>>> element = browser.find_element_by_id('lst-ib')
>>> assert element is not None
>>> element.send_keys('Red Hat' + Keys.RETURN)
>>> assert browser.title.startswith('Red Hat')

>>> browser.get('https://www.google.com')
>>> element = browser.find_element_by_id('hplogo')
>>> assert element is not None
>>> browser.execute_script("arguments[0].setAttribute('srcset', 'https://omaciel.fedorapeople
.org/ogmaciel.png')", element)
>>> browser.execute_script("arguments[0].setAttribute('height', '100%')", element)
```

## Demo
[Demo](https://youtu.be/FQwwiVh5Cok)

## Using Python Selenium with Unittest

Let's create a couple of automated tests using Python's unittest module:

File: [test_SeleniumUnittest.py](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/tests/test_SeleniumUnittest.py)

![Selenium + Python Unittest](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/images/python_unittest.png)

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

Let's do the same exercise, but this time using **pytest**

### Install pytest

**NOTE**: This step can be skipped if you've cloned the repository and install all Python dependencies.

```shell
pip install pytest
```

File: [test_SeleniumPytest.py](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/tests/test_SeleniumPytest.py)

![Selenium + Pytest](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/images/python_pytest.png)

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

Now, let's execute all tests in multiple threads:

### Install python-xdist

**NOTE**: This step can be skipped if you've cloned the repository and install all Python dependencies.

```shell
pip install python-xdist
```

### Execute All Tests

```shell
pytest -n 4 
```

## Using Python Selenium with Pytest and SauceLabs

Assuming that you have an account at [SauceLabs](https://saucelabs.com/) and that you have exported your credentials via your system's environmental variables:

File: [test_SeleniumSauce.py](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/tests/test_SeleniumSauce.py)

![Selenium + SauceLabs](https://github.com/omaciel/Web-UI-Automation-with-Selenium-for-Beginners/blob/master/images/python_saucelabs.png)

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

## Demo
[Demo](https://youtu.be/dxr8lxTv90A)
