from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.main_browser import MainBrowser
from igp.service.modifier.modifier import BaseModifier
from igp.util.exceptions import LoginDetailsError
from igp.util.events import AccountNameUpdatedEvent, ConfirmedLogInEvent, Event
from igp.util.tools import click, output
from igp.util.turbomode import turbo_wait


class BaseIGPaccount():
    listeners:list = []
    commands = []
    modifier = BaseModifier()
    username: str = ""
    password: str = ""
    driver: MainBrowser = None
    logged_acc = None
    confirmed_valid = False
    window = None
    login_url = "https://igpmanager.com/app/p=login"
    
    
    def __init__(self, username:str, password:str):
        self.initialised = False
        try:
            self.isclean(username)
            self.isclean(password)
        except LoginDetailsError as e:
            raise e
                 
        self.driver = MainBrowser.get_instance()
        self.set_details(username, password)
        self.initialised = True


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
    
    
    def add_to_listeners(object):
        BaseIGPaccount.listeners.append(object)
        
        
    def changed(self, event:Event):
        for listener in BaseIGPaccount.listeners:
            listener.handle(event)
        

    def set_details(self, username:str, password:str):
        if self.logged_in():
            self.log_out()
        self.username = username
        self.password = password 
        self.confirmed_valid = False
        if self.initialised:
            self.changed(AccountNameUpdatedEvent(self, self))

     
    def login(self):
        if self.logged_in():
            output(f"Tried to log into of account {self.return_name()} which was already logged in", log_only=True)
            return

        if BaseIGPaccount.logged_acc:
            BaseIGPaccount.logged_acc.log_out()
        output(f"Trying to login to {self.username} account", log_only=True)

        # create a new tab for this user
        self.window = self.driver.open_window(self.login_url)
        turbo_wait()
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "loginUsername")))
        elemUser = self.driver.find_element(By.ID, "loginUsername")
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "loginPassword")))
        elemPW = self.driver.find_element(By.ID, "loginPassword")
        elemUser.clear()
        elemPW.clear()
        elemUser.send_keys(self.username)
        elemPW.send_keys(self.password)
        elemPW.send_keys(Keys.RETURN)
        turbo_wait()

        login_success = ec.visibility_of_element_located((By.ID, "header"))
        login_fail = ec.any_of(ec.presence_of_element_located((By.XPATH, "//*[contains(text(),'not found or is inactive')]")),
                               ec.presence_of_element_located((By.XPATH, "//*[contains(text(),'Username & Password do not match')]")))
        WebDriverWait(self.driver, 10).until(ec.any_of(login_success, login_fail))

        if login_fail(self.driver):
            output("Details were invalid. Please set them again", log_only=True)
            self.reset_window()
        else:
            BaseIGPaccount.logged_acc = self
            output(f"Logged in to {self.return_name()}", log_only=True)
            if not self.confirmed_valid:
                self.confirmed_valid = True
                self.changed(ConfirmedLogInEvent(self, self))
            
            self.confirmed_valid = True
            

    def log_out(self):
        if not self.logged_in():
            output(f"Tried to log out of account {self.return_name()} which was already logged out", log_only=True)
            return
       
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "headerProfile")))
        click(self.driver.find_element(By.ID, "headerProfile"))

        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "mLogout")))
        click(self.driver.find_element(By.ID, "mLogout"))
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "btn")))
        logout_confirm = self.driver.find_elements(By.CLASS_NAME, "btn")[-1]
        click(logout_confirm)
        BaseIGPaccount.logged_acc = None
        self.reset_window()
        turbo_wait()
        
        output(f"Logged out of {self.return_name()} account", log_only=True)


    def reset_window(self):
        self.driver.close_specific_window(self.window)
        self.window = None
    
    
    def hit_save(self):
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "action")))
        save = self.driver.find_element(By.ID, "action")
        click(save)
        turbo_wait()
        

    def close_message(self):
        return "Please log in to use this feature."


    def return_name(self):
        if not self.confirmed_valid:
            if not self.username:
                self.username = "-blank-"
            return "*" + self.username + "*"

        return self.username


    def logged_in(self):
        return self == BaseIGPaccount.logged_acc
    
    
    def __str__(self) -> str:
        return self.return_name()
    
    def help(self) -> str:
        return self.__str__()
    

    def tuto_skip(self):
        try:
            WebDriverWait(self.driver, 0.5).until(ec.presence_of_element_located((By.ID, "tutorial-container")))
        except:
            return
        
        tutocont = self.driver.find_element(By.ID, "tutorial-container")
        try:
            skip = tutocont.find_element(By.CLASS_NAME, "confirm")
            click(skip)
            tooltip = self.driver.find_elements(By.CLASS_NAME, "tTip")[0]
            tutodone = tooltip.find_elements(By.CLASS_NAME, "btn")[0]
            click(tutodone)
            return
        except:
            self.recursive_tuto_continue()


    def recursive_tuto_continue(self):
        '''Keep clicking continue until there are no more to click'''
        try:
            tuto_continue = self.driver.find_element(By.CLASS_NAME, "tutorial-continue")
            click(tuto_continue)
            self.recursive_tuto_continue()
        except:
            return


