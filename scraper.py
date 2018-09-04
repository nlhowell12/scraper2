import argparse
import requests
import re
import sys
from bs4 import BeautifulSoup


def create_parser():
    """Creates an argument parser for this file"""
    parser = argparse.ArgumentParser(
        description='Scrapes a url for urls, emails, and phone numbers'
    )
    parser.add_argument('url', help='URL to scrape')
    return parser


def find_urls(url):
    """Finds all the URLs inside the html of a page"""
    print 'URLS:'
    for url in set(re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
            r'(?:%[0-9a-fA-F][0-9a-fA-F]))+', url.text)):
        print url


def find_emails(url):
    """Finds all the email addresses in the html of a page"""
    print 'Emails:'
    for email in set(re.findall(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", url.text)):
        print email


def find_phone(url):
    """Finds all the phone numbers in the html of a page"""
    print 'Phone Numbers'
    for phone in set(re.findall(
        r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})'
            r'(\se?x?t?(\d*))?', url.text)):
        print "-".join(phone[0:3])


def making_soup_relative(url):
    soup = BeautifulSoup(url.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    for link in soup.find_all('img'):
        urls.append(link.get('src'))
    for link in set(urls):
        print link


def main():
    parser = create_parser().parse_args()
    if not parser.url:
        print parser.help
        sys.exit(1)
    else:
        response = requests.get(parser.url)
        # find_urls(response)
        # find_emails(response)
        # find_phone(response)
        making_soup_relative(response)


if __name__ == "__main__":
    main()
