# Website Crawler

This Python code is designed to crawl a website and gather information about its internal and external links, as well as files present on those websites. It can be useful for tasks such as website analysis, SEO optimization, link verification, and file scraping.

## Features

- Crawls a website to extract internal and external links, and files
- Validates and filters links based on specified criteria
- Generates a list of internal URLs and files found during the crawling process
- Provides a summary of the total number of internal and external links, and files

## Installation

To use this code, you need to have Python installed on your system. You can install the necessary libraries by running the following command:

```python3
pip install requests bs4 colorama
```

## Usage

1. Modify the `extensions.txt` file: Add the file extensions you want to consider during the crawling process, with each extension on a new line.

2. Run the code: Open a terminal or command prompt and navigate to the directory containing the Python script. Then run the script with the URL as a command-line argument. For example:

```python website_crawler.py https://example.com```

3. Results: The script will print the progress of the crawling process and provide a summary of the total number of internal and external links, and files found. It will also generate an `output.txt` file containing the list of internal URLs and files.

## Notes

- Make sure to respect the website's terms of service and robots.txt files when crawling.
- Be aware of the legal and ethical implications of crawling and scraping websites. Ensure your actions comply with applicable laws and regulations.




