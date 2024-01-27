import urllib.request
from bs4 import BeautifulSoup

url = ["https://www.rootsandrain.com/organiser137/ews/events/filters/seriess342,351,509," + \
      "655,907,1085,1161,1344,1521,1623/",
      "https://www.rootsandrain.com/event-list/filters/2023/seriess1623/"]

BASE = "https://www.rootsandrain.com"

def resultsparser(u):
    print(u)

for u in url:
    with urllib.request.urlopen(u) as resp:
        soup = BeautifulSoup(resp, 'html.parser')
        table = soup.find('table', class_='list')
        for row in table.tbody.find_all('tr'):
            for anchor in row.find_all('a'):
                if str.find(anchor.get('href'),'event') > 0 and \
                        str.find(anchor.get('href'),'photos') < 0 and \
                        str.find(anchor.get('href'),'videos') < 0:
                    resultsparser(BASE + anchor.get('href'))
