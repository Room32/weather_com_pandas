import pandas as pd
import requests
from bs4 import BeautifulSoup

dict = {}
index = ['temperature', 'sky', 'rain', 'wind']

def download_data(url = 'https://weather.com/weather/tenday/l/cab89b601f184244370b4cc259412b0c2c9f09e700a719a4d7201fa0082269bc'):

    response = requests.get(url).text

    with open('weather.html', 'w', encoding='utf-8') as file:
        file.write(response)

def find_data():

    with open('weather.html', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'lxml')
    group_details = soup.find_all('details', class_='DaypartDetails--DayPartDetail--2XOOV Disclosure--themeList--1Dz21')

    for i in group_details:

        info_per_day = i.find_next('summary', class_='Disclosure--Summary--3GiL4 DaypartDetails--Summary--3Fuya Disclosure--hideBorder'
                    'OnSummaryOpen--3_ZkO').find_next('div', class_='DaypartDetails--DetailSummaryContent--1-r0i Disclo'
                    'sure--SummaryDefault--2XBO9').find_next('div', class_='DetailsSummary--DetailsSummary--1DqhO DetailsSummary--fadeOnOpen--KnNyF')

        data_day = info_per_day.find_next('h3', class_='DetailsSummary--daypartName--kbngc').text
        data_temperature_max = info_per_day.find_next('div', class_='DetailsSummary--temperature--1kVVp').\
            find_next('span', class_='DetailsSummary--highTempValue--3PjlX').text
        data_temperature_min = info_per_day.find_next('div', class_='DetailsSummary--temperature--1kVVp').\
            find('span', class_='DetailsSummary--lowTempValue--2tesQ').text
        data_sky = info_per_day.find('span', class_='DetailsSummary--extendedData--307Ax').text
        data_rain_probability = info_per_day.find('div', class_='DetailsSummary--precip--1a98O').find('span').text
        data_wind = info_per_day.find('span', class_='Wind--windWrapper--3Ly7c undefined').text

        dict[data_day] = [data_temperature_max+'/'+data_temperature_min, data_sky, data_rain_probability, data_wind]


if __name__ == '__main__':
    download_data()
    find_data()
    df = pd.DataFrame(dict, index=index).to_csv('weather.csv')
