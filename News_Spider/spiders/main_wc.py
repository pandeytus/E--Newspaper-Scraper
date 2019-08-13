from News_Spider.spiders.WebCrawler import *
from News_Spider.spiders.PaperLinks import *

def main_wc():
    pages = 5

    url = NewsLinks
    #url = input("Input the website you wish to scrape articles from\n")
    #complete_url = f"https://{url}"

    for links in url:
        WebCrawler(links,links,pages)


