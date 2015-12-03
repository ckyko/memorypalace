from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_1_hompage(self):
        # Amber needs to memorize som chemistry terms and goes to MemoryPalace
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention MemoryPalace
        self.assertIn('MemoryPalace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome!', header_text)

    def test_2_register(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('MemoryPalace', self.browser.title)
        element = self.browser.find_element_by_id("header_modal_L|R")
        element.click()
        element = self.browser.find_element_by_id("tab_modal_register")
        element.click()
        element = self.browser.find_element_by_id("id_username")
        element.send_keys("testuser")
        element = self.browser.find_element_by_id("email")
        element.send_keys("testuser@testemail.com")
        element = self.browser.find_element_by_id("id_password1")
        element.send_keys("testuser")
        element = self.browser.find_element_by_id("id_password2")
        element.send_keys("testuser")
        self.browser.find_element_by_id("register_submit").submit()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/" );

    def test_3_login(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('MemoryPalace', self.browser.title)
        element = self.browser.find_element_by_id("header_modal_L|R")
        element.click()
        element = self.browser.find_element_by_id("tab_modal_login")
        element.click()
        element = self.browser.find_element_by_id("username")
        element.send_keys("testuser")
        element = self.browser.find_element_by_id("password")
        element.send_keys("testuser")
        self.browser.find_element_by_id("login_submit").submit()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/" );

if __name__ == '__main__':
    unittest.main()
