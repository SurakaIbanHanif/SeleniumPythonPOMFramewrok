from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import pytest


@pytest.mark.usefixtures("setup_and_teardown")
class TestOne:
    def test_ninja_search_for_a_valid_product(self):
        self.driver.find_element(By.NAME, "search").send_keys("Hp")
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-lg']").click()
        assert self.driver.find_element(By.LINK_TEXT, "HP LP3065").is_displayed()



    def test_ninja_search_for_an_invalid_product(self):
        self.driver.find_element(By.NAME, "search").send_keys("MotorByke")
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-lg']").click()
        expected_text= "There is no product that matches the search criteria."
        assert self.driver.find_element(By.XPATH, "//p[contains(text(),'There is no product that matches the search criter')]").text.__eq__(expected_text)



    def test_ninja_search_without_providing_any_product(self):
        self.driver.find_element(By.NAME, "search").send_keys(" ")
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-lg']").click()
        expected_text01 = "Products meeting the search criteria"
        assert self.driver.find_element(By.XPATH,"//h2[normalize-space()='Products meeting the search criteria']").text.__eq__(expected_text01)

