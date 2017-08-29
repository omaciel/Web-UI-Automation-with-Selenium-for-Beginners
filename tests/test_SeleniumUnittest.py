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
