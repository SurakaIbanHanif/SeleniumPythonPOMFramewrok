from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class HomePage:
    SEARCH_BOX = (By.ID, "js--search")
    RESULT_TITLES = (By.XPATH, "//h4")
    NO_RESULT_MESSAGE = (By.XPATH, "//*[contains(.,'No Result Found')]")

    def __init__(self, driver):
        self.driver = driver

    def search(self, keyword):
        search_box = self.driver.find_element(*self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

    def empty_search(self):
        search_box = self.driver.find_element(*self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(Keys.ENTER)
        return search_box

    def get_result_titles(self):
        elements = self.driver.find_elements(*self.RESULT_TITLES)
        return [e.text for e in elements if e.text.strip()]

    def is_title_present(self, expected_text):
        titles = self.get_result_titles()
        return any(expected_text in t for t in titles)

    def get_no_result_text(self):
        elements = self.driver.find_elements(*self.NO_RESULT_MESSAGE)
        if elements:
            return elements[0].text
        return ""

    def get_validation_message(self):
        search_box = self.driver.find_element(*self.SEARCH_BOX)
        return search_box.get_attribute("validationMessage")
