# This Python file uses the following encoding: utf-8
import requests
import bs4

class Weather():

    def __init__(self, zip):
        self.zip = zip

    def set_weather_page(self):
        page = 'https://weather.com/weather/today/l/{}:4:US'.format(self.zip)

        try:
            req = requests.get(page)
            req.raise_for_status()

            self.weatherPage = bs4.BeautifulSoup(req.text, "html.parser")

        except requests.HTTPError:
            raise

        except requests.ConnectionError:
            raise


    def get_temp(self):
        temp = self.weatherPage.find('span', class_="_-_-components-src-organism-CurrentConditions-CurrentConditions--tempValue--MHmYY")
        return temp.text

    def get_phrase(self):
        phrase = self.weatherPage.find('div', class_="_-_-components-src-organism-CurrentConditions-CurrentConditions--phraseValue--mZC_p")
        return phrase.text

    def get_city(self):
        city = self.weatherPage.find('h1', class_="_-_-components-src-organism-CurrentConditions-CurrentConditions--location--1YWj_")
        return city.text.replace('Weather', '')

    def get_tonight(self):
        tonight = self.weatherPage.find('div', class_="today-daypart-temp")
        return tonight.text

    def get_tonight_phrase(self):
        phrase = self.weatherPage.find('span', class_="today-daypart-wxphrase")
        return phrase.text
