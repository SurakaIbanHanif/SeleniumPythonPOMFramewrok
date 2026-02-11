import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup_and_teardown")
class TestLogin:
    def test_open_login_page(self):
        wait = WebDriverWait(self.driver, 20)

        wait.until(EC.element_to_be_clickable((
            By.XPATH, "//a[contains(@href,'login') and (contains(.,'Hello') or contains(.,'Sign'))]"
        ))).click()

        wait.until(EC.url_contains("/login"))
        assert "/login" in self.driver.current_url

    def test_google_login_button_visible(self):
        wait = WebDriverWait(self.driver, 20)

        # Open login page
        wait.until(EC.element_to_be_clickable((
            By.XPATH, "//a[contains(@href,'login')]"
        ))).click()

        google_btn = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//*[self::a or self::button][contains(.,'Google')]"
        )))

        assert google_btn.is_displayed()

    def test_login_with_google_using_saved_profile(self):
        wait = WebDriverWait(self.driver, 30)

        # 1️Click "Hello, Sign in"
        wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@href,'login') and (contains(.,'Hello') or contains(.,'Sign'))]"
        ))).click()

        # 2️ Click Google button
        google_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//*[self::a or self::button][contains(.,'Google')]"
        )))

        main_window = self.driver.current_window_handle
        before_handles = set(self.driver.window_handles)
        google_btn.click()

        # 3️ Switch to Google window (if new tab opens)
        wait.until(lambda d: len(d.window_handles) >= len(before_handles))
        after_handles = set(self.driver.window_handles)
        new_window = list(after_handles - before_handles)

        if new_window:
            self.driver.switch_to.window(new_window[0])

        # 4️ Select saved Google account (if chooser appears)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Choose an account')]"))
            )

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((
                By.XPATH,
                "//*[contains(text(),'suraka.hanif@enosisbd.com')]/ancestor::*[self::div or self::li][1]"
            ))).click()
        except:
            # Already logged in / chooser skipped
            pass

        # 5️ Switch back to rokomari window
        WebDriverWait(self.driver, 30).until(lambda d: len(d.window_handles) >= 1)

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if "rokomari.com" in self.driver.current_url:
                break

        # 6️ Assert login success (profile name visible)
        wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(.,'Hello') and (contains(.,'Suraka') or contains(.,'সুরাকা'))]"
        )))

        assert True

    def test_logged_in_user_profile_visible(self):
        wait = WebDriverWait(self.driver, 20)

        profile = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(.,'Hello') and contains(.,'Suraka')]"
        )))

        assert profile.is_displayed()
