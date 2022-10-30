import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.util.decorators import igpcommand
from igp.util.tools import output


class CarRepairCommands(BaseIGPaccount):
    repair_page = "https://igpmanager.com/app/p=cars&tab=repair"
    FIX_TYPES = [["c1PartSwap", "c2PartSwap"], ["c1EngSwap", "c2EngSwap"]]
    
    
    @igpcommand(alias="test task") 
    def just_tried_this(self):
        output(f'You just tried this with {self.return_name()}')
        
    
    @igpcommand(alias="fix cars", page=repair_page)
    def fix_cars(self):   
        #fix every part of both cars
        #only fix car condition if below 80%
        self.fix_car(0, 0, 80)
        self.fix_car(1, 0, 80)
        #always fix engine if below 100%
        self.fix_car(0, 1, 100)
        self.fix_car(1, 1, 100)


    @igpcommand(alias="fix car", page=repair_page)
    def fix_car(self, car_num=0, fix_type=0, threshold=0):
        '''repairs a part of the car
            car_num indicates which car we should look at, 0 for c1, 1 for c2
            bar_num indicates whether to look at car or engine condition
        '''
        car_id = self.FIX_TYPES[fix_type][car_num]
        
        if threshold > 100:
            threshold = 100

        # don't repair if above threshold%   
        if self.car_health(car_num, fix_type) >= threshold:
            return

        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, car_id)))
        # igp has silly on screen blocking element which can temporarily
        # prevent clicks, so we wait for that to go and try again
        try:
            self.driver.find_element(By.ID, car_id).click()
        except:
            time.sleep(1)
            self.driver.find_element(By.ID, car_id).click()

        tooltip = self.driver.find_elements(By.CLASS_NAME, "tTip")[0]
        fix_car = tooltip.find_elements(By.CLASS_NAME, "btn")[0]
        fix_car.click()
        

    def car_health(self, car_num=0, bar_num=0) -> int:
        '''
            returns percentage of car health
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
        prefixes = [["Car1", "Eng1"],["Car2","Eng2"]]
        message = ""
        for car in range(2):
            for type in range(2):
                health = self.car_health(car, type)
                message += f"{prefixes[car][type]}: {health}, "
              
        output(message[:-2])
    
