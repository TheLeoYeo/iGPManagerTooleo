from igp.service.commands.car_repair import CarRepairCommands
from igp.service.commands.driver_train import DriverTrainCommands
from igp.service.commands.set_setup import SetupCommands
from igp.service.commands.set_strategy import StrategyCommands


class IGPaccount(CarRepairCommands, DriverTrainCommands, SetupCommands, StrategyCommands):
    pass
