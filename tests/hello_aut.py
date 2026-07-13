import unittest, sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By

class AutTest(unittest.TestCase):

    def setUp(self):
        # Mengambil jenis browser dari Environment Variable (default: firefox)
        browser_type = os.getenv('BROWSER_TYPE', 'firefox').lower()

        # Pemilihan Options secara dinamis
        if browser_type == 'chrome':
            options = webdriver.ChromeOptions()
        elif browser_type == 'edge':
            options = webdriver.EdgeOptions()
        else:
            options = webdriver.FirefoxOptions()

        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        server = 'http://localhost:4444'

        self.browser = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser.quit)

    def test_homepage(self):
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "http://localhost"

        self.browser.get(url)
        
        # Penamaan screenshot dinamis agar mudah dibedakan
        browser_type = os.getenv('BROWSER_TYPE', 'firefox')
        self.browser.save_screenshot(f'screenshot_{browser_type}.png')

        expected_result = "Welcome back, Guest!"
        actual_result = self.browser.find_element(By.TAG_NAME, 'p')

        self.assertIn(expected_result, actual_result.text)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')