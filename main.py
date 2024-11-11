import asyncio
import IssuerCodeExtractor
import DatabaseManager
import DataScraper
import time
import sys
import importlib.util
import subprocess

import MSEStockScraper


def check_dependencies():
    """Check and install required dependencies"""

    # Check Python version
    if sys.version_info < (3, 12):
        print("Python 3.12 or higher is required.")
        sys.exit(1)
    else:
        print(f"Python {sys.version.split()[0]} detected. Proceeding with dependency check.\n")

    required_packages = {
        'aiohttp': 'aiohttp',
        'pandas': 'pandas',
        'beautifulsoup4': 'bs4',
        'sqlite3': 'sqlite3',
        'asyncio': 'asyncio',
        'queue': 'queue',
        'threading': 'threading',
        'time': 'time',
    }

    for package_name, module_name in required_packages.items():
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                print(f"Installing required package: {package_name}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            else:
                print(f"Found required package: {package_name}")
        except (ImportError, subprocess.CalledProcessError):
            print(f"Error installing required package: {package_name}")
            sys.exit(1)
    print("\n\n")

def run_query_mode():
    first_pipe = IssuerCodeExtractor.IssuerCodeExtractor()
    second_pipe = DatabaseManager.DatabaseManager()
    print("Getting issuer codes...")
    issuer_codes = first_pipe.get_issuer_codes()
    issuer_codes = first_pipe.filter_codes(issuer_codes)
    print(f"Found {len(issuer_codes)} valid issuer codes\n")
    print("Valid codes:")
    print(issuer_codes)
    while True:
        print("Enter issuer code you want the data for:")
        issuer_code_for_sample = input()
        if issuer_code_for_sample in issuer_codes:
            print("Enter how many rows to fetch:")
            num_rows = int(input())
            if 0 < num_rows <= 10000:
                print(second_pipe.fetch_sample_data(issuer_code=issuer_code_for_sample, limit=num_rows))
            else:
                print(second_pipe.fetch_sample_data(issuer_code=issuer_code_for_sample, limit=10000))
        else:
            print("The code you entered is not valid")

        print("Continue to query? ('n' for No, 'y' for Yes):")
        usr_in = input()
        if usr_in == 'y':
            pass
        else:
            exit(11)


async def main():
    try:

        first_pipe = IssuerCodeExtractor.IssuerCodeExtractor()
        second_pipe = DatabaseManager.DatabaseManager()
        third_pipe = DataScraper.DataScraper(second_pipe)

        print("Checking and installing required dependencies...")
        check_dependencies()

        print("Enter string \"query\" to run the program in query mode")
        #print("Enter string \"bench\" to run the program in benchmark mode or enter a number to exec normally")
        print("Enter string \"normal\" to run the program in normal (or leave blank to run the program in normal mode)")

        user_input = input()
        if user_input == "query":
            run_query_mode()

        print("Enter the number of threads to be used (leave empty for default = 200)")

        thread_number = input()
        if thread_number.isdigit() and 1 < int(thread_number) <= 200:
            thread_number = int(thread_number)
        else:
            thread_number = 200

        start_time = time.time()

        print("Getting issuer codes...")
        issuer_codes = first_pipe.get_issuer_codes()
        #issuer_codes = issuer_codes[:5]
        print(f"Found {len(issuer_codes)} valid issuer codes\n")

        print("Filtering issuer codes...")
        issuer_codes = first_pipe.filter_codes(issuer_codes)
        print(f"Remaining codes: {len(issuer_codes)}\n")

        print("Checking data currency...")
        update_info = second_pipe.check_data_currency(issuer_codes)
        print(f"{len(update_info)} issuers need updating\n")

        if update_info:
            print("Starting data update...\n")
            await third_pipe.update_data(update_info=update_info)
            print("\nData update completed\n")
        else:
            print("All data is up to date")

        execution_time = time.time() - start_time

        print(f"\nScraping completed successfully in {execution_time:.2f} seconds\n\n")

        print("Display a sample of the scraped data? ('n' for No, 'y' for Yes):")
        usr_in = input()
        if usr_in == 'y':
            print("Enter issuer code you want the data for:")
            issuer_code_for_sample = input()
            if issuer_code_for_sample in issuer_codes:
                print("Enter how many rows to fetch:")
                num_rows = int(input())
                if 0 < num_rows <= 10000:
                    print(second_pipe.fetch_sample_data(issuer_code=issuer_code_for_sample, limit=num_rows))
                else:
                    print(second_pipe.fetch_sample_data(limit=10000))
            else:
                print("The code you entered is not valid")

        # For debugging purposes
        # print(MSEStockScraper.no_table_codes)

        print("Press enter to close the program...")
        input()
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
