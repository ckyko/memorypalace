"""
test_functionality
Test most of the major functions of the project
"""
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

loc=os.getcwd()#get current location
keys_dict = {"username":"testuser", "email":"testuser@testemail.com", "password":"testuser",
             "palace_name":"testuser_palace", "room_name":"testuser_palace_room",
             "img_loc":loc+"/coreapp/static/images/previews/pre1.jpg"  }
class NewVisitorTest(unittest.TestCase):


    '''
    Function defined below are to be called by test functions
    '''
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(8)

    def tearDown(self):
        self.browser.quit()

    def register(self):
        '''
        This function will register a user from the dictionary onto the website
        '''
        #Register user
        #click on the Login|Register button on the nav bar
        self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='#modal_register_login']").click()
        #click on the Tab of register
        self.browser.find_element_by_id("tab_modal_register").click()
        #Enter the Username
        self.browser.find_element_by_id("id_username").send_keys(keys_dict["username"])
        #Enter the Email
        self.browser.find_element_by_id("email").send_keys(keys_dict["email"])
        #Enter the Password
        self.browser.find_element_by_id("id_password1").send_keys(keys_dict["password"])
        #Re-Enter the Password
        self.browser.find_element_by_id("id_password2").send_keys(keys_dict["password"])
        #Submit the Registration
        self.browser.find_element_by_id("register_submit").submit()
        #Check if redirected to hompage after succesfull Registration
        self.assertEquals(self.browser.current_url, "http://localhost:8000/#modal_login" )

    def login(self):
        '''
        This function will let a user login to the website
        '''
        #Login User
        #click on the Login|Register button on the nav bar
        self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@href='#modal_register_login']").click()
        #click on the Tab of Login
        self.browser.find_element_by_id("tab_modal_login").click()
        #Enter the Username
        self.browser.find_element_by_id("username").send_keys(keys_dict["username"])
        #Enter the Password
        self.browser.find_element_by_id("password").send_keys(keys_dict["password"])
        #Submit login
        self.browser.find_element_by_id("login_submit").submit()
        #Check if redirected to the homepage after succesfull login
        self.assertEquals(self.browser.current_url, "http://localhost:8000/" )

    def logout(self):
        '''
        This function will let a user logout to the website
        '''
        #Check if logged in, if so logout
        if self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@data-activates='testuser']"):
            self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[3]/a[@data-activates='testuser']").click()
            self.browser.find_element_by_id('testuser').click()

    def Palace_add(self):
        '''
        This function lets user create a palace
        '''
        #click on Palace Library of nav bar
        self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library/']").click()
        #click on the Private Tab
        self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']").click()
        #click on the add button of Private Tab
        self.browser.find_element_by_id("private_add_palace_card").click()
        #Enter the Palace Name
        self.browser.find_element_by_id("id_palaceName").send_keys(keys_dict["palace_name"])
        #Submit the form
        self.browser.find_element_by_id("createPalace_submit").submit()

    def Palace_delete(self):
        '''
        This function lets user delete a palace
        '''
        #Go to the homepage
        self.browser.get('http://localhost:8000')
        #click on Palace Library of nav bar
        self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library/']").click()
        #click on the Private Tab
        self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']").click()
        #Check if it conatains a palace with name 'testuser_palace'
        self.assertTrue('testuser_palace', self.browser.find_element_by_tag_name("p"))
        #click on delete button to delete the palace#Check if in Memory Palace under specific room
        self.browser.find_element_by_id("delete_"+keys_dict["palace_name"]).click()

    def Room_add(self):
        '''
        This function lets user create a room
        '''
        #click on Palace Library of nav bar
        self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library/']").click()
        #click on the Private Tab
        self.browser.find_element_by_xpath("//div/ul[@class='tabs']/li[2]/a[@href='#Private']").click()
        #click on edit button to edit the palace
        self.browser.find_element_by_id("edit_"+keys_dict["palace_name"]).click()
        #Check if it gets redirected to the Memory Palace
        self.assertEquals(self.browser.current_url,
                          "http://localhost:8000/MemoryPalace/?palaceName=testuser_palace")
        #click on the add button to add room
        self.browser.find_element_by_id("background_add").click()
        #Enter the room name
        self.browser.find_element_by_id("id_roomName").send_keys(keys_dict["room_name"])
        #Enter the location of the backround image to be added
        self.browser.find_element_by_id("id_backgroundImage").send_keys(keys_dict["img_loc"])
        #Submit the form
        self.browser.find_element_by_id("createRoom_submit").submit()
        #Check if in Memory Palace under specific room
        self.assertEquals(self.browser.current_url, "http://localhost:8000/MemoryPalace/?palaceName="
                          +keys_dict['palace_name']+'&roomName='+keys_dict['room_name'])

    def Room_delete(self):
        '''
        This function lets user delete a room
        '''
        #Delete the room
        self.browser.get('http://127.0.0.1:8000/deleteRoom?palaceName='+keys_dict['palace_name']
                         +'&roomName='+keys_dict['room_name'])

    '''
    Funtions defined below are test functions
    '''
    def test_1_User_Register_Login(self):
        '''
        This function tests the homepage of the website and calls in register, login and logout functions
        '''
        #Load homepage
        self.browser.get('http://localhost:8000')
        #Check for title of the browser
        self.assertIn('MemoryPalace', self.browser.title)
        #Check for heading of the page
        self.assertIn('Welcome!', self.browser.find_element_by_tag_name('h1').text)
        #Call register function
        self.register()
        self.browser.get('http://localhost:8000')
        #Call login function
        self.login()
        #Call logout function
        self.logout()

    def test_2_palace_library(self):
        '''
        This function tests the palace library of the website
        '''
        #Load homepage
        self.browser.get('http://localhost:8000')
        #click on Palace Library of nav bar
        self.browser.find_element_by_xpath("//nav/div/ul[@class='right hide-on-med-and-down']/li[2]/a[@href='/palace_library/']").click()
        #Check if Private tab is disabled
        element = self.browser.find_element_by_class_name("disabled")
        action_chains = ActionChains(self.browser)
        action_chains.move_to_element(element)

    def test_3_private_palace_library(self):
        '''
        This function tests if palaces can be succesfully created
        '''
        #Load homepage
        self.browser.get('http://localhost:8000')
        #Call login function
        self.login()
        #Call add function
        self.Palace_add()
        #click on edit button of palace
        self.browser.find_element_by_id("edit_"+keys_dict["palace_name"]).click()
        #Check if redirected to Memory Palace
        self.assertEquals(self.browser.current_url, "http://localhost:8000/MemoryPalace/?palaceName=testuser_palace")
        #Call logout function
        self.logout()

    def test_4_Memory_Palace(self):
        '''
        This function tests if rooms can be created under a palace
        '''
        #Load homepage
        self.browser.get('http://localhost:8000')
        #Call login function
        self.login()
        #Call Room_add function
        self.Room_add()
        #Call Room_delete function
        self.Room_delete()
        #Call Palace_delete function
        self.Palace_delete()
        #Call logout function
        self.logout()

if __name__ == '__main__':
    unittest.main()
