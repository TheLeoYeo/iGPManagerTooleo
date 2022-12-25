from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from igp.service.base_igp_account import BaseIGPaccount
from igp.service.commands.tasks import Categories
from igp.service.modifier.modifier import BaseModifier, IntegerField
from igp.util.decorators import igpcommand
from igp.util.tools import click, output
from igp.util.turbomode import turbo_wait


class DriverTrainCommands(BaseIGPaccount):
    training_page = "https://igpmanager.com/app/p=training"
     
    @igpcommand(alias="train if above X%", page=training_page, category=Categories.TRAINING, 
                modifier=BaseModifier(IntegerField("threshold", 0, 100, 50)))
    def train_above_threshold(self, threshold:int=50):
        '''Train if driver is above a certain minimal health value.
        Default is 50%''' 
        
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
        click(train_button)
        turbo_wait()


    @igpcommand(alias="train until X%", page=training_page, category=Categories.TRAINING,
                modifier=BaseModifier(IntegerField("threshold", 0, 100)))
    def train_until_threshold(self, threshold:int=0):
        '''Train while driver is above a certain minimal health value
        Default is 0%
        Stops once we hit specified percentage or we have trained
        more than 12 times'''
        
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
            click(train_button)
            count = count + 1


    @igpcommand(alias="specific driver health", page=training_page, category=Categories.TRAINING,
                modifier=BaseModifier(IntegerField("driver_num", 1, 10, 1)))
    def driver_health(self, driver_num:int=1):
        """Displays the health of a specified driver
        Specify driver by number, first driver = 1, nth driver = n"""
            
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "trainTable")))
        table = self.driver.find_element(By.ID, "trainTable")
        try:
            driver_row = table.find_elements(By.TAG_NAME, "tr")[driver_num]
            health = self.driver_health_given_row(driver_row)
            message = f"Driver {driver_num}: {health}%"
            output(message)
        except:
            output("Error: no such driver")
            
        
    @igpcommand(alias="all driver health", page=training_page, category=Categories.TRAINING)
    def all_driver_healths(self):
        """Displays the health of all drivers"""
        
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "trainTable")))
        table = self.driver.find_element(By.ID, "trainTable")
        message = ""
        try:
            for i in range(5):
                driver_row = table.find_elements(By.TAG_NAME, "tr")[1 + i]
                health = self.driver_health_given_row(driver_row)
                message += f"Driver {1 + i}: {health}%, "
        except:
            pass
        
        output(message[:-2])

 
    def driver_health_given_row(self, row):
        return int(row.find_element(By.CLASS_NAME, "tHealth").text)


    def dt_clear_selections(self):
        check_input = self.driver.find_element(By.ID, "checkAll")
        check_container = check_input.find_element(By.XPATH, "./..")
        check = check_container.find_element(By.TAG_NAME, "label")

        click(check)

        # double click may be needed
        train_button = self.driver.find_element(By.ID, "trainTrain")
        if "disabled" not in train_button.get_attribute("class"):
            click(check)


    def dt_select_row(self, row):
        click(row.find_element(By.TAG_NAME, "label"))
        

    def train_row(self, row, threshold):
        if threshold >= self.driver_health_given_row(row):
            return
        
        self.dt_select_row(row)
        train_button = self.driver.find_element(By.ID, "trainTrain")
        click(train_button)
        self.dt_select_row(row)
