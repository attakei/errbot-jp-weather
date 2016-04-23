# -*- coding:utf8 -*-
from __future__ import print_function, absolute_import, unicode_literals
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

    @botcmd
    def jpweather_city(self, msg, args):
        if args == '':
            cities = self.fetch_cities()
        else:
            cities = self.fetch_cities_from_area(args)
        return u'\n'.join(['* {}'.format(city) for city in cities.keys()])

    @botcmd
    def jpweather_area(self, msg, args):
        # area_name = args.split()[0]
        areas = self.fetch_areas()
        return u'\n'.join(['* {}'.format(area) for area in areas])

    def find_city_id(self, city_name):
        cities = self.fetch_cities()
        return cities.get(city_name, None)

    def find_weather_hack(self, city_name):
        city_id = self.find_city_id(city_name)
        if city_id is None:
            return u'{} は確認不可能な地域です'.format(city_name)
        resp = requests.get(self.WEATHER_HACK_API_URL, {'city':city_id})
        wt_json = resp.json()
        return u'{}: {}は{}'.format(wt_json['title'], wt_json['forecasts'][0]['dateLabel'], wt_json['forecasts'][0]['telop'])

    def fetch_cities(self):
        resp = requests.get(self.WEATHER_HACK_AREA_URL)
        tree = ElementTree.fromstring(resp.content)
        return {elm.attrib['title']: elm.attrib['id'] for elm in tree.findall('.//city')}

    def fetch_areas(self):
        resp = requests.get(self.WEATHER_HACK_AREA_URL)
        tree = ElementTree.fromstring(resp.content)
        return [elm.attrib['title'] for elm in tree.findall('.//pref')]

    def fetch_cities_from_area(self, area):
        resp = requests.get(self.WEATHER_HACK_AREA_URL)
        tree = ElementTree.fromstring(resp.content)
        return {elm.attrib['title']: elm.attrib['id'] for elm in tree.findall('./pref[title="' + area + '"]/city')}
