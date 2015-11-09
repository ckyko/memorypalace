from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Amber needs to memorize som chemistry terms and goes to MemoryPalace
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention MemoryPalace
        self.assertIn('MemoryPalace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Memory Palace', header_text)

if __name__ == '__main__':
    unittest.main()
