from igp.service.commands.car_repair import CarRepairCommands
from igp.service.commands.driver_train import DriverTrainCommands


class IGPaccount(CarRepairCommands, DriverTrainCommands):
    pass
