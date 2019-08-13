import requests
from bs4 import BeautifulSoup
import tldextract
from pathlib import Path
from News_Spider.spiders.concatenate import *
import pandas as pd


def WebCrawler(url,base_url,page):
    '''
    crawler using bs4 beautifulsoup
    :param url: url which the web crawler has to crawl
    :param base_url: base url to append on other links
    :param page: page to control recursion
    :return: a list containing links present in the url

    '''
#url = "https://timesofindia.indiatimes.com/home/headlines"
#base_url="https://timesofindia.indiatimes.com"
    ext = tldextract.extract(base_url)  # extracting info from url
    domain = ext.domain  # extracting domain
    date = str(datetime.date.today())  #getting present date
    dir_name = f"D://News_Spider/News_Spider/Crawled data/Links/Links{date}"  # hard coding dir name
    with open("D://News_Spider/News_Spider/Crawled data/allow_url.csv",'a') as fd:  # creating file for saving urls
        fd.write(base_url)
        fd.write("\n")
        logging.info("Allow url file appended")
    try:
        os.makedirs(dir_name)
        logging.info("Directory created for storing website links")
    except Exception as e:
        pass
    indir = Path(f"D://News_Spider/News_Spider/Crawled data/Links/Links{date}")
    cms ='.cms'    # checking extensions of articles and other important keywords to get useful urls only
    ece = '.ece'
    html = '.html'
    htm = '.htm'
    page = requests.get(url, verify=False)   # verify set to false to establish connection with websites without ssl certificates
    # urllib3 will throw warning message on scrapy command line
    soup = BeautifulSoup(page.content, 'html.parser')
    http = 'http://'
    https= 'https://'
    #iter_page = 0
    links=[]
    stop1 =str('#0')
    stop2 =str( '#o')   # stop words to be not be added in the list of links
    stop3=str( '#O')
    stop4 = str('javascript')
    stop5=str('javascript:void(0)')
    stop6 =str('javascript:void(0);')
    stop7=str('#')
    stop0=str('None')

    try:
        # finding links which are required by us
        for url in soup.find_all('a',recursive=True):
            linkss = url.get('href')
            logging.info(f"Links from website- {domain} being scraped")

            try:
                if cms in linkss or ece in linkss or html in linkss or htm in linkss or linkss[-1].isdigit() or linkss[-1] == '/' or linkss[-1].isalpha():
                    if http in linkss or https in linkss:
                        links.append(linkss)
                        logging.info("Link being appended into the list")
                    elif http not in linkss or https not in linkss:
                        if linkss[0] == '/' and linkss[1] == '/':
                            linkss = f"https:{linkss}"
                            links.append(linkss)
                        elif stop0 not in linkss or stop1 not in linkss or stop2 not in linkss or stop3 not in linkss or stop4 not in linkss or stop5 not in linkss or stop6 not in linkss or stop7 not in linkss :
                            links.append(base_url + linkss)
                            logging.info("Link being appended into the list")

                elif cms not in linkss:
                    if stop0 not in linkss or stop1 not in linkss or stop2 not in linkss or stop3 not in linkss or stop4 not in linkss or stop5 not in linkss or stop6 not in linkss or stop7 not in linkss:
                        for i in range(0):
                            WebCrawler(linkss, base_url,0)

                else:
                    break

                #try:
                 #   links.remove('https://timesofindia.indiatimes.comjavascript:void(0);')
                  #  links.remove('https://timesofindia.indiatimes.comjavascript:void(0)')
                #except Exception as e:
                 #   pass
            except Exception as e:
                pass

    except Exception as e:
        pass
    links=set(links)
    links=list(links)
    #print(links)


    file_name = f"Links_{domain}.csv"
    file_open = indir/file_name
    df = pd.DataFrame(links)
    df.to_csv(file_open,encoding='utf-8', index=False, header= False)
    logging.info("Links stored being written into a csv file")
    concatenate()
    return base_url   # returning base_url  of the link used for starting crawling


