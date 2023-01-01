from faker import Faker

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.service.commands.tasks import Categories
from igp.service.modifier.modifier import *
from igp.util.decorators import CommandType, simpleigpcommand
from igp.util.events import AccountCreatedEvent, Event
from igp.util.tools import click, output
from igp.util.turbomode import turbo_wait


class AccountCommands(BaseIGPaccount):
    sign_up_page = "https://igpmanager.com/app/p=join"
    fk = Faker("en_GB")
    listeners = []
    
    @simpleigpcommand(alias="create account", page=sign_up_page, category=Categories.MISC, type=CommandType.ACCOUNTLESS,
            modifier=BaseModifier(TextField("first_name", fk.first_name), TextField("last_name", fk.last_name), 
                                  TextField("email", fk.email), TextField("password", fk.word)))
    def sign_up(self, first_name:str=fk.first_name(), last_name:str=fk.last_name(), email:str=fk.email(), password:str=fk.word()):
        '''Creates a new account with the given details
        Leave the details the way they are to generate an account with random details
        If the email conflicts, no account will be created'''
        
        
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        for input in inputs:
            name = input.get_attribute("name")
            if name == "nameL":
                input.send_keys(first_name)
            
            elif name == "nameF":
                input.send_keys(last_name)
            
            elif name == "email":
                input.send_keys(email)
                
            elif name == "password":
                input.send_keys(password)
                
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "submit")))
        submitbutton = self.driver.find_element(By.CLASS_NAME, "submit")
        
        signup_success = self.find_text_on_page("Team name")
        signup_fail = ec.any_of(self.find_text_on_page("You must enter a First name"),
                                self.find_text_on_page("You must enter a Surname"),
                                self.find_text_on_page("username or email is already in use"),
                                self.find_text_on_page("You must enter a valid Email address"),
                                self.find_text_on_page("You must enter a Password"))
        
        click(submitbutton)
        WebDriverWait(self.driver, 20).until(ec.any_of(signup_success, signup_fail))
        if signup_fail(self.driver):
            email_test = self.find_text_on_page("username or email is already in use")
            if email_test(self.driver):
                output("Email was already in use, use another one")
            else:
                output("Sign up attempt failed. Please enter valid details")
            return
        
        turbo_wait()
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "tutorial-continue")))
        tuto_continue = self.driver.find_element(By.CLASS_NAME, "tutorial-continue")
        # click opening tuto button
        click(tuto_continue)
        
        # click for team name
        tuto_continue = self.driver.find_element(By.CLASS_NAME, "tutorial-continue")
        click(tuto_continue)
        
        # click for nationality
        tuto_continue = self.driver.find_element(By.CLASS_NAME, "tutorial-continue")
        click(tuto_continue)
        
        # click for music and team logo
        tuto_continue = self.driver.find_element(By.CLASS_NAME, "tutorial-continue")
        click(tuto_continue)
        
        content = self.driver.find_element(By.ID, "page-content")
        submit_container = content.find_elements(By.CLASS_NAME, "sixteen")[1]
        submit_button = submit_container.find_element(By.TAG_NAME, "a")
        click(submit_button)
        turbo_wait()
        
        output(f"Created acc fn:{first_name}, ln:{last_name}, e:{email}, p:{password}")
        
        # some fucked shit I have to do to test login and add account to screen
        newacc = self.create(email, password)
        BaseIGPaccount.logged_acc = newacc
        self.driver.get("https://igpmanager.com/app/p=home&tab=news")
        self.tuto_skip()
        newacc.log_out()
        
        
    def find_text_on_page(self, text:str):
        return ec.presence_of_element_located((By.XPATH, "//*[contains(text(),'"+text+"')]"))
    
    
    def add_to_ac_listeners(object):
        AccountCommands.listeners.append(object)
        
        
    def changed(self, event:Event):
        for listener in self.listeners:
            listener.handle(event)