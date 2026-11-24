# total = 200
# count_rain = 9
# count_drainpipe = 56

# print('총 데이터: ', total, '개')
# print('호우 원인: ', count_rain, '개 (', count_rain/total*100, '%)')
# print('노후 및 노수 하수도관 원인: ', count_drainpipe, '개 (', count_drainpipe/total*100, '%)')

# import matplotlib.pyplot as plt

# causes = ['Heavy Rain', 'Old drainpipe', 'other']
# counts = [9, 56, 200 - 9 - 56]

# plt.bar(causes, counts, color=['skyblue', 'orange', 'gray'])
# plt.title('The Causes of Sinkhole')
# plt.xlabel('Cause')
# plt.ylabel('Number')
# plt.show()

# import matplotlib.pyplot as plt
# import pandas as pd

# cityNameMap = {
#     '부천시': 'Bucheon-si',
#     '화성시': 'Hwaseong-si',
#     '의왕시': 'Uiwang-si',
#     '남양주시': 'Namyangju-si',
#     '고양시 일산서구': 'Goyang-si Ilsanseo-gu',
#     '고양시 일산동구': 'Goyang-si Ilsandong-gu',
#     '파주시': 'Paju-si',
#     '과천시': 'Gwacheon-si',
#     '의정부시': 'Uijeongbu-si',
#     '평택시': 'Pyeongtaek-si',
#     '구리시': 'Guri-si'
# }

# df = city_count.dataFrame()
# city_counts = df['City'].value_counts()
# city_counts_top10 = city_counts.head(10)

# city_counts_top10.index = city_counts_top10.index.map(cityNameMap)

# plt.figure(figsize=(10, 5))
# city_counts_top10.plot(kind='bar', color='green')
# plt.title('Top 10 Sinkhole-Prone Cities in Gyeonggi-do')
# plt.xlabel('City')
# plt.ylabel('Number of Sinkholes')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

import pandas as pd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import os

self.api_key=os.getenv("API_KEY")

if not self.api_key:
    raise ValueError("API_KEY environment variable is not set")

class SinkholeData:
    def __init__(self, startnumber=1, endnumber=1000):
        self.startnumber=startnumber
        self.endnumber=endnumber
        self.api_key = os.getenv("API_KEY")
    
        self.sido_nmlist = []
        self.signgu_nmlist = []
        self.detail_infolist = []
        self.occur_datelist = []
        self.occur_regionlist = []
        self.causelist = []

    def dataArrange(self):
        for page in range(1, 5):
            url = 'https://openapi.gg.go.kr/Tgrdsubsidinfo'
            params = {
                'KEY': self.api_key,
                'pIndex': page,
                'pSize': 50
            }
            req = requests.get(url, params=params)
            html = req.text
            soup = BeautifulSoup(html, 'xml')
            
            signgu_nm = soup.find_all('SIGNGU_NM')
            detail_info = soup.find_all('TGRD_SUBSID_REGION_DETAIL_INFO')
            occur_date = soup.find_all('OCCUR_DE')
            occur_region = soup.find_all('OCCUR_REGION_GEOFET_KIND_NM')
            cause = soup.find_all('FIRST_OCCUR_CAUSE')

            for code in signgu_nm:
                self.signgu_nmlist.append(code.text)
            for code in detail_info:
                self.detail_infolist.append(code.text)
            for code in occur_date:
                self.occur_datelist.append(code.text)
            for code in occur_region:
                self.occur_regionlist.append(code.text)
            for code in cause:
                self.causelist.append(code.text)

    def dataFrame(self):
        data = {
            'City' : self.signgu_nmlist, 
            'Occur Date' : self.occur_datelist, 
            'Occur Region' : self.occur_regionlist, 
            'Detail Information' : self.detail_infolist, 
            'First Occur Cause' : self.causelist
        }
        df = pd.DataFrame(data)
        return df
    
class HeavyRain(SinkholeData):
    def __init__(self, startnumber=1, endnumber=1000):
        super().__init__(startnumber, endnumber)
        self.dataArrange()

    def countCause(self):
        cnt = 0
        for cause in self.causelist:
            if '호우' in cause:
                cnt += 1
        return cnt

cause_count = HeavyRain(1, 1000)
cnt = cause_count.countCause()
print('호우 원인 개수:', cnt)

class Drainpipe(SinkholeData):
    def __init__(self, startnumber=1, endnumber=1000):
        super().__init__(startnumber, endnumber)
        self.dataArrange()

    def countCause(self):
        cnt = 0
        cnt2 = 0
        for cause in self.causelist:
            if '하수관' in cause:
                cnt += 1
            elif '노후' in cause:
                cnt2 += 1
        return cnt, cnt2

cause_count = Drainpipe(1, 1000)
cnt = cause_count.countCause()
print('하수관 노후 및 누수 원인 개수:', cnt)

class City(SinkholeData):
    def __init__(self, startnumber=1, endnumber=1000):
        super().__init__(startnumber, endnumber)
        self.dataArrange()
        self.dataFrame()

    def cityCount(self):
        df = pd.DataFrame({'City': self.signgu_nmlist})
        return df['City'].value_counts()

city_count = City(1, 1000)    
city_count.cityCount()

if __name__ == "__main__":
    sinkhole = SinkholeData()
    sinkhole.dataArrange()
    df = sinkhole.dataFrame()
    print(df.head())
