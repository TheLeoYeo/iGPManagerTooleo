from igp.service.commands.car_repair import CarRepairCommands
from igp.service.commands.create_account import AccountCommands
from igp.service.commands.driver_train import DriverTrainCommands
from igp.service.commands.set_setup import SetupCommands
from igp.service.commands.set_strategy import StrategyCommands


class IGPaccount(CarRepairCommands, DriverTrainCommands, SetupCommands, StrategyCommands, AccountCommands):
    pass


def no_account():
    return "N/A"

#hard coded monitor account, 
MONITOR_ACCOUNT = IGPaccount("leobot@bot.com","botForLeosMonitoring")
MONITOR_ACCOUNT.return_name = no_account