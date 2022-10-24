from os import path
from igp.service.igpaccount import IGPaccount
from igp.util.events import Event
from util.utils import join


ACCDIR = ("igp","config","accounts.txt")
FORMATMSG = "Please format the accounts file such that there is:\nOne account per line.\nline looks like email;password;"


class AccountIterator():
    accounts = []
    singleton = None
    listeners = []
    
    def get_instance(*args, **kwargs):
        if not AccountIterator.singleton:
            AccountIterator.singleton = AccountIterator(*args, **kwargs)
        
        return AccountIterator.singleton
    
    def __init__(self, accounts:list=[], minimised=True):
        self.accounts:list = []
        self.index = -1
        self.collect_accounts(minimised)
        
        for account in accounts:
            self.add_account(account)
            
        if len(self.accounts) >= 0:
            self.index = 0


    def acc_dir(self):
        return join(*ACCDIR, uplevel=2)


    def collect_accounts(self, minimised=False):
        with open(self.acc_dir(), "r") as acc_file:
            lines = acc_file.readlines()[1:]
            for index, line in enumerate(lines):
                data = line.split(";")
                if len(data) > 3:
                    print(f"\nToo many semi-colons on line {index}.\n{FORMATMSG}")

                elif len(data) < 3:
                    print(f"\nNot enough semi-colons on line {index}.\n{FORMATMSG}")

                else:
                    valid = True
                    for datum in data:
                        if "\\" in datum:
                            print(f"{datum} has invalid characters")
                            valid = False
                            break

                    if valid:
                        self.add_account(IGPaccount(data[0], data[1], minimised))               
                

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

        unique = True
        for index, added_account in enumerate(self.accounts):
            # password has potentially been updated, replace old account details
            if added_account.username == account.username:
                self.accounts[index] = account
                unique = False
                break

        if unique:
            self.accounts.append(account)
            
        self.changed()


    def add_make_current(self, account: IGPaccount):
        if not account:
            return

        self.add_account(account)
        while self.current() != account:
            next(self)


    def add_to_listeners(self, object):
        self.listeners.append(object)
        
        
    def changed(self):
        for listener in self.listeners:
            listener.handle(Event.ACCOUNTS_UPDATED)