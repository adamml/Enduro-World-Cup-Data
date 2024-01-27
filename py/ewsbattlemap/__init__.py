"""A module to scrape and manipulate results from the UCI Mountain Bike Enduro
World Cup.

    :author: Adam Leadbetter (@adamml)
"""

import urllib.request
from bs4 import BeautifulSoup

__URL_LIST__ = ["https://ucimtbworldseries.com/results/raceCategory/" + 
                "uci-edr-world-cup-les-portes-du-soleil-edr-women-elite"]
"""A private module level variable listing all the URLs to scrape data from"""

def __dumpData(rider: str or None, 
               team: str or None, 
               nation: str or None,
               position: int or None,
               dnf: bool,
               dns: bool):
    """A private function to dump the data for a record"""
    if team is None:
        team = 'NULL'
    else:
        team = f"\"{team}\""
    ps_str: str = ""
    dnf_str: str = ""
    if position is None:
        ps_str = "NULL"
    else:
        ps_str = str(position)
    if dnf is False:
        dnf_str = 'FALSE'
    else:
        dnf_str = 'TRUE'
    if dns is False:
        dns_str = 'FALSE'
    else:
        dns_str = 'TRUE'
    print(f'{{\"rider\": \"{rider}\", \"team\": {team}, \"nation\": \"{nation}\", \"position\": {ps_str}, \"dnf\": {dnf_str}, \"dns\": {dns_str}}}')

def fetchData():
    """Scrape all results from the UCI Mountain Bike World Cup website"""
    print(__URL_LIST__)
    for url in __URL_LIST__:
        with urllib.request.urlopen(url) as uopen:
            soup = BeautifulSoup(uopen, 'html.parser')

            for table in soup.find_all('tbody'):
                if str(table.get('class')).find('divide') > -1:
                    i: int = 0
                    rider: str or None = None
                    team: str or None = None
                    nation: str or None = None
                    dnf: bool or None = None
                    dns: bool or None = None
                    for tr in table.find_all('tr'):
                        for tc in tr.find_all('a'):
                            for h3 in tc.find_all('h3'):
                                if rider is not None and \
                                            h3.get_text().title() != rider:
                                    __dumpData(rider, team, nation,
                                               position, dnf, dns)
                                rider = h3.get_text().title().strip()
                                team = None
                                nation = None
                                position = None
                                dnf = None
                                dns = None
                                for svg in tr.find_all('svg'):
                                    nation = str(svg.get('id')).split('-')[1]
                                try:
                                    position = int(
                                        tr.find_all('td')[0].get_text())
                                    dnf = False
                                    dns = False
                                except ValueError:
                                    if tr.find_all(
                                            'td')[0].get_text(
                                            ).strip() == "DNF":
                                        dnf = True
                                        dns = False
                                    elif tr.find_all(
                                            'td')[0].get_text(
                                            ).strip() == "DNS":
                                        dnf = False
                                        dns = True
                                print(tr.find_all('td')[3].get_text().strip())
                            for p in tc.find_all('p'):
                                team = p.get_text().title().strip()

                    
                    __dumpData(rider, team, nation, position, dnf, dns)
                    
                        