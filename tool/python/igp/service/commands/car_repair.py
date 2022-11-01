from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.util.decorators import igpcommand
from igp.util.tools import click, output
from igp.service.modifier.modifier import BaseModifier, IntegerField, OptionField


class RepairType(Enum):
    CAR = 0
    ENGINE = 1
    

class CarRepairCommands(BaseIGPaccount):
    repair_page = "https://igpmanager.com/app/p=cars&tab=repair"
    FIX_TYPES = [["c1PartSwap", "c2PartSwap"], ["c1EngSwap", "c2EngSwap"]]
    ALL_REP_TYPES = [RepairType.CAR, RepairType.ENGINE]

    @igpcommand(alias="test task") 
    def just_tried_this(self):
        output(f'You just tried this with {self.return_name()}')
        
    
    @igpcommand(alias="fix cars", page=repair_page,
                modifier=BaseModifier(IntegerField("eng_threshold", 0, 100, 100), IntegerField("part_threshold", 0, 100, 70)))
    def fix_cars(self, eng_threshold=99, part_threshold=80):
        """Repairs engine + parts of all cars
            Default wear threshold to fix parts is 70%
            Default wear threshold to fix engines is 100%"""
        
        #fix every part of both cars
        self.fix_car(0, RepairType.CAR, part_threshold)
        self.fix_car(1, RepairType.CAR, part_threshold)
        self.fix_car(0, RepairType.ENGINE, eng_threshold)
        self.fix_car(1, RepairType.ENGINE, eng_threshold)


    @igpcommand(alias="fix car", page=repair_page, 
                modifier=BaseModifier(IntegerField("car_num", 1, 2), OptionField("fix_type", ALL_REP_TYPES), IntegerField("threshold", 0, 100, 100)))
    def fix_car(self, car_num=0, fix_type=RepairType, threshold=100):
        '''Repairs a specified part of a specific car
            car_num indicates which car we should look at, 1 for c1, 2 for c2
            fix_type indicates whether to look at car or engine condition
            threshold is how low the health needs to be to require fixing
            threshold default is 100%'''
        
        car_num -= 1
        
        car_id = self.FIX_TYPES[fix_type.value][car_num]
        
        if threshold > 100:
            threshold = 100

        # don't repair if above threshold%   
        if self.car_health(car_num, fix_type.value) >= threshold:
            return

        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, car_id)))
        click(self.driver.find_element(By.ID, car_id))

        tooltip = self.driver.find_elements(By.CLASS_NAME, "tTip")[0]
        fix_car = tooltip.find_elements(By.CLASS_NAME, "btn")[0]
        click(fix_car)
        

    def car_health(self, car_num=0, bar_num=0) -> int:
        '''returns percentage of car health
            car_num indicates which car we should look at, 0 for c1, 1 for c2
            bar_num indicates whether to look at car (0) or engine (1) condition
        '''

        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "repair")))
        table = self.driver.find_element(By.ID, "repair")
        try:
            car = table.find_elements(By.CLASS_NAME, "eight")[car_num]
        except:
            return "NAN"
        
        bar = car.find_elements(By.CLASS_NAME, "ratingBar")[bar_num]
        health_bar = bar.find_elements(By.TAG_NAME, "div")[0]
        health_text = health_bar.get_attribute("style")
        return int(health_text.split(": ")[1].split("%")[0])

   
    @igpcommand(alias="car health", page=repair_page)
    def all_car_health(self):
        '''Shows % of car and engine health for all cars'''
        
        prefixes = [["Car1", "Eng1"],["Car2","Eng2"]]
        message = ""
        for car in range(2):
            for type in range(2):
                health = self.car_health(car, type)
                message += f"{prefixes[car][type]}: {health}, "
              
        output(message[:-2])
    
