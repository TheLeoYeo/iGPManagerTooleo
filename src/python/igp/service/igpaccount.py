from igp.service.commands.car_repair import CarRepairCommands
from igp.service.commands.driver_train import DriverTrainCommands

COMMAND_FILES = (CarRepairCommands, DriverTrainCommands, )


class IGPaccount(*COMMAND_FILES):
    pass
