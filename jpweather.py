# -*- coding:utf8 -*-
from __future__ import division, print_function, absolute_import
from errbot import BotPlugin, botcmd
import requests
from xml.etree import ElementTree


class JpWeather(BotPlugin):
    WEATHER_HACK_AREA_URL = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
    WEATHER_HACK_API_URL = 'http://weather.livedoor.com/forecast/webservice/json/v1?'

    @botcmd
    def jpweather(self, msg, args):
        result = self.find_weather_hack(args)
        return result

    def find_city_id(self, city_name):
        resp = requests.get(self.WEATHER_HACK_AREA_URL)
        tree = ElementTree.fromstring(resp.content)
        cities = {elm.attrib['title']: elm.attrib['id'] for elm in tree.findall('.//city')}
        return cities.get(city_name, None)

    def find_weather_hack(self, city_name):
        city_id = self.find_city_id(city_name)
        if city_id is None:
            return u'{} は確認不可能な地域です'.format(city_name)
        resp = requests.get(self.WEATHER_HACK_API_URL, {'city':city_id})
        wt_json = resp.json()
        return u'{}: {}は{}'.format(wt_json['title'], wt_json['forecasts'][0]['dateLabel'], wt_json['forecasts'][0]['telop'])
