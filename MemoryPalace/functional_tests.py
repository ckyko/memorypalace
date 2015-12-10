from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import unittest

keys_dict = {"username":"testuser", "email":"testuser@testemail.com", "password":"testuser", "palace_name":"testuser_palace", "room_name":"testuser_palace_room", "img_loc":"/home/satya/Pictures/Selection_006.png"  }
class NewVisitorTest(unittest.TestCase):


    '''
    Function defined below are to be called by test functions
    '''
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def register(self):
        '''
        This function will register a user from the dictionary onto the website
        '''
        #Register user
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='#modal_register_login']")
        element.click()
        element = self.browser.find_element_by_id("tab_modal_register")
        element.click()
        element = self.browser.find_element_by_id("id_username")
        element.send_keys(keys_dict["username"])
        element = self.browser.find_element_by_id("email")
        element.send_keys(keys_dict["email"])
        element = self.browser.find_element_by_id("id_password1")
        element.send_keys(keys_dict["password"])
        element = self.browser.find_element_by_id("id_password2")
        element.send_keys(keys_dict["password"])
        self.browser.find_element_by_id("register_submit").submit()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/" )

    def login(self):
        '''
        This function will let a user login to the website
        '''
        #Login User
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='#modal_register_login']")
        element.click()
        element = self.browser.find_element_by_id("tab_modal_login")
        element.click()
        element = self.browser.find_element_by_id("username")
        element.send_keys(keys_dict["username"])
        element = self.browser.find_element_by_id("password")
        element.send_keys(keys_dict["password"])
        self.browser.find_element_by_id("login_submit").submit()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/" )

    def logout(self):
        '''
        This function will let a user logout to the website
        '''
        if self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='/logout']"):
            self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='/logout']").click()

    def Palace_add(self):
        '''
        This function lets user create a palace
        '''
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element = self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']")
        element.click()
        element = self.browser.find_element_by_id("private_add_palace_card")
        element.click()
        element = self.browser.find_element_by_id("id_palaceName")
        element.send_keys(keys_dict["palace_name"])
        self.browser.find_element_by_id("createPalace_submit").submit()

    def Palace_delete(self):
        '''
        This function lets user delete a palace
        '''
        self.browser.get('http://localhost:8000')
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element = self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']")
        element.click()
        self.assertTrue('testuser_palace', self.browser.find_element_by_tag_name("p"))
        element = self.browser.find_element_by_id("delete_"+keys_dict["palace_name"])
        element.click()

    def Room_add(self):
        '''
        This function lets user create a room
        '''
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element = self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']")
        element.click()
        element = self.browser.find_element_by_id("edit_"+keys_dict["palace_name"])
        element.click()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/MemoryPalace/?palaceName=testuser_palace" )
        element = self.browser.find_element_by_id("background_add")
        element.click()
        element = self.browser.find_element_by_id("id_roomName")
        element.send_keys(keys_dict["room_name"])
        element = self.browser.find_element_by_id("id_backgroundImage")
        element.click()
        element.send_keys(keys_dict["img_loc"])
        element.send_keys(Keys.RETURN)
        self.browser.find_element_by_id("createRoom_submit").submit()

    def Room_delete(self):
        '''
        This function lets user delete a room
        '''
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element = self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']")
        element.click()
        element = self.browser.find_element_by_id("edit_"+keys_dict["palace_name"])
        element.click()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/MemoryPalace/?palaceName=testuser_palace" )
        element=self.browser.find_element_by_id(keys_dict["palace_name"]+"_"+keys_dict["room_name"])
        self.browser.get('http://127.0.0.1:8000/deleteRoom?palaceName='+keys_dict['palace_name']+'&roomName='+keys_dict['room_name'])
    '''
    Funtions defined below are test functions
    '''
    def test_1_User_Register_Login(self):
        '''
        This function tests the homepage of the website and calls in register, login and logout functions
        '''
        #Load homepage
        self.browser.get('http://localhost:8000')
        self.assertIn('MemoryPalace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome!', header_text)
        self.register()
        self.login()
        self.logout()

    def test_2_palace_library(self):
        '''
        This function tests the palace library of the website
        '''
        self.browser.get('http://localhost:8000')
        element = self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library']")
        element.click()
        element=self.browser.find_element_by_class_name("disabled")
        action_chains = ActionChains(self.browser)
        action_chains.move_to_element(element)

    def test_3_private_palace_library(self):
        '''
        This function tests if palaces can be succesfully created
        '''
        self.browser.get('http://localhost:8000')
        self.login()
        self.Palace_add()
        element = self.browser.find_element_by_id("edit_"+keys_dict["palace_name"])
        element.click()
        self.assertEquals(self.browser.current_url, "http://localhost:8000/MemoryPalace/?palaceName=testuser_palace" )
        self.logout()

    def test_4_Memory_Palace(self):
        '''
        This function tests if rooms can be created under a palace
        '''
        self.browser.get('http://localhost:8000')
        self.login()
        self.Room_add()
        self.Room_delete()
        self.Palace_delete()
        self.logout()

if __name__ == '__main__':
    unittest.main()
