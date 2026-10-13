
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://localhost:8000/login.html"


class LoginTests:

    def setUp(self):
        if self.browser == "Chrome":
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()

        self.driver.get(URL)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        if hasattr(self, "driver"):
            self.driver.quit()

    def test_valid_login(self):
        self.driver.find_element(
            By.ID, "username"
        ).send_keys("admin")

        self.driver.find_element(
            By.ID, "password"
        ).send_keys("admin123")

        self.driver.find_element(
            By.ID, "loginButton"
        ).click()

        message = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "message")
            )
        )

        self.assertEqual(
            message.text, "Login successful!"
        )

    def test_invalid_login(self):
        self.driver.find_element(
            By.ID, "username"
        ).send_keys("wronguser")

        self.driver.find_element(
            By.ID, "password"
        ).send_keys("wrongpass")

        self.driver.find_element(
            By.ID, "loginButton"
        ).click()

        message = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "message")
            )
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
