import argparse
import csv
import re
import requests
from collections import Counter
from io import StringIO


# Part I - Pull down web log file """downloading log file content from input URL"""
def download_file(url):                 #
    response = requests.get(url)                        # HTTP GET request to url
    response.raise_for_status()                          # request status or error
    return StringIO(response.text)                      # returned text like file


# Part II - Process file using CSV module
def process_csv(csvfile):
    return list(csv.reader(csvfile))


# Part III - Search and count image hits
def count_image(csvdata):
    pattern = re.compile(r'.*.\.(jpg|gif|png)$', re.IGNORECASE)                          # re to match file type,ignore case
    total = len(csvdata)                                                                        # total rows
    image_hits = sum(1 for row in csvdata if pattern.match(row[0]))                             # match
    percentage = (image_hits / total) * 100 if total else 0                                     # percentage calc
    print(f"Image requests account for {percentage:.1f}% of all requests")


# Part IV - Finding most popular browser
def browser_type(csvdata):
    browser_patterns = {                                                                         # re to find browser in strings
        'Firefox': re.compile(r'Firefox', re.IGNORECASE),
        'Chrome': re.compile(r'Chrome', re.IGNORECASE),
        'Internet Explorer': re.compile(r'Internet Explorer', re.IGNORECASE),
        'Safari': re.compile(r'Safari(?!.*Chrome)', re.IGNORECASE)                        # when chrome is not present in string
    }
    count = Counter()

    for row in csvdata:                                                                     # extract browser info from 3rd column
        for browser, pattern in browser_patterns.items():
            if pattern.search(row[2]):
                count[browser] += 1
                break
    if count:
        most_common = count.most_common(1)
        print(f"The most popular browser today is: {most_common[0][0]}")
    return count


# Main function to execute
def main(url):
    file = download_file(url)
    csv_data = process_csv(file)
    count_image(csv_data)
    browser_type(csv_data)
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)



