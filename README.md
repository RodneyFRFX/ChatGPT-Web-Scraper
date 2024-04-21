# Web Scraping and Filtering for Malware Detection in the PowerIndustry

This Python script is designed to scrape URLs, filter out those containing potential malware-related content, and write the filtered results to a CSV file along with the relevant text content.

## Setup Instructions
1. Ensure you have Python installed on your system.
2. Install the required libraries by running:
    ```
    pip install requests beautifulsoup4 nltk numpy
    ```
3. Clone or download the script to your local machine.

## Usage
1. Open the script in a Python environment or execute it via the command line.
2. Run the script to start the web scraping and filtering process.

## Script Overview
### Libraries
- `urllib.parse`: For URL manipulation and joining.
- `requests`: For making HTTP requests.
- `bs4 (BeautifulSoup)`: For parsing HTML content.
- `nltk`: For text processing utilities.
- `time`: For time-related functionalities.
- `threading`: For concurrent execution of tasks.
- `queue`: For managing queues of URLs.
- `csv`: For CSV file operations.
- `os`: For system-related operations.
- `numpy`: For numerical operations.

### Functions
1. `Scraper(url, q)`: Scrapes URLs from a given webpage and adds them to the queue `q`.
2. `multiScraper(queue, filtered)`: Multi-threaded version of `Scraper`.
3. `Filter(q, filtered)`: Filters URLs containing potential malware-related content and adds them to the `filtered` queue.
4. `multiFilter(queue, filtered)`: Multi-threaded version of `Filter`.
5. `is_ascii(s)`: Checks if a string is ASCII.
6. `mask(soup, link, title, visited)`: Applies filtering based on keywords and other criteria.
7. `filterScrapeWrite(url, visited)`: Scrapes, filters, and writes to CSV for a given URL.
8. Other auxiliary functions for managing queues and file I/O.

## Example Usage
- Define a starting URL.
- Run the `filterScrapeWrite` function to initiate the scraping and filtering process.
- Subsequently, run multiple iterations to perform deeper scraping and filtering using a multi-threaded approach.

## Notes
- Ensure proper exception handling and error logging to handle any issues during scraping and filtering.
- Adjust parameters such as the number of generations and threading as per your requirements.
- Make sure to respect website terms of service and robots.txt when scraping.

## Author
This script was authored by [Rodney Frazier]

