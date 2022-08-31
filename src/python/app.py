from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def output_with_message(message: str):
    print("***********************************************************************************************************************")
    print(message)
    print("***********************************************************************************************************************")



# The next part cycles through FZ Cars 19 through to 45 logging in one after the other
for x in range(19,45):

    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_argument('log-level=3')

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })

    driver = webdriver.Chrome(chrome_options=option)
    driver.get("https://igpmanager.com/app/p=login")

    user = "FZ"+str(x)+"@FZ.com"
    # user = "FZ21@FZ.com"

    time.sleep(1)
    assert "iGP Manager" in driver.title
    elemUser = driver.find_element_by_id("loginUsername")
    elemPW = driver.find_element_by_id("loginPassword")
    elemUser.clear()
    elemPW.clear()
    elemUser.send_keys(user)
    elemPW.send_keys("inter")
    elemPW.send_keys(Keys.RETURN)
    time.sleep(1)
    driver.get("https://igpmanager.com/app/p=cars&tab=repair")
    time.sleep(1)
    # driver.find_element_by_id("c1PartSwap").click
    # print("***********************************************************************************************************************")
    # print(user + " Car Repaired")
    # print("***********************************************************************************************************************")
    time.sleep(1)
    REPAIRTEST = driver.find_element_by_id("c1EngSwap").get_attribute('data-tip')
    # driver.find_element_by_id("c1EngSwap").click
    # This is where I got stuck on replacing engines

    output_with_message(user + " " + REPAIRTEST + " Engine Repaired")

    # Driver Training Element Below
    time.sleep(1)
    driver.get("https://igpmanager.com/app/p=training")
    time.sleep(1)
    
    # finds the health bar on the screen and checks if it is 100 
    elemHealth = driver.find_element_by_class_name("tHealth").text
    if elemHealth == "100":
        elemTrain = driver.find_element_by_id("trainTrain").click()
        output_with_message("Driver " + user + " trained")
        time.sleep(1)
        driver.close()
    
    else:
        output_with_message("Driver " + user + " NOT trained due to health being " + elemHealth)
        time.sleep(1)
        driver.close()
        