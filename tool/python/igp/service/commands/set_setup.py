from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.service.modifier.modifier import BaseModifier, IntegerField, OptionField
from igp.util.exceptions import NoSuchPilotError
from igp.util.tools import click, output
from igp.util.decorators import igpcommand


class Suspension(Enum):
    SOFT = 0
    NEUTRAL = 1
    FIRM = 2
    
    
class DriverTab(Enum):
    DRIVER1 = 1
    DRIVER2 = 2


class SetupCommands(BaseIGPaccount):
    setup_page = "https://igpmanager.com/app/p=race&tab=setup"
    ALL_SUSP_TYPES = [Suspension.SOFT, Suspension.NEUTRAL, Suspension.FIRM]
    ALL_DRV_TYPES = [DriverTab.DRIVER1, DriverTab.DRIVER2]
    
    @igpcommand(alias="setup all drivers", page=setup_page, help="Sets the setup of all drivers in the account", 
                modifier=BaseModifier(OptionField("suspension", ALL_SUSP_TYPES, 0), IntegerField("rheight", 1, 50, 20), IntegerField("wlevel", 1, 50, 20)))
    def setup_drivers(self, suspension:Suspension=Suspension.SOFT, rheight:int=20, wlevel:int=20):
        for driver in self.ALL_DRV_TYPES:
            self.setup_driver(driver, suspension, rheight, wlevel)


    @igpcommand(alias="setup a driver", page=setup_page, 
                modifier=BaseModifier(OptionField("driver", ALL_DRV_TYPES), OptionField("suspension", ALL_SUSP_TYPES, 0), IntegerField("rheight", 1, 50, 20), IntegerField("wlevel", 1, 50, 20)))
    def setup_driver(self, driver:DriverTab=DriverTab.DRIVER1, suspension:Suspension=Suspension.SOFT, rheight:int=20, wlevel:int=20):
        """Set setup for a driver"""

        try:
            self.grab_tab(driver)
        except NoSuchPilotError:
            return
        
        form = self.driver.find_element(By.ID, f"d{driver.value}setup")
        table = form.find_element(By.CLASS_NAME, "linkFill")
        rows = table.find_elements(By.TAG_NAME, "tr")

        self.set_suspension(rows[0], suspension)
        output(f"suspension set to {suspension.name}", log_only=True)
        rh = self.set_row_value(rows[1], rheight)
        output(f"ride height set to {rh}", log_only=True)
        wl = self.set_row_value(rows[2], wlevel)
        output(f"wing level set to {wl}", log_only=True)
        self.hit_save()
        
        
    def grab_tab(self, tab:DriverTab):
        num = tab.value
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, f"driver{num}")))
        button = self.driver.find_element(By.ID, f"driver{num}")
        if "disabled" in button.get_attribute("class"):
            raise NoSuchPilotError()

        click(button)


    def set_suspension(self, row:WebElement, suspension:Suspension):
        button = row.find_element(By.CLASS_NAME, "rotateThis")
        click(button)
        while button.text.upper() != suspension.name:
            click(button)

  
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
