from selenium.webdriver.common.by import By
from db_operations import get_new_users, update_status

def test_register_users_from_db(driver):

    users = get_new_users()

    for user in users:

        driver.get("https://parabank.parasoft.com/parabank/register.htm")

        driver.find_element(By.ID, "customer.firstName").send_keys(user["first_name"])
        driver.find_element(By.ID, "customer.lastName").send_keys(user["last_name"])
        driver.find_element(By.ID, "customer.address.street").send_keys(user["address"])
        driver.find_element(By.ID, "customer.address.city").send_keys(user["city"])
        driver.find_element(By.ID, "customer.address.state").send_keys(user["state"])
        driver.find_element(By.ID, "customer.address.zipCode").send_keys(user["zip_code"])
        driver.find_element(By.ID, "customer.phoneNumber").send_keys(user["phone"])
        driver.find_element(By.ID, "customer.ssn").send_keys(user["ssn"])
        driver.find_element(By.ID, "customer.username").send_keys(user["username"])
        driver.find_element(By.ID, "customer.password").send_keys(user["password"])
        driver.find_element(By.ID, "repeatedPassword").send_keys(user["password"])

        driver.find_element(By.CSS_SELECTOR, "input[value='Register']").click()

        # Success check
        if "successfully" in driver.page_source:
            update_status(user["id"], "REGISTERED")
        else:
            update_status(user["id"], "FAILED")
