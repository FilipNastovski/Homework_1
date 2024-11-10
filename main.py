import IssuerCodeExtractor
import DatabaseManager
import DataScraper
import subprocess
import time
import sys


def check_dependencies():
    """Check and install required dependencies"""

    """Check Python version and install required dependencies"""
    # Check if Python version is 3.12 or above
    if sys.version_info < (3, 12):
        print("Python 3.12 or higher is required.")
        sys.exit(1)
    else:
        print(f"Python {sys.version.split()[0]} detected. Proceeding with dependency check.\n")

    required_packages = {
        'lxml': 'lxml',
        'pandas': 'pandas',
        'selenium': 'selenium',
        'sqlite3': 'sqlite3'
    }

    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            print(f"Installing required package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            print(f"Successfully installed {package}")


def run_for_benchmark(first_pipe, second_pipe, third_pipe):
    """Run in most optimised mode for benchmark"""
    start_time = time.time()

    third_pipe.update_data(update_info=second_pipe.check_data_currency(first_pipe.filter_codes(
        first_pipe.get_issuer_codes())), max_threads=12)

    execution_time = time.time() - start_time

    print("Displaying a sample of the scraped data:")
    print(second_pipe.fetch_sample_data(30))

    print(f"\nScraping completed successfully in {execution_time:.2f} seconds\n\n")

    print("Press enter to close the program...")
    input()

def run_query_mode():
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
            if 0 < num_rows <= 500:
                print(second_pipe.fetch_sample_data(issuer_code=issuer_code_for_sample, limit=num_rows))
            else:
                print(second_pipe.fetch_sample_data(limit=500))
        else:
            print("The code you entered is not valid")

        print("Continue to query? ('n' for No, 'y' for Yes):")
        usr_in = input()
        if usr_in == 'y':
            pass
        else:
            exit(11)


if __name__ == "__main__":
    try:

        first_pipe = IssuerCodeExtractor.IssuerCodeExtractor()
        second_pipe = DatabaseManager.DatabaseManager()
        third_pipe = DataScraper.DataScraper(second_pipe)

        print("Checking and installing required dependencies...")
        check_dependencies()

        # TO DO add a query mode only for fetching data from database
        print("Enter string \"query\" to run the program in query mode")
        print("Enter string \"bench\" to run the program in benchmark mode or enter a number to exec normally")
        print("Enter string \"normal\" to run the program in normal (or leave blank to run the program in normal mode)")

        user_input = input()
        if user_input == "query":
            run_query_mode()
        if user_input == "bench":
            run_for_benchmark(first_pipe, second_pipe, third_pipe)
            exit(10)

        print("Enter the number of threads to be used in (Default = 4)")

        thread_number = input()
        if thread_number.isdigit() and 1 < int(thread_number) <= 32:
            thread_number = int(thread_number)
        else:
            thread_number = 4

        start_time = time.time()

        print("Getting issuer codes...")
        issuer_codes = first_pipe.get_issuer_codes()
        #issuer_codes = ["ADIN", "ALK"]
        print(f"Found {len(issuer_codes)} valid issuer codes\n")

        print("Filtering issuer codes...")
        issuer_codes = first_pipe.filter_codes(issuer_codes)
        print(f"Remaining codes: {len(issuer_codes)}\n")

        print("Checking data currency...")
        update_info = second_pipe.check_data_currency(issuer_codes)
        print(f"{len(update_info)} issuers need updating\n")

        if update_info:
            print("Starting data update...\n")
            third_pipe.update_data(update_info=update_info, max_threads=thread_number)
            print("\nData update completed\n")
        else:
            print("All data is up to date")

        execution_time = time.time() - start_time

        print("Display a sample of the scraped data? ('n' for No, 'y' for Yes):")
        usr_in = input()
        if usr_in == 'y':
            print("Enter issuer code you want the data for:")
            issuer_code_for_sample = input()
            if issuer_code_for_sample in issuer_codes:
                print("Enter how many rows to fetch:")
                num_rows = int(input())
                if 0 < num_rows <= 300:
                    print(second_pipe.fetch_sample_data(issuer_code=issuer_code_for_sample, limit=num_rows))
                else:
                    print(second_pipe.fetch_sample_data(limit=100))
            else:
                print("The code you entered is not valid")
                print(second_pipe.fetch_sample_data())

        print(f"\nScraping completed successfully in {execution_time:.2f} seconds\n\n")

        print("Press enter to close the program...")
        input()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
