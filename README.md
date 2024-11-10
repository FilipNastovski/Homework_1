# Macedonian Stock Exchange Data Analysis

## Project Description
This application automates the collection and processing of historical stock market data from the Macedonian Stock Exchange (MSE). Using a Pipe and Filter architecture, it systematically retrieves, processes, and stores daily stock market data for all listed issuers over the past decade. The system automatically handles data updates, ensuring the database remains current while avoiding duplicate entries.

## Requirements

### Functional Requirements
1. **Issuer Data Retrieval**
   - Automatically fetch all listed issuers from MSE website
   - Filter out bonds and numerical codes
   - Extract issuer codes from the dropdown menu

2. **Historical Data Management**
   - Retrieve historical data spanning at least 10 years
   - Check and store the last available date for each issuer
   - Update existing data with new entries

3. **Data Processing**
   - Format dates consistently (English format)
   - Format prices with proper delimiters (e.g., 21,600.00)
   - Validate and clean data before storage

4. **Database Operations**
   - Check existing data for each issuer
   - Identify and fill data gaps
   - Prevent duplicate entries

### Non-Functional Requirements
1. **Performance**
   - Efficient data retrieval and processing
   - Minimal system resource usage
   - Reasonable response times for data updates

2. **Reliability**
   - Error handling for network issues
   - Data consistency checks
   - Recovery from interruptions

3. **Maintainability**
   - Modular code structure
   - Version control

4. **Usability**
   - Simple and automatic setup process
   - Clear error messages

## System Architecture

### Class Structure
1. **IssuerCodeExtractor**
   - Handles web scraping of issuer codes
   - Filters invalid codes
   - Uses Selenium for web automation

2. **DatabaseManager**
   - Manages SQLite database operations
   - Handles data insertion and updates
   - Maintains data integrity

3. **DataScraper**
   - Coordinates data retrieval process
   - Implements threading for parallel processing
   - Manages the scraping queue

4. **MSEStockScraper**
   - Scrapes historical stock data
   - Formats data according to requirements
   - Handles web page navigation

## Setup Instructions

### Prerequisites
- Python 3.12 or higher
- Chrome/Firefox browser
- Internet connection

### Installation
1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Run the appropriate setup script:
- Windows: Double-click `run_for_windows.bat`
- Unix/Linux/Mac: Execute `./run_for_unix.sh`

The script will:
- Create a virtual environment
- Install required dependencies
- Initialize the database
- Start the data collection process

### Manual Setup (if needed)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the program
python main.py
```

## Database Structure
The application uses SQLite (`mse_stocks.db`) with the following structure:
- Date: Trading date
- Last Trade Price: Closing price
- Max: Daily maximum price
- Min: Daily minimum price
- Volume: Trading volume
- Turnover: Daily turnover in denars


## Data Flow
1. Extract issuer codes from MSE website
2. Check database for existing data
3. Determine date ranges for missing data
4. Retrieve and process missing data
5. Store formatted data in database


## Contact
[Filip Nastovski 221550 filip.nastovski.1@students.finki.ukim.mk]
