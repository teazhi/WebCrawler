import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import sys

colorama.init()
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN

BOLD = '\033[1m'
RESET = colorama.Fore.RESET

global urls

internal_urls = set()
external_urls = set()
files1 = set()
urls = set()

extensions = set(line.strip() for line in open('extensions.txt'))

def checkValidLink(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and parsed.netloc.startswith("www.")


def getAllLinks(url, internal_urls, external_urls, files1, urls):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors

        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(response.content, "html.parser")

        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue

            href = urljoin(url, href)

            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            print(f"{GREEN}Processing URL: {href}{RESET}")

            if not checkValidLink(href):
                print(f"{YELLOW}Invalid URL: {href}")
                continue

            if domain_name == parsed_href.netloc:
                if href not in files1:
                    for exten in extensions:
                        if href.endswith(exten):
                            urls.add(href)
                            files1.add(href)
                            print(f"{RED}[#] File: {href}{RESET}")
                        else:
                            continue
                else:
                    continue
            else:
                if href not in external_urls:
                    if href not in internal_urls:
                        print(f"{GREEN}[*] Internal link: {href}{RESET}")
                        urls.add(href)
                        internal_urls.add(href)
                        links = getAllLinks(
                            href, internal_urls, external_urls, files1, urls
                        )
                        internal_urls.update(links[0])
                        external_urls.update(links[1])
                        files1.update(links[2])
                    else:
                        continue
                else:
                    continue

    except requests.exceptions.RequestException as e:
        print(f"{RED}[!] Error requesting URL: {url} - {e}{RESET}")

    return internal_urls, external_urls, files1

def crawl():
    links_to_crawl = [sys.argv[1]]  # Start with the initial URL
    iteration = 0
    max_iterations = 100
    while links_to_crawl and iteration < max_iterations:
        try:
            link = links_to_crawl.pop(0)  # Get the first link in the list
            links = getAllLinks(
                link, internal_urls, external_urls, files1, urls
            )
            internal_urls.update(links[0])
            external_urls.update(links[1])
            files1.update(links[2])
            links_to_crawl.extend(links[0])
            iteration += 1
        except requests.exceptions.RequestException as e:
            print(f"{RED}[!] Error requesting URL: {link}{RESET}")
            continue

def urlCrawl():
    try:
        crawl()
        print("")
        print(f"{CYAN + BOLD}•------------------------------•{RESET}")
        print("")
        print(" [+] Total Internal links:", len(internal_urls))
        print(" [+] Total External links:", len(external_urls))
        print(" [+] Total Files:", len(files1))
        print("")
        print(" [+] Total:", len(external_urls) + len(internal_urls) + len(files1))
        print("")
        print(f" {GREEN}██████████████████████████████")
        print("")
        print(f"{CYAN}•------------------------------•")

        with open('output.txt', 'w+') as f:
            for item in internal_urls:
                f.write(item + "\n")
            for item2 in files1:
                f.write(item2 + "\n")
    except:
        pass

urlCrawl()


