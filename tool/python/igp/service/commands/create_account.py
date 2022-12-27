from faker import Faker

from igp.service.base_igp_account import BaseIGPaccount
from igp.service.commands.tasks import Categories
from igp.util.decorators import CommandType, simpleigpcommand
from igp.util.tools import click, output
from igp.service.modifier.modifier import *


class AccountCommands(BaseIGPaccount):
    sign_up_page = "https://igpmanager.com/app/p=join"
    fk = Faker("en_GB")
    
    @simpleigpcommand(alias="create account", page=sign_up_page, category=Categories.MISC, type=CommandType.ACCOUNTLESS,
            modifier=BaseModifier(TextField("first_name", fk.first_name), TextField("last_name", fk.last_name), 
                                  TextField("email", fk.email), TextField("password", fk.word)))
    def sign_up(self, first_name:str=fk.first_name(), last_name:str=fk.last_name(), email:str=fk.email(), password:str=fk.word()):
        '''Creates a new account with the given details
        Leave the details the way they are to generate an account with random details
        If the email conflicts, no account will be created'''
        
        print(f"{first_name}, {last_name}, {email}, {password}")