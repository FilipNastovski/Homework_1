from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import pandas as pd
import warnings
import time

warnings.filterwarnings("ignore", category=FutureWarning, message="Passing literal html to 'read_html' is deprecated")


def clean_numeric(value):
    """Clean numeric values, handling both string and numeric inputs"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.replace(',', '').replace(' ', ''))
    return None


class MSEStockScraper:
    def __init__(self, issuer_code):
        self.url = f"https://www.mse.mk/en/stats/symbolhistory/{issuer_code}"
        self.symbol = issuer_code
        self.driver = None
        self.data = []
        # Column names in order as they appear
        self.column_names = [
            "Date",
            "Last Trade Price",
            "Max",
            "Min",
            "Avg. Price",
            "%chg.",
            "Volume",
            "Turnover in BEST (denars)",
            "Total turnover (denars)"
        ]
        # Columns to keep
        self.columns_to_keep = [
            "Date",
            "Last Trade Price",
            "Max",
            "Min",
            "Volume",
            "Turnover in BEST (denars)"
        ]
        self.setup_driver()

    def setup_driver(self):
        """Initialize the Chrome WebDriver with necessary options"""
        options = webdriver.ChromeOptions()
        # Comment argument --headless to see the Chrome tab open and do the scraping
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.driver = webdriver.Chrome(options=options)

    def wait_for_element(self, by, value, timeout=20):
        """Wait for an element to be present and return it"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def set_date(self, date_picker_id, date_str):
        """Set date in a date picker"""
        try:
            date_picker = self.wait_for_element(By.ID, date_picker_id)
            self.driver.execute_script(f"document.getElementById('{date_picker_id}').value = '{date_str}'")
            # time.sleep(0.5)
        except Exception as e:
            print(f"Error setting date for {date_picker_id}: {str(e)}")
            raise

    def click_search(self):
        """Click the search button"""
        try:
            search_button = self.wait_for_element(
                By.CSS_SELECTOR,
                "input.btn.btn-primary-sm[value='Find']"
            )
            search_button.click()
            # time.sleep(2)
        except Exception as e:
            print(f"Error clicking search button: {str(e)}")
            raise

    def scrape_table(self):
        """Scrape the data table and return as a DataFrame"""
        try:
            table = self.wait_for_element(By.ID, "resultsTable", 20)
            # Read table without headers
            df = pd.read_html(table.get_attribute('outerHTML'), header=None)[0]

            df.columns = self.column_names

            # Keep only the desired columns
            df = df[self.columns_to_keep]

            # Convert numeric columns
            numeric_columns = ['Last Trade Price', 'Max', 'Min', 'Volume', 'Turnover in BEST (denars)']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].apply(clean_numeric)

            # Convert date column to datetime
            df['Date'] = pd.to_datetime(df['Date']).dt.date

            return df

        except Exception as e:
            print(f"Error scraping table: {self.symbol}")

            print("Table HTML:", table.get_attribute('outerHTML') if 'table' in locals() else "Table not found")
            raise

    def scrape_year_data(self, year):
        """Scrape data for a specific year"""
        try:
            start_date = f"01/01/{year}"
            end_date = f"12/31/{year}"

            print(f"Scraping data for year {year} code: {self.symbol}")

            self.set_date("FromDate", start_date)
            self.set_date("ToDate", end_date)
            self.click_search()

            year_data = self.scrape_table()

            if year_data is None or len(year_data) == 0:
                print(f"No data found for year {year}")
            else:
                print(f"Successfully scraped {len(year_data)} rows for year {year} Code: {self.symbol}")

            return year_data

        except Exception as e:
            print(f"Error scraping data for {self.symbol} for year: {year}")
            return None

    def scrape_historical_data(self, years=10):
        """Scrape data for the specified number of years"""
        try:
            self.driver.get(self.url)

            current_year = datetime.now().year
            start_year = current_year - years + 1

            all_data = []

            time.sleep(3)  # Wait for initial page load

            for year in range(start_year, current_year + 1):
                year_data = self.scrape_year_data(year)
                if year_data is not None and not year_data.empty:
                    all_data.append(year_data)
                time.sleep(2)

            if all_data:
                final_data = pd.concat(all_data, ignore_index=True)
                final_data = final_data.drop_duplicates()
                final_data.sort_values('Date', ascending=False, inplace=True)

                # Uncomment to save the data for each code into separate scv files
                # self.save_to_csv(final_data)
                return final_data
            else:
                raise Exception("No data was successfully scraped")

        finally:

            if self.driver:
                self.driver.quit()