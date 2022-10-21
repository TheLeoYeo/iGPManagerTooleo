from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.main_browser import MainBrowser
from igp.util.tools import output_with_message
from igp.util.exceptions import LoginDetailsError


class BaseIGPaccount():
    commands = []
    username: str = ""
    password: str = ""
    driver: MainBrowser = None
    logged_acc = None
    window = None
    login_url = "https://igpmanager.com/app/p=login"
    
    
    def __init__(self, username:str, password:str, minimised:bool=False):
        try:
            self.isclean(username)
            self.isclean(password)
        except LoginDetailsError as e:
            raise e
                 
        
        self.driver = MainBrowser.get_instance(minimised)
        self.set_details(username, password)


    def isclean(self, text: str):
        org_length = len(text)
        if org_length == 0:
            raise LoginDetailsError
        
        filtered = text.replace("\\", "")
        if len(filtered) < org_length:
            raise LoginDetailsError

        filtered = text.replace(";", "")
        if len(filtered) < org_length:
            raise LoginDetailsError

        return True
        

    def set_details(self, username:str, password:str):
        if self.logged_in():
            self.log_out()
        self.username = username
        self.password = password 

     
    def login(self):
        if self.logged_in():
            output_with_message("logged in already")
            return

        if BaseIGPaccount.logged_acc:
            BaseIGPaccount.logged_acc.log_out()
        output_with_message(f"Trying to login to {self.username} account")

        # create a new tab for this user
        self.window = self.driver.open_window(self.login_url)
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "loginUsername")))
        elemUser = self.driver.find_element(By.ID, "loginUsername")
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "loginPassword")))
        elemPW = self.driver.find_element(By.ID, "loginPassword")
        elemUser.clear()
        elemPW.clear()
        elemUser.send_keys(self.username)
        elemPW.send_keys(self.password)
        elemPW.send_keys(Keys.RETURN)

        login_success = ec.visibility_of_element_located((By.ID, "header"))
        login_fail = ec.any_of(ec.presence_of_element_located((By.XPATH, "//*[contains(text(),'not found or is inactive')]")),
                               ec.presence_of_element_located((By.XPATH, "//*[contains(text(),'Username & Password do not match')]")))
        WebDriverWait(self.driver, 10).until(ec.any_of(login_success, login_fail))

        if login_fail(self.driver):
            output_with_message("Details were invalid. Please set them again")
            self.reset_window()
        else:
            BaseIGPaccount.logged_acc = self
            output_with_message(f"We've logged in to {self.username}")
        
        
    def just_tried_this(self):
        self.driver.to_window()
        output_with_message(f'You just tried this with {self.return_name()}')


    def log_out(self):
        if not self.logged_in():
            output_with_message("You've already logged out of this account!")
            return
       
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "headerProfile")))
        self.driver.find_element(By.ID, "headerProfile").click()
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "mLogout")))
        self.driver.find_element(By.ID, "mLogout").click()
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "btn")))
        logout_confirm = self.driver.find_elements(By.CLASS_NAME, "btn")[-1]
        logout_confirm.click()
        BaseIGPaccount.logged_acc = None
        self.reset_window()
        
        output_with_message(f"Just closed the tab for {self.username} account")


    def reset_window(self):
        self.driver.close_specific_window(self.window)
        self.window = None
        

    def close_message(self):
        return "Please log in to use this feature."


    def return_name(self):
        if not self.logged_in():
            if not self.username:
                self.username = "-blank-"
            return self.username + "***"

        return self.username


    def logged_in(self):
        return self == BaseIGPaccount.logged_acc
    
    def __str__(self) -> str:
        return self.username
