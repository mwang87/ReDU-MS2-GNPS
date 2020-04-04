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

from selenium.common.exceptions import TimeoutException

SERVER_URL = os.environ.get("SERVER_URL", "https://redu.ucsd.edu")

class TestInterfaceready(unittest.TestCase):
    def setUp(self):
        try:
            import chromedriver_binary
        except:
            os.system('pip install chromedriver-binary')            
            import chromedriver_binary

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)
        #self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        #self.vars = {}
        
    def tearDown(self):
        self.driver.quit()

    def test_compound_enrichment(self):
        #going to the page
        #url = "https://redu.ucsd.edu/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE"
        url = "{}/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE".format(SERVER_URL)
        #url = "http://localhost:5006/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE"  
        print(url)
        self.driver.get(url)
        time.sleep(1)
 
        wait = WebDriverWait(self.driver, 180)
        print("begin")
            
        #waiting for the modal to go away
        wait.until(EC.invisibility_of_element_located((By.ID, 'loadMe'))) #works when we say "visibility" locally
        print("past check one")

        #waiting for the button to be clickable
        wait.until(EC.visibility_of_element_located((By.ID,'querycompound')))

        print("past check two")
        #clicking the button
        python_button = self.driver.find_element_by_id('querycompound')
        print("past check three")
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
