import atexit

from igp.service.igpaccount import IGPaccount
from igp.util.events import AccountAddedEvent, AccountNameUpdatedEvent, AccountRemovedEvent, Event
from igp.util.tools import output, replace_if_gone
from util.utils import join


ACCDIR = ("igp","config","accounts.txt")
FORMATMSG = "Please format the accounts file such that there is:\nOne account per line.\nline looks like email;password;"


class AccountIterator():
    singleton = None
    listeners = []
    
    def get_instance(*args, **kwargs):
        if not AccountIterator.singleton:
            AccountIterator.singleton = AccountIterator(*args, **kwargs)
        
        return AccountIterator.singleton
    
    
    def __init__(self, accounts:list=[], minimised=True):
        self.default_file = "email;password;\n"
        replace_if_gone(self.acc_dir(), self.default_file)
        self.accounts:list[IGPaccount] = []
        self.index = -1
        
        for account in accounts:
            self.add_account(account)
            
        if len(self.accounts) >= 0:
            self.index = 0
            
        self.collected_accounts = False


    def acc_dir(self):
        return join(*ACCDIR, uplevel=2)


    def collect_accounts(self, minimised=True):
        with open(self.acc_dir(), "r") as acc_file:
            lines = acc_file.readlines()[1:]
            for index, line in enumerate(lines):
                data = line.split(";")
                if len(data) > 3:
                    output(f"\nToo many semi-colons on line {index}.\n{FORMATMSG}")

                elif len(data) < 3:
                    output(f"\nNot enough semi-colons on line {index}.\n{FORMATMSG}")

                else:
                    valid = True
                    for datum in data:
                        if "\\" in datum:
                            output(f"{datum} has invalid characters")
                            valid = False
                            break

                    if valid:
                        self.add_account(IGPaccount(data[0], data[1], minimised))
                        
        self.collected_accounts = True
                        
                                                
    def update_file(self):
        if not self.collected_accounts:
            return
        
        open(self.acc_dir(), "w").close()
        with open(self.acc_dir(), "a") as acc_file:
            acc_file.write("email;password;\n")
            for account in self.accounts:
                acc_file.write(f"{account.username};{account.password};\n")
                

    def next(self):
        self.index = (self.index + 1) % len(self.accounts)
        return self.current()


    def prev(self):
        self.index = (self.index - 1) % len(self.accounts)
        return self.current()


    def current(self) -> IGPaccount:
        try:
            return self.accounts[self.index]
        except:
            return None


    def add_account(self, account: IGPaccount):
        if not account:
            return

        for added_account in self.accounts:
            # password has potentially been updated, replace old account details
            if added_account.username == account.username:
                added_account.set_details(account.username, account.password)
                self.changed(AccountNameUpdatedEvent(self, added_account))
                return

        self.accounts.append(account)
        self.changed(AccountAddedEvent(self, account))
             
              
    def remove_account(self, account: IGPaccount):
        if account in self.accounts:
            self.accounts.remove(account)
            self.changed(AccountRemovedEvent(self, account))


    def remove_accounts(self, accounts: list[IGPaccount]):
        for account in accounts:
            self.remove_account(account)
           
            
    def add_make_current(self, account: IGPaccount):
        if not account:
            return

        self.add_account(account)
        while self.current() != account:
            next(self)


    def add_to_listeners(self, object):
        self.listeners.append(object)
        
        
    def changed(self, event:Event):
        for listener in self.listeners:
            listener.handle(event)
            
            
def exit_handler():
    AccountIterator.get_instance().update_file()

atexit.register(exit_handler)