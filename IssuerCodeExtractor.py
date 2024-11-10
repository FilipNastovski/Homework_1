from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from typing import List

class IssuerCodeExtractor:
    """First pipe: Extract and filter issuer codes from MSE website."""

    def __init__(self):
        self.url = "https://www.mse.mk/en/stats/symbolhistory/ADIN"
        self.driver = None

    def setup_driver(self):
        """Initialize Chrome WebDriver with headless mode."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def get_issuer_codes(self) -> List[str]:
        """Extract all issuer codes from the dropdown."""
        try:
            self.setup_driver()
            self.driver.get(self.url)

            # Wait for dropdown to be present
            dropdown = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.ID, "Code"))
            )

            # Extract all options
            options = dropdown.find_elements(By.TAG_NAME, "option")
            codes = [option.get_attribute('value') for option in options if option.get_attribute('value')]

            return codes

        finally:
            if self.driver:
                self.driver.quit()

    def filter_codes(self, codes: List[str]) -> List[str]:
        """Filter out codes containing numbers or starting with E, M, or S."""
        filtered_codes = []
        for code in codes:
            if (not any(char.isdigit() for char in code) and
                    not code.startswith(('E', 'M', 'S'))):
                filtered_codes.append(code)
        return filtered_codes

    def get_data(self) -> List[str]:
        """Main method to get and filter issuer codes."""
        codes = self.get_issuer_codes()
        return self.filter_codes(codes)
