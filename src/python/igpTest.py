from igp.service.accounts import AccountIterator
from igp.service.options import options
from igp.util.tools import output_with_message


def main():
    output_with_message('''Welcome to the app.
    If log in fails, navigate to account, set details again -
    then attempt to log in again.
    Logging in unlocks iGP web features such as training drivers
    Users that aren't logged in will have asterisks next to the name
    e.g. username*** ''')

    # add the accounts to accounts list
    # put 'from igp.service.igpaccount import IGPaccount' at the top
    # account = IGPaccount()
    # acc_iter = AccountIterator([account])

    # to minimise window add minimised paramter to the constructor
    # acc_iter = AccountIterator(..., minimised=True)
    # by default it is set to False
    acc_iter = AccountIterator(minimised=True)

    while not options(acc_iter):
        pass


if __name__ == "__main__":
    main()
