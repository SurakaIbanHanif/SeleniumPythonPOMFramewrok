import logging
import pytest
import time
import os
from selenium.webdriver.common.by import By
from TEST.Utilities.ExcelUtils import get_data_from_excel
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# ==========================
# Logging Configuration
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("setup_and_teardown")
class TestRegister:

    def open_register_page(self):
        wait = WebDriverWait(self.driver, 15)

        logger.info("Clicking 'My Account'")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='My Account']")
        )).click()
        logger.info("Clicking 'Register'")

        wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Register")
        )).click()
        logger.info("Register page opened")


    @pytest.mark.parametrize(
        "firstname, lastname, email, telephone, password, password_confirmed",
        get_data_from_excel("TEST/ExcelFile/User_email_pass.xlsx", "RegisterTest")
    )
    def test_register_with_excel_data(
        self, firstname, lastname, email, telephone, password, password_confirmed
    ):
        wait = WebDriverWait(self.driver, 15)

        logger.info(f"Starting registration for email: {email}")

        self.open_register_page()

        try:
            # ---- Fill form ----
            logger.info("Filling registration form")

            wait.until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys(firstname)
            wait.until(EC.visibility_of_element_located((By.ID, "input-lastname"))).send_keys(lastname)
            wait.until(EC.visibility_of_element_located((By.ID, "input-email"))).send_keys(email)
            wait.until(EC.visibility_of_element_located((By.ID, "input-telephone"))).send_keys(str(telephone))
            wait.until(EC.visibility_of_element_located((By.ID, "input-password"))).send_keys(password)
            wait.until(EC.visibility_of_element_located((By.ID, "input-confirm"))).send_keys(password_confirmed)

            logger.info("Ticking privacy policy checkbox")
            wait.until(EC.element_to_be_clickable((By.NAME, "agree"))).click()

            logger.info("Submitting registration form")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@value='Continue']")
            )).click()

            # Wait for either success or error
            wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, "#content h1") or
                                d.find_elements(By.CSS_SELECTOR, ".alert.alert-danger"))

            page_h1 = self.driver.find_element(By.CSS_SELECTOR, "#content h1").text.strip()

            if page_h1 == "Your Account Has Been Created!":
                logger.info("Registration successful")
                assert True
            else:
                alerts = self.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
                error_text = " | ".join(a.text.strip() for a in alerts if a.text.strip())

                #feilure evidence
                logger.error("Registration failed")
                logger.error(f"Current URL: {self.driver.current_url}")
                logger.error(f"H1 text: {page_h1}")
                logger.error(f"Alerts: {error_text}")

                self._capture_screenshot()

                assert False, f"Register failed. URL='{self.driver.current_url}', Alerts='{error_text}'"

        except Exception as e:
            logger.exception("Unexpected exception occurred during registration")
            self._capture_screenshot()
            raise

    def test_register_without_mandatory_fields(self):
        wait = WebDriverWait(self.driver, 15)

        logger.info("Testing registration without mandatory fields")

        self.open_register_page()

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@value='Continue']")
        )).click()

        warning = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
        ).text

        logger.info(f"Warning displayed: {warning}")

        assert "Warning:" in warning

    # ==========================
    # Screenshot Helper
    # ==========================
    def _capture_screenshot(self):
        os.makedirs("artifacts", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = f"artifacts/failure_{timestamp}.png"
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved at: {path}")
