from igp.service.commands.car_repair import CarRepairCommands
from igp.service.commands.driver_train import DriverTrainCommands
from igp.service.commands.set_strategy import SetupCommands


class IGPaccount(CarRepairCommands, DriverTrainCommands, SetupCommands):
    pass
