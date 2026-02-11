from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from TEST.Utilities.ExcelUtils import get_data_from_excel
import time
import pytest


@pytest.mark.usefixtures("setup_and_teardown")
class TestLogin:
    @pytest.mark.parametrize("email_address, password", get_data_from_excel("TEST/ExcelFile/User_email_pass.xlsx", "LoginTest"))
    def test_login_with_valid_credentials(self, email_address,password):
        self.driver.find_element(By.XPATH, "//span[text()='My Account']").click()
        self.driver.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        self.driver.find_element(By.ID, "input-email").send_keys(email_address)
        self.driver.find_element(By.ID, "input-password").send_keys(password)
        self.driver.find_element(By.XPATH, "//input[@value='Login']").click()
        assert self.driver.find_element(By.XPATH, "//a[normalize-space()='Edit your account information']").is_displayed()


    def test_login_without_fillingout_credentials(self):
        self.driver.find_element(By.XPATH, "//span[text()='My Account']").click()
        self.driver.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        self.driver.find_element(By.ID, "input-email").send_keys(" ")
        self.driver.find_element(By.ID, "input-password").send_keys(" ")
        self.driver.find_element(By.XPATH, "//input[@value='Login']").click()
        expected_warning_message= "Warning: No match for E-Mail Address and/or Password."
        assert self.driver.find_element(By.XPATH, "//div[contains(text(),'No match for E-Mail Address')]").text.__contains__(expected_warning_message)


