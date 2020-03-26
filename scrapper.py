from bs4 import BeautifulSoup as bs
import sys
import requests
import os
import datetime
import tldextract

class Scraper:
    def __init__(self):
        self._data = None
        self._url = None
        self.status_ok = 200
        self.status_error = 400
        self.soup = bs(features="html.parser")

    @property
    def url(self):
        return self._url

    @property
    def data(self):
        return self._data

    @url.setter
    def url(self, new_url):
        self._url = new_url

    @data.setter
    def data(self, new_data):
        self._data = new_data


    def get_text(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            self.data = bs(r.text)
        else:
            return "cosik nie dzialaa"
        txt_only = self.data.get_text()

        print(txt_only)
        return txt_only

    def get_images(self):
        r = requests.get(self.url)
        scrap = bs(features="html.parser")
        data = ""
        if r.status_code == 200:
            self.data = bs(r.text)
        else:
            return "cosik nie dzialaa"
        imgs = self.data.find_all("img")
        imgs_urls = [ link['src'] for link in imgs]
        return 0

    def make_main_dwnld_dir(self):
        if not os.path.exists('soup_downloads'):
            os.mkdir('soup_downloads')

    def make_specific_dwnld_dir(self):
        # naming style: domain_name-date-time

        domain_part = tldextract.extract(self.url).domain
        now = datetime.datetime.now()
        date_time_part = f"{now.year}_{now.month}_{now.day}--{now.hour}_{now.min}"
        dir_name = f"{domain_part}--{date_time_part}"
        if not os.path.exists('soup_downloads/dir_name'):
            os.mkdir('soup_downloads/dir_name')
