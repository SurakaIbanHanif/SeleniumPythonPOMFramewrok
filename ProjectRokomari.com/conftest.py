from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pytest


@pytest.fixture()
def setup_and_teardown(request):
    global driver
    char_options = Options()
    char_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=char_options)
    driver.maximize_window()
    driver.get("https://www.rokomari.com/")
    request.cls.driver=driver
    yield
    driver.quit()

