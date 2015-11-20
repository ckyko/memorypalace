from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_hompage(self):
        # Amber needs to memorize som chemistry terms and goes to MemoryPalace
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention MemoryPalace
        self.assertIn('MemoryPalace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome!', header_text)

    def test_register(self):

        self.browser.get('http://localhost:8000/register')
        self.assertIn('MemoryPalace', self.browser.title)
        element = self.browser.find_element_by_id("id_username")
        element.send_keys("testuser")
        element = self.browser.find_element_by_id("email")
        element.send_keys("testuser@testemail.com")
        element = self.browser.find_element_by_id("id_password1")
        element.send_keys("testuser")
        element = self.browser.find_element_by_id("id_password2")
        element.send_keys("testuser")
        self.browser.find_element_by_id("register_submit").click()
        self.assertIn('http://localhost:8000', self.browser.current_url)

if __name__ == '__main__':
    unittest.main()
