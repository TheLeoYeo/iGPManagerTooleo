from enum import Enum
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.util.exceptions import NoSuchPilotError
from igp.util.tools import output


class Suspension(Enum):
    SOFT = 0
    NEUTRAL = 1
    FIRM = 2


class SetupCommands(BaseIGPaccount):
    strategy_page = "httpshttps://igpmanager.com/app/p=race&tab=strategy"
    setup_page = "https://igpmanager.com/app/p=race&tab=setup"


    def setup_drivers(self, suspension:Suspension=Suspension.SOFT, rheight:int=20, wlevel:int=20):
        if not self.logged_in():
                output("log in first")
                return

        if self.driver.current_url != self.setup_page:
            self.driver.get(self.setup_page)

        self.setup_driver(1, suspension, rheight, wlevel)


    def setup_driver(self, driver:int=1, suspension:Suspension=Suspension.SOFT, rheight:int=20, wlevel:int=20):
        """Set setup for a driver
            1 for driver 1 and 2 for driver 2
        """
        
        if not self.logged_in():
                output("log in first")
                return

        if self.driver.current_url != self.setup_page:
            self.driver.get(self.setup_page)

        if driver > 2:
            raise NoSuchPilotError()

        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, f"driver{driver}")))

        form = self.driver.find_element(By.ID, f"d{driver}setup")
        table = form.find_element(By.CLASS_NAME, "linkFill")
        rows = table.find_elements(By.TAG_NAME, "tr")

        self.set_suspension(rows[0], suspension)
        self.set_ride_height(rows[1], rheight)
        self.set_wing_level(rows[2], wlevel)


    def set_suspension(row, suspension:Suspension):
        button = row.find_element(By.CLASS_NAME, "rotateThis")
        while button.text.upper() != suspension.name:
            button.click()
        
              
    def train_by_threshold(self, threshold):
        '''
            Train until driver reaches a certain minimal health value
        '''
        if threshold < 0:
            threshold = 0
            
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "trainTable")))
        table = self.driver.find_element(By.ID, "trainTable")

        driver_rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        self.dt_clear_selections()

        for row in driver_rows:
            if threshold < self.driver_health_given_row(row):
                self.dt_select_row(row)

        train_button = self.driver.find_element(By.ID, "trainTrain")
        train_button.click()


    def driver_health(self, driver_num):
        table = self.driver.find_element(By.ID, "trainTable")
        driver_row = table.find_elements(By.CLASS_NAME, "tr")[driver_num]
        return self.driver_health_given_row(driver_row)


    def driver_health_given_row(self, row):
        return int(row.find_element(By.CLASS_NAME, "tHealth").text)


    def dt_clear_selections(self):
        check_input = self.driver.find_element(By.ID, "checkAll")
        check_container = check_input.find_element(By.XPATH, "./..")
        check = check_container.find_element(By.TAG_NAME, "label")

        try:
            check.click()
        except:
            time.sleep(1)
            check.click()
        # double click may be needed

        train_button = self.driver.find_element(By.ID, "trainTrain")
        if "disabled" not in train_button.get_attribute("class"):
            check.click()


    def dt_select_row(self, row):
        try:
            row.find_element(By.TAG_NAME, "label").click()
        except:
            time.sleep(1)
            row.find_element(By.TAG_NAME, "label").click()
        

    def train_row(self, row, threshold):
        if threshold >= self.driver_health_given_row(row):
            return
        
        self.dt_select_row(row)
        train_button = self.driver.find_element(By.ID, "trainTrain")
        train_button.click()
        self.dt_select_row(row)
