import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.util.decorators import igpcommand
from igp.util.tools import output


class DriverTrainCommands(BaseIGPaccount):
    training_page = "https://igpmanager.com/app/p=training"

            
    @igpcommand(alias="train if above 50%", page=training_page)
    def train_above_threshold(self, threshold:int=50):
        '''Train if driver is above a certain minimal health value
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


    @igpcommand(alias="train until 0%", page=training_page)
    def train_until_threshold(self, threshold:int=0):
        '''Train while driver is above a certain minimal health value
        '''       
        if threshold < 0:
            threshold = 0
            
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "trainTable")))
        table = self.driver.find_element(By.ID, "trainTable")

        driver_rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        more_training = True
        count = 0
        while more_training and count <= 12:
            more_training = False
            self.dt_clear_selections()
            for row in driver_rows:
                if threshold < self.driver_health_given_row(row):
                    self.dt_select_row(row)
                    more_training = True

            train_button = self.driver.find_element(By.ID, "trainTrain")
            train_button.click()
            count = count + 1


    @igpcommand(alias="driver health", page=training_page)
    def driver_health(self, driver_num:int=1):
        if driver_num < 1:
            driver_num = 1
            
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "trainTable")))
        table = self.driver.find_element(By.ID, "trainTable")
        driver_row = table.find_elements(By.TAG_NAME, "tr")[driver_num]
        health = self.driver_health_given_row(driver_row)
        output(health)

 
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
