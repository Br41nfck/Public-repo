import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import itertools


### TEST DATA ###
url1 = "https://www.w3schools.com/html/html_tables.asp"
url2 = 'https://getbootstrap.com/docs/4.0/content/tables/'
url3 = 'https://www.javatpoint.com/html-table'
url4 = 'https://www.freecodecamp.org/news/html-tables-table-tutorial-with-css-example-code/'
url5 = 'https://html5css.ru/tags/tag_table.php'
url6 = 'https://www.mousedc.ru/learning/6-tablitsy-table-tr-td-th-html/'
url7 = 'https://html.com/tables/'
url8 = 'https://htmlreference.io/tables/'


url_list = [url1, url2, url3, url4, url5, url6, url7, url8]


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
        "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"
                   ]

    user_agent = {"User-Agent": user_agents[random.randint(0, len(user_agents) - 1)]}

    return user_agent


def get_url(urls):

    site_text = requests.get(urls, headers=get_random_user_agent()).text
    soup = BeautifulSoup(site_text, 'lxml')

    # Delete links
    for link in soup.find_all('a', href=True):
        link.extract()

    # Delete blank tags
    for tag in soup.find_all():
        if len(tag.get_text(strip=True)) == 0:
            tag.extract()

    data = []
    table = soup.find('table')

    headers = [head.text.strip() for head in table.find_all('th')]
    print(headers)
    rows = table.find_all('tr')

    # Write rows to data
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    # Delete blank elements
    for elem in data:
        if not elem:
            data.remove(elem)

    data = list(itertools.chain(*data))
    # print(data)
    return data


def write_to_xls(urls):
    name = urls.split("/")
    name = name[2]
    table = get_url(urls)
    print(table)
    df = pd.DataFrame(table)
    df.to_excel(str(name+'.xlsx'))
    print('#'*10, "Done")


# get_url(url)

for url in url_list:
    write_to_xls(url)
