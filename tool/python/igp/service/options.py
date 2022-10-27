from igp.service.accounts import AccountIterator
from igp.service.igpaccount import IGPaccount
from igp.service.main_browser import MainBrowser
from igp.util.exceptions import LoginError
from igp.util.tools import output


def options(accounts: AccountIterator):
    account: IGPaccount = accounts.current()
    
    
    func = IGPaccount.commands["car_health"]
    output(func(account, 0, 0))
    choice = ""

    if account:
        if account.logged_in():
            # account has an igp window and has been logged into
            choice = input(f"account {account.return_name()}\nlogout/fix/health/train/trainuntil/try/setdetails/exit/up/down/add?: ")
        else:
            choice = input(f"account {account.return_name()}\nsetdetails/login/exit/up/down/add?: ")
    else:
        # no accounts have been added
        choice = input(f"No accounts added, 'add' account or 'exit'?: ")


    # choice has been made now we decide what to do
    if account:
        if not account.logged_in():
            # options specific to non-logged in account
            if choice == "login":
                account.login()
                return
        else:
            # options specific to logged in account
            if choice == "logout":
                account.log_out()
                return
            
        # options available to all accounts 
        if choice == "try":
            account.just_tried_this()
            return

        elif choice == "fix":
            account.fix_cars()
            return
        
        elif choice == "health":
            output(f"Health is: {account.car_health()}")
            return

        elif choice == "train":
            account.train_drivers()
            return

        elif choice == "trainuntil":
            try:
                threshold = int(input("Type minimum health all drivers can have after training"))
            except:
                output("Please type a number")
                return
            account.train_until_threshold(threshold)
            return
            
        elif choice == "setdetails":
            username = input("type username")
            password = input("type password")
            account.set_details(username, password)
            return

        elif choice == "up":
            output("swapped account")
            accounts.next()
            return

        elif choice == "down":
            output("swapped account")
            accounts.prev()
            return


    #options available all the time  
    if choice == "add":       
        username = input("type username")
        password = input("type password")
        try:
            new_account = IGPaccount(username, password)
            accounts.add_make_current(new_account)
        except LoginError:
            output("Username or password was wrong")
        return

    elif choice == "exit":
            output("Quitting")
            MainBrowser.get_instance().quit()
            return True
        
    else:
        output("Invalid command, try again")
        return
