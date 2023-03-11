import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        s = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=s)

    def test_logout(self):
        # Init
        driver = self.browser
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()

        # Wait for initialize, in seconds
        wait = WebDriverWait(driver, 10)
        try:
            element = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        except ValueError:
            driver.quit()

        # Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(1)

        # Logout
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        driver.find_element(By.ID, "logout_sidebar_link").click()
        time.sleep(1)

        # Verification
        login_url = "https://www.saucedemo.com/inventory.html"
        response_data = driver.current_url
        self.assertIn(login_url, response_data)
        response_data = driver.find_element(By.CLASS_NAME, "title").text
        self.assertIn('Products', response_data)
        login_url = "https://www.saucedemo.com/"
        response_data = driver.current_url
        self.assertIn(login_url, response_data)

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
