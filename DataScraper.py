from datetime import datetime, date
from typing import Optional, Dict
from queue import Queue
from queue import Empty
import DatabaseManager
import MSEStockScraper
import pandas as pd
import threading


class DataScraper:
    """Third pipe: Scrape and store missing data."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.queue = Queue()
        self.error_lock = threading.Lock()
        self.errors = []

    def scrape_issuer(self, issuer_code: str, start_date: Optional[date] = None):
        """Scrape data for a single issuer."""
        try:
            scraper = MSEStockScraper.MSEStockScraper(issuer_code)
            today = datetime.now().date()  # Get today's date (without time)

            if not start_date:
                years = 10
            else:
                years = (today - start_date).days // 365 + 1

            data = scraper.scrape_historical_data(years=years)

            if data is not None and not data.empty:
                if start_date:
                    data = data[data['Date'] > start_date]

                # Clean the DataFrame
                for col in data.columns:
                    if col not in ['Date']:  # Skip date column
                        data[col] = pd.to_numeric(data[col], errors='coerce')

                self.db_manager.save_data(data, issuer_code)
            else:
                with self.error_lock:
                    self.errors.append(f"No data retrieved for {issuer_code}")

        except Exception as e:
            with self.error_lock:
                self.errors.append(f"Error scraping {issuer_code}: {str(e)}")

    def process_queue(self):
        """Process items from the queue using multiple threads."""
        while True:
            try:
                issuer_code, start_date = self.queue.get_nowait()
                self.scrape_issuer(issuer_code, start_date)
                self.queue.task_done()
            except Empty:
                break
            except Exception as e:
                with self.error_lock:
                    self.errors.append(f"Queue processing error: {str(e)}")
                self.queue.task_done()

    def update_data(self, update_info: Dict[str, Optional[datetime]], max_threads: int = 200):
        """Update data for all issuers that need updating."""
        # Clear previous errors
        self.errors = []

        # Fill queue with work items
        for issuer_code, last_date in update_info.items():
            self.queue.put((issuer_code, last_date))

        # Create and start worker threads
        threads = []
        thread_count = min(max_threads, len(update_info))
        for _ in range(thread_count):
            thread = threading.Thread(target=self.process_queue)
            thread.daemon = True
            thread.start()
            threads.append(thread)

        # Wait for all work to be completed
        self.queue.join()

        for thread in threads:
            thread.join()

        # Report any errors that occurred
        if self.errors:
            print("\nErrors encountered during scraping:")
            for error in self.errors:
                print(error)
