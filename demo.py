import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.entrepreneur.com'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

linksitem = []
for x in range(1,2):
    r = requests.get(f'https://www.entrepreneur.com/franchises/category/personal-care-businesses/{x}')
    soup = BeautifulSoup(r.content, 'lxml')

    tablelist = soup.find_all('table', class_='w-full bg-white shadow overflow-hidden sm:rounded-md table-fixed')

    for item in tablelist:
        for link in item.find_all('a', class_='flex items-center w-full', href=True):
            linksitem.append(baseurl + link['href'])
    # print(linksitem)

# testlink = 'https://www.entrepreneur.com/franchises/greatclips/282392'

entrepreneurlist = []
for link in linksitem:
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    tableabout  = soup.find_all('div', class_='bg-white shadow pb-2 sm:rounded-lg mb-12')[0]
    industry = tableabout.find_all('dd', class_='mt-1 text-base text-gray-900 font-normal sm:mt-0 sm:col-span-2')[0].text.strip()
    relatedcategories = tableabout.find_all('dd', class_='mt-1 text-base text-gray-900 font-normal sm:mt-0 sm:col-span-2')[1].text.strip()

    entrepreneur = {
        'industry': industry,
        'relatedcategories': relatedcategories
    }
    entrepreneurlist.append(entrepreneur)
    print('Saving:', entrepreneur['industry'])

df = pd.DataFrame(entrepreneurlist)
print(df.head(15))

df.to_csv('entrepreneur.csv')
