# -*- coding:utf8 -*-
from __future__ import print_function, absolute_import, unicode_literals
from errbot import BotPlugin, botcmd
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup


class JpWeather(BotPlugin):
    WEATHER_HACK_AREA_URL = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
    WEATHER_HACK_API_URL = 'http://weather.livedoor.com/forecast/webservice/json/v1?'

    def activate(self):
        super(JpWeather, self).activate()
        # TODO: port to method
        cities = {}
        areas = []
        resp = requests.get(self.WEATHER_HACK_AREA_URL)
        soup = BeautifulSoup(resp.content)
        for city_elm in soup.find_all('city'):
            city = {
                'id': city_elm.attrs['id'],
                'name': city_elm.attrs['title'],
                'area': city_elm.parent.attrs['title'],
            }
            cities[city['name']] = city
            if city['area'] not in areas:
                areas.append(city['area'])
        self['cities'] = cities
        self['areas'] = areas

    @botcmd
    def jpweather(self, msg, args):
        """Say weather on specified city of Japan
        """
        result = self.find_weather_hack(args)
        return result

    @botcmd
    def jpweather_city(self, msg, args):
        """Say list of cities abled to report weather
        """
        if args == '':
            cities = [name for name in self['cities'].keys()]
        else:
            cities = [city['name'] for city in self['cities'].values() if city['area'] == args]
        return u'\n'.join(cities)

    @botcmd
    def jpweather_area(self, msg, args):
        # area_name = args.split()[0]
        return u'\n'.join(self['areas'])

    def find_weather_hack(self, city_name):
        city = self['cities'].get(city_name, None)
        if city_name is None:
            return u'{} は確認不可能な地域です'.format(city_name)
        resp = requests.get(self.WEATHER_HACK_API_URL, {'city': city['id']})
        wt_json = resp.json()
        return u'{}: {}は{}'.format(wt_json['title'], wt_json['forecasts'][0]['dateLabel'], wt_json['forecasts'][0]['telop'])
