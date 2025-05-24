# code from last years course https://git.arts.ac.uk/jmurr/bsc-big-data/blob/main/week_02/01_crawling.py
from bs4 import BeautifulSoup
import requests
import random
import time


def get_soup(wiki_suffix):
    url = url = "https://en.wikipedia.org" + wiki_suffix
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")

    return soup


def link_is_valid(link):
    ignores = [
        "png",
        "jpg",
        "jpeg",
        "isbn",
        "svg",
        "identifier",
        "File",
        "Special",
        "Template",
        "Mailto",
        "Portal",
        "Help",
        "Category",
        "Talk",
        "Wikipedia",
        "Main_Page",
    ]

    if link.startswith("/wiki/"):
        valid = True
        for ignore in ignores:
            if ignore in link:
                valid = False
                break
    return valid


def get_links(soup):
    links = []

    for a in soup.find_all("a"):
        try:
            link = a["href"]
            if link_is_valid(link):
                links.append(link)
        except:
            pass

    return links


def crawl(seed):
    links_visited = []
    suffix = "/wiki/" + seed
    for i in range(10):
        soup = get_soup(suffix)
        links = get_links(soup)
        suffix = random.choice(links)
        links_visited.append(suffix)
    return links_visited


if __name__ == "__main__":
    seed = input("Enter a keyword:")
    suffix = "/wiki/" + seed
    print(f"Starting off with {suffix}")

    while True:
        soup = get_soup(suffix)
        links = get_links(soup)
        suffix = random.choice(links)
        print(f"Visited: {suffix}")

        time.sleep(3)
