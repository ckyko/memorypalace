from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def register(self):
        #Register user
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='#modal_register_login']")
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
        self.assertEquals(self.browser.current_url, "http://localhost:8000/" )

    def login(self):
        #Login User
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='#modal_register_login']")
        element.click()
        element = self.browser.find_element_by_id("tab_modal_login")
        element.click()
        element = self.browser.find_element_by_id("username")
        element.send_keys("testuser")
        element = self.browser.find_element_by_id("password")
        element.send_keys("testuser")
        self.browser.find_element_by_id("login_submit").submit()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/" )

    def logout(self):
        if self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='/logout']"):
            self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='/logout']").click()

    def test_1_User_Register_Login(self):
        #Load homepage
        self.browser.get('http://localhost:8000')
        self.assertIn('MemoryPalace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome!', header_text)
        self.register()
        self.login()
        self.logout()

    def test_2_palace_library(self):
        self.browser.get('http://localhost:8000')
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element=self.browser.find_element_by_class_name("disabled")
        action_chains = ActionChains(self.browser)
        action_chains.move_to_element(element)

    def test_3_private_palace_add(self):
        self.browser.get('http://localhost:8000')
        self.login()
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element = self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']")
        element.click()
        element = self.browser.find_element_by_id("private_add_palace_card")
        element.click()
        element = self.browser.find_element_by_id("id_palaceName")
        element.send_keys("testuser_palace")
        self.browser.find_element_by_id("createPalace_submit").submit()
        element = self.browser.find_element_by_id("private_palace_edit")
        element.click()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/MemoryPalace/?palaceName=testuser_palace" )
        self.logout()

    def test_4_Memory_Palace(self):
        self.browser.get('http://localhost:8000')
        self.login()
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element = self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']")
        element.click()
        element = self.browser.find_element_by_id("private_palace_edit")
        element.click()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/MemoryPalace/?palaceName=testuser_palace" )
        element = self.browser.find_element_by_id("background_add")
        element.click()
        element = self.browser.find_element_by_id("id_roomName")
        element.send_keys("testuser_palace_room")
        element = self.browser.find_element_by_id("id_backgroundImage")
        element.click()
        element.send_keys("/home/satya/Pictures/Selection_006.png")
        element.send_keys(Keys.RETURN)
        self.browser.find_element_by_id("createRoom_submit").submit()
        self.logout()

if __name__ == '__main__':
    unittest.main()
