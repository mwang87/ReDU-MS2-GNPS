import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait


from selenium.webdriver.common.keys import Keys
import unittest, time, re
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import chromedriver_binary
SERVER_URL = os.environ.get("SERVER_URL", "https://redu.ucsd.edu")

class TestInterfaceready(unittest.TestCase):
  
    def setUp(self):    
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless') 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)

        
    def tearDown(self):
        self.driver.quit()

    def test_compound_enrichment(self):
        #going to the page
        url = "{}/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE".format(SERVER_URL)

        
        self.driver.get(url)
        time.sleep(1)
        wait = WebDriverWait(self.driver, 180) 
        #aiting for the modal to go away
        wait.until(EC.invisibility_of_element_located((By.ID, 'loadMe'))) #works when we say "visibility" locally
        wait.until(EC.visibility_of_element_located((By.ID,'querycompound')))
        #clicking the button
        python_button = self.driver.find_element_by_id('querycompound')

        python_button.click()

        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert present, error")
            return 1
        except Exception:
            print("no alert, passing")

if __name__ == "__main__":
    unittest.main()
