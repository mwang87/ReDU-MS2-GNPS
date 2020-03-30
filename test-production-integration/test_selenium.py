import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import os

SERVER_URL = os.environ.get("SERVER_URL", "https://redu.ucsd.edu")

class TestInterfaceready(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)
        #self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        self.vars = {}
        
    def tearDown(self):
        self.driver.quit()

    def test_compound_enrichment(self):
        #going to the page
        self.driver.get("{}/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE".format(SERVER_URL))
        #self.driver.get("http://localhost:5006/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE")
        time.sleep(1) 
        
        wait = WebDriverWait(self.driver, 180)
        
        #waiting for the modal to go aay
        wait.until(EC.invisibility_of_element_located((By.ID, 'loadMe')))

        #waiting for the button to be clickable
        wait.until(EC.element_to_be_clickable((By.ID,'querycompound')))
        
        #clicking the button
        python_button = self.driver.find_element(By.ID, 'querycompound')
        python_button.click()
        #time.sleep(60)

        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert present, error")
            return 1
        except Exception:
            print("no alert, passing")

if __name__ == "__main__":
    unittest.main()
