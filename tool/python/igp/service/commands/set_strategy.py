from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.service.modifier.modifier import BaseModifier, NumberOfStintsField, OptionField, StintsField, TyresField
from igp.util.exceptions import NoSuchPilotError
from igp.util.tools import click, output
from igp.util.decorators import igpcommand
from util.utils import StintNumbers, Tyres


class DriverTab(Enum):
    DRIVER1 = 1
    DRIVER2 = 2


class StrategyCommands(BaseIGPaccount):
    strategy_page = "https://igpmanager.com/app/p=race&tab=strategy"
    ALL_DRV_TYPES = [DriverTab.DRIVER1, DriverTab.DRIVER2]
    
    
    tyresfield = TyresField("tyres")
    stintsfield = StintsField("stints")
    @igpcommand(alias="set all drivers' strat", page=strategy_page, help="Sets the strategy of all drivers in the account", 
                modifier=BaseModifier(NumberOfStintsField("num_of_stints", tyresfield, stintsfield), tyresfield, stintsfield))
    def set_all_strats(self, num_of_stints:StintNumbers=StintNumbers.THREE, tyres:list[Tyres]=[], stints:list[int]=[]):
        for driver in self.ALL_DRV_TYPES:
            self.set_driver_strat(driver, num_of_stints, tyres, stints)


    tyresfield2 = TyresField("tyres")
    stintsfield2 = StintsField("stints")
    @igpcommand(alias="set a driver's strat", page=strategy_page, help="Sets the strategy of a specific driver in the account", 
                modifier=BaseModifier(OptionField("driver", ALL_DRV_TYPES), NumberOfStintsField("num_of_stints", tyresfield2, stintsfield2), tyresfield2, stintsfield2))
    def set_driver_strat(self, driver:DriverTab=DriverTab.DRIVER1, num_of_stints:StintNumbers=StintNumbers.THREE, tyres:list[Tyres]=[], stints:list[int]=[]):
        try:
            self.grab_strat_tab(driver)
        except NoSuchPilotError:
            return
        
        form = self.driver.find_element(By.ID, f"d{driver.value}strategy")
        pit_element = form.find_element(By.ID, f"beginner-d{driver.value}PitsWrap")
        self.fix_pit_number(pit_element, len(tyres)-1)
        
        table = form.find_element(By.CLASS_NAME, "strategy")
        tyres_row = table.find_element(By.CLASS_NAME, "tyre")
        tyre_buttons = tyres_row.find_elements(By.TAG_NAME, "td")
        for index, tyre_button in enumerate(tyre_buttons):
            if "hidden" not in tyre_button.get_attribute("style"):
                click(tyre_button)
                stintform = self.driver.find_element(By.ID, "stintDialog")
                tyre = tyres[index]
                length = stints[index]
                select_tyre_row = stintform.find_element(By.CLASS_NAME, "tyre")
                button = select_tyre_row.find_element(By.ID, f"ts-{tyre.value}")
                click(button)
                length_row = stintform.find_element(By.CLASS_NAME, "igpNum")
                slength = self.set_row_value(length_row, length)
                output(f"stint length set to {slength}", log_only=True)
                
                submit = stintform.find_element(By.CLASS_NAME, "submit")
                click(submit)
                
        self.hit_save()
        
        
    tyresfield3 = TyresField("tyres")
    stintsfield3 = StintsField("stints")
    @igpcommand(alias="set tyres + auto-length", page=strategy_page, help="Sets the strategy of a specific driver in the account, stint lengths are automatic", 
                modifier=BaseModifier(OptionField("driver", ALL_DRV_TYPES), NumberOfStintsField("num_of_stints", tyresfield3, stintsfield3), tyresfield3))
    def set_driver_strat(self, driver:DriverTab=DriverTab.DRIVER1, num_of_stints:StintNumbers=StintNumbers.THREE, tyres:list[Tyres]=[]):
        try:
            self.grab_strat_tab(driver)
        except NoSuchPilotError:
            return
        
        form = self.driver.find_element(By.ID, f"d{driver.value}strategy")
        pit_element = form.find_element(By.ID, f"beginner-d{driver.value}PitsWrap")
        self.fix_pit_number(pit_element, len(tyres)-1)
        
        table = form.find_element(By.CLASS_NAME, "strategy")
        tyres_row = table.find_element(By.CLASS_NAME, "tyre")
        tyre_buttons = tyres_row.find_elements(By.TAG_NAME, "td")
        for index, tyre_button in enumerate(tyre_buttons):
            if "hidden" not in tyre_button.get_attribute("style"):
                click(tyre_button)
                stintform = self.driver.find_element(By.ID, "stintDialog")
                tyre = tyres[index]
                select_tyre_row = stintform.find_element(By.CLASS_NAME, "tyre")
                button = select_tyre_row.find_element(By.ID, f"ts-{tyre.value}")
                click(button)
                
                submit = stintform.find_element(By.CLASS_NAME, "submit")
                click(submit)
                
        self.hit_save()
        
    
    def grab_strat_tab(self, tab:DriverTab):
        num = tab.value
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, f"driver{num}Strategy")))
        button = self.driver.find_element(By.ID, f"driver{num}Strategy")
        if "disabled" in button.get_attribute("class"):
            raise NoSuchPilotError()

        click(button)
    
    
    def fix_pit_number(self, pit_element:WebElement, numpits:int):
        current = self.elem_to_num(pit_element)
        if current == numpits:
            return current
        
        decrement = pit_element.find_element(By.CLASS_NAME, "minus")
        increment = pit_element.find_element(By.CLASS_NAME, "plus")
           
        # if clickable and still needs reducing, reduce value
        while "disabled" not in decrement.get_attribute("class") and numpits < self.elem_to_num(pit_element):
            click(decrement)
            
        current = self.elem_to_num(pit_element)
        if current == numpits:
            return current
            
        # if clickable and still needs increasing, increase value
        while "disabled" not in increment.get_attribute("class") and numpits > self.elem_to_num(pit_element):
            click(increment)
            
        return self.elem_to_num(pit_element)
       
        
    def elem_to_num(self, pitnumber:WebElement):
        return int(pitnumber.text.split(" ")[0])

    
    def set_row_value(self, row:WebElement, value:int) -> int:
        current_box = row.find_element(By.CLASS_NAME, "num")
        
        current = int(current_box.text)
        if current == value:
            return current
               
        decrement = row.find_element(By.CLASS_NAME, "minus")
        increment = row.find_element(By.CLASS_NAME, "plus")

        # start by trying to make big, faster change

        action = ActionChains(self.driver)
        action.click_and_hold(decrement).perform()
        while "disabled" not in decrement.get_attribute("class") and value < int(current_box.text):
            pass       
        action.release(decrement).perform()
        
        current = int(current_box.text)
        if current == value:
            return current
        
        action = ActionChains(self.driver)
        action.click_and_hold(increment).perform()
        while "disabled" not in increment.get_attribute("class") and value > int(current_box.text):
            pass
        action.release(increment).perform()
        
        current = int(current_box.text)
        if current == value:
            return current
        
        
        # make more precise and slower changes    
        # if clickable and still needs reducing, reduce value
        while "disabled" not in decrement.get_attribute("class") and value < int(current_box.text):
            click(decrement)
            
        current = int(current_box.text)
        if current == value:
            return current
            
        # if clickable and still needs reducing, reduce value
        while "disabled" not in increment.get_attribute("class") and value > int(current_box.text):
            click(increment)
            
        current = int(current_box.text)
        return current
