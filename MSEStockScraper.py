import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import warnings

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
        self.columns_to_keep = [
            "Date",
            "Last Trade Price",
            "Max",
            "Min",
            "Volume",
            "Turnover in BEST (denars)"
        ]

    def scrape_table(self, start_date, end_date):
        """Scrape the data table and return as a DataFrame"""
        try:
            params = {
                "FromDate": start_date,
                "ToDate": end_date
            }
            response = requests.get(self.url, params=params)
            soup = BeautifulSoup(response.content, "html.parser")

            table = soup.find("table", id="resultsTable")
            if table:
                # Read table without headers
                df = pd.read_html(str(table), header=None)[0]
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
            else:
                return None

        except Exception as e:
            print(f"Error scraping table: {self.symbol}")
            return None

    def scrape_historical_data(self, years=10):
        """Scrape data for the specified number of years"""
        try:
            current_year = datetime.now().year
            start_year = current_year - years + 1

            all_data = []

            for year in range(start_year, current_year + 1):
                start_date = f"01/01/{year}"
                end_date = f"12/31/{year}"
                print(f"Scraping data for year {year} code: {self.symbol}")
                year_data = self.scrape_table(start_date, end_date)
                if year_data is not None and not year_data.empty:
                    print(f"Successfully scraped {len(year_data)} rows for year {year} Code: {self.symbol}")
                    all_data.append(year_data)
                else:
                    print(f"Scraping data for year {year} code: {self.symbol} error: NO DATA")

            if all_data:
                final_data = pd.concat(all_data, ignore_index=True)
                final_data = final_data.drop_duplicates()
                final_data.sort_values('Date', ascending=False, inplace=True)
                return final_data
            else:
                raise Exception("No data was successfully scraped")

        except Exception as e:
            print(f"Error scraping historical data: {self.symbol}")
            return None
