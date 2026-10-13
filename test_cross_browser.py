
import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://127.0.0.1:8000/login.html"
CI = os.getenv("GITHUB_ACTIONS") == "true"


class LoginTests:
    def setUp(self):
        if self.browser == "Chrome":
            options = webdriver.ChromeOptions()

            if CI:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=options)

        elif self.browser == "Firefox":
            options = webdriver.FirefoxOptions()

            if CI:
                options.add_argument("-headless")

            self.driver = webdriver.Firefox(options=options)

        self.driver.get(URL)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        if hasattr(self, "driver"):
            self.driver.quit()

    def test_valid_login(self):
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin123")
        self.driver.find_element(By.ID, "loginButton").click()

        message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "message"))
        )
        self.assertEqual(message.text, "Login successful!")

    def test_invalid_login(self):
        self.driver.find_element(By.ID, "username").send_keys("wronguser")
        self.driver.find_element(By.ID, "password").send_keys("wrongpass")
        self.driver.find_element(By.ID, "loginButton").click()

        message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "message"))
        )
        self.assertEqual(
            message.text,
            "Invalid username or password"
        )


class ChromeTests(LoginTests, unittest.TestCase):
    browser = "Chrome"


class FirefoxTests(LoginTests, unittest.TestCase):
    browser = "Firefox"


if __name__ == "__main__":
    unittest.main(verbosity=2)
