import scrapy
from scrapy import Field
from News_Spider.spiders.main_wc import *
import csv
from newsplease import NewsPlease
import tldextract


class NewsItem(scrapy.Item):

    # Creating fields for storing scraped information
    Website = Field()
    Headline = Field()
    Time = Field()
    Author = Field()
    Article = Field()
    URL = Field()


class NewsSpider(scrapy.spiders.Spider):
    name = "ArticleScraper"

    main_wc()  # calling WebCrawler through a main function
    with open("D://News_Spider/News_Spider/Crawled data/AllLinks.csv",'r',encoding='utf-8') as file:
        reader = csv.reader(file)
        my_list = list(reader)  # list of urls to scrape from
    new_list =[''.join(x) for x in my_list]
    start_urls = new_list
    with open("D://News_Spider/News_Spider/Crawled data/allow_url.csv",'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        my_url = list(reader)
    url_list =[''.join(x) for x in my_url]
    allowed_domains = list(set(url_list))  # list of allowed_domains to scrape

    #rules = [Rule(LinkExtractor(), follow=True, callback='parse_item')]

    def parse(self, response):

        ext = tldextract.extract(response.url)
        domain = ext.domain  # website name taken from url

        obj = NewsItem()  # Item instance created
        art = NewsPlease.from_url(response.url)  # making connection with news-please library for extracting information
        obj['Time'] = art.date_publish

        obj['Website'] = domain
        obj['Headline'] = art.title

        obj['Article'] = art.text

        obj['Author'] = art.authors
        obj['URL'] = art.url
        yield obj
