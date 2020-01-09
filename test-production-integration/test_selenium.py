import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import os

SERVER_URL = os.environ.get("SERVER_URL", "https://redu.ucsd.edu")

class TestInterfaceready(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        self.vars = {}

    def tearDown(self):
        self.driver.quit()

    def test_compound_enrichment(self):
        #self.driver.get("{}/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE".format(SERVER_URL))
        self.driver.get("http://localhost:5005/compoundenrichmentdashboard?compound=ESCITALOPRAM%20OXALATE")
        time.sleep(1)
        WebDriverWait(self.driver, 180).until(expected_conditions.element_to_be_clickable((By.ID, "queryresultsbutton")))
        python_button = self.driver.find_element_by_id("queryresultsbutton")
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