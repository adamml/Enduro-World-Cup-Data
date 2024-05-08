"""A module to scrape and manipulate results from the UCI Mountain Bike Enduro
World Cup.

    :author: Adam Leadbetter (@adamml)
"""

import urllib.request
from bs4 import BeautifulSoup
from typing import Optional

_URL_LIST = [[2023,1,"Maydena, Tasmania", "AUS", "F", "https://ucimtbworldseries.com/results/raceCategory/maydena-edr-women-elite/2023"],
             [2023,1,"Maydena, Tasmania", "AUS", "M", "https://ucimtbworldseries.com/results/raceCategory/maydena-edr-men-elite/2023"],
             [2023,2,"Derby, Tasmania", "AUS", "M", "https://ucimtbworldseries.com/results/raceCategory/derby-edr-men-elite/2023"],
             [2023,2,"Derby, Tasmania", "AUS", "F", "https://ucimtbworldseries.com/results/raceCategory/derby-edr-women-elite/2023"],
             [2023, 3, "Finale Ligure", "ITA", "M", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-finale-outdoor-region-edr-men-elite/2023"],
             [2023, 3, "Finale Ligure", "ITA", "F", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-finale-outdoor-region-edr-women-elite/2023"],
             [2023, 4, "Leogang", "AUT", "M", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-leogang-salzburgerland-edr-men-elite/2023"],
             [2023, 4, "Leogang", "AUT", "F", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-leogang-salzburgerland-edr-women-elite/2023"],
             [2024, 5, "Val Di Fassa Trentino", "ITA", "M", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-val-di-fassa-trentino-edr-men-elite/2023"],
             [2024, 5, "Val Di Fassa Trentino", "ITA", "F", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-val-di-fassa-trentino-edr-women-elite/2023"],
             [2024, 6, "Loudenville-Peyragudes", "FRA", "M", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-loudenvielle-peyragudes-edr-men-elite/2023"],
             [2024, 6, "Loudenville-Peyragudes", "FRA", "F", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-loudenvielle-peyragudes-edr-women-elite/2023"],
             [2024, 7, "Les Gets", "FRA", "M", "https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-les-portes-du-soleil-edr-men-elite/2023"],
             [2023,7,"Les Gets","FRA","F","https://ucimtbworldseries.com/results/raceCategory/uci-edr-world-cup-les-portes-du-soleil-edr-women-elite/2023"]]
"""A private module level variable listing all the URLs to scrape data from"""

class StageRecord:
    """This class describes an individual record of a rider's result for a
    given stage of a given round of the Enduro World Series or UCI Mountain
    Bike Enduro World Cup"""
    def __init__(self,
                 event_stage_sequence: int,
                 position: Optional[int],
                 stage_time_seconds: Optional[float],
                 stage_points: Optional[int]):
        self.__event_stage_sequence = event_stage_sequence
        self.__position = position
        self.__stage_points = stage_points
        self.__stage_time_seconds = stage_time_seconds

    @property
    def event_stage_sequence(self) -> int:
        return self.__event_stage_sequence
        
    @property
    def position(self) -> Optional[int]:
        return self.__position
    
    @property
    def stage_time_seconds(self) -> Optional[float]:
        return self.__stage_time_seconds
    
    @property
    def stage_points(self) -> Optional[int]:
        return self.__stage_points
        
    def asDict(self) -> dict:
        return {
            "event_stage_sequence": self.__event_stage_sequence,
            "position": self.__position,
            "stage_time_seconds": self.__stage_time_seconds,
            "stage_points": self.__stage_points
        }

class DataRecord:
    """This  class describes an individual record of a rider's result for a
    given round of the Enduro World Series or UCI Mountain Bike Enduro
    World Cup"""
    def __init__(self,
                 event_year: int,
                 event_year_sequence: int,
                 event_location: str,
                 event_location_nation: str,
                 elite_m_or_f: str,
                 rider: Optional[str]="",
                 rider_id: Optional[int]=0,
                 team: Optional[str]=None,
                 nation: Optional[str]="",
                 position: Optional[int]=None,
                 dnf: Optional[bool]=False,
                 dns: Optional[bool]=False,
                 event_time_seconds: Optional[float]=None,
                 event_delta_seconds: Optional[float]=None,
                 event_points: Optional[int]=0,
                 stages: Optional[list]=[]):
        self.__event_year = event_year
        self.__event_year_sequence = event_year_sequence
        self.__event_location = event_location
        self.__event_location_nation = event_location_nation
        self.__elite_m_or_f = elite_m_or_f
        self.__rider = rider
        self.__rider_id = rider_id
        self.__team = team
        self.__nation = nation
        self.__position = position
        self.__dnf = dnf
        self.__dns = dns
        self.__event_time_seconds = event_time_seconds
        self.__event_delta_seconds = event_delta_seconds
        self.__event_points = event_points
        self.__stages = stages

    @property 
    def rider(self) -> Optional[str]:
        return self.__rider
    
    @property
    def team(self) -> Optional[str]:
        return self.__team
    
    @property
    def nation(self) -> Optional[str]:
        return self.__nation
    
    @property
    def position(self) -> Optional[int]:
        return self.__position
    
    @property
    def dnf(self) -> Optional[bool]:
        return self.__dnf
    
    @property
    def dns(self) -> Optional[bool]:
        return self.__dns
    
    @property
    def event_time_seconds(self) -> Optional[float]:
        return self.__event_time_seconds
    
    @property
    def event_delta_seconds(self) -> Optional[float]:
        return self.__event_delta_seconds
    
    @property
    def stages(self) -> Optional[list]:
        return self.__stages

    def asDict(self) -> dict:
        """Returns the instance of DataRecord as a Python `dict`"""
        return {
            "event_year": self.__event_year,
            "event_year_sequence": self.__event_year_sequence,
            "event_location": self.__event_location,
            "event_location_nation": self.__event_location_nation,
            "elite_m_or_f": self.__elite_m_or_f,
            "rider": self.__rider,
            "rider_id": self.__rider_id,
            "team": self.__team,
            "nation": self.__nation,
            "position": self.__position,
            "dnf": self.__dnf,
            "dns": self.__dns,
            "event_time_seconds": self.__event_time_seconds,
            "event_time_delta": self.__event_delta_seconds,
            "event_points": self.__event_points,
            "stages": self.__stages
        }


def _hhmmssStrToFloat(hhmmss:str) -> float:
    return ((float(hhmmss.split(":")[0])* 3600) +
            (float(hhmmss.split(":")[1])* 60) +
            float(hhmmss.split(":")[2]))

def fetchData() -> list:
    results = []
    """Scrape all results from the UCI Mountain Bike World Cup website"""
    for url in _URL_LIST:
        with urllib.request.urlopen(str(url[5])) as uopen:
            soup = BeautifulSoup(uopen, 'html.parser')
            stages = []
            for table in soup.find_all('tbody'):
                if str(table.get('class')).find('divide') > -1:
                    i: int = 0
                    rider: Optional[str] = None
                    rider_id: Optional[int] = None
                    team: Optional[str] = None
                    nation: Optional[str] = None
                    dnf: Optional[bool] = None
                    dns: Optional[bool] = None
                    racetime: Optional[float] = None
                    racedelta: Optional[float] = None
                    position: Optional[int] = None
                    points: Optional[int] = None
                    stages = []
                    for tr in table.find_all('tr'):
                        for tc in tr.find_all('a'):
                            for h3 in tc.find_all('h3'):
                                if rider is not None and \
                                            h3.get_text().title() != rider:
                                    results.append(DataRecord(
                                        url[0], url[1], url[2], url[3], url[4],
                                        rider, rider_id, team, nation, position, dnf,
                                        dns, racetime, racedelta, points, stages))
                                rider = h3.get_text().title().strip()
                                try:
                                    rider_id = int(tc.get('href').split('/')[-1])
                                except ValueError:
                                    rider_id = None
                                team = None
                                nation = None
                                position = None
                                dnf = None
                                dns = None
                                racetime = None
                                racedelta = None
                                points = None
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
                                if position == 1:
                                    racetime = _hhmmssStrToFloat(tr.find_all('td')[3].get_text().strip())
                                    winning_time: float = racetime
                                    racedelta = float(0)
                                else:
                                    try:
                                        racedelta = _hhmmssStrToFloat(tr.find_all('td')[3].get_text().strip())
                                        racetime = racedelta + winning_time
                                    except ValueError:
                                        racedelta = None
                                        racetime = None
                                try:
                                    points = int(tr.find_all('td')[4].get_text().strip())
                                except ValueError:
                                    points = 0
                            for p in tc.find_all('p'):
                                team = p.get_text().title().strip()
                        for t2 in tr.find_all('table'):
                            passed_head = False
                            for tr2 in t2.find_all('tr'):
                                if passed_head:
                                    td2 = tr2.find_all('td')
                                    st_seq = int(td2[0].get_text().strip().split(' ')[1])
                                    try:
                                        st_pos = int(td2[2].get_text().strip())
                                    except ValueError:
                                        st_pos = None
                                    try:
                                        st_tim = _hhmmssStrToFloat(td2[1].get_text().strip()[4:])
                                    except ValueError:
                                        st_tim = None
                                    try:
                                        st_pts = int(td2[3].get_text().strip())
                                    except ValueError:
                                        st_pts = None
                                    stages.append(StageRecord(
                                        st_seq,
                                        st_pos,
                                        st_tim,
                                        st_pts
                                    ))
                                else:
                                    passed_head = True
                                    stages = []
                    results.append(DataRecord(
                        int(url[0]), int(url[1]), str(url[2]), str(url[3]), str(url[4]),
                        rider, rider_id, team, nation, position,
                        dnf, dns, racetime, racedelta, stages=stages))
    return results
