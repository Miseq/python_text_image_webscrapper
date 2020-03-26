from bs4 import BeautifulSoup as bs
import sys
import requests
import os
import datetime
import tldextract
import clint
import validators

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
        imgs = self.data.find_all("img",{"src":True})
        imgs_urls = [ link['src'] for link in imgs if link['src'] != ""]
        valid_urls = self.check_image_urls(imgs_urls)

        #TODO DO ZIPA i dodac liste urls pobranych

        for i, image in enumerate(valid_urls):
            file_extension = image.split(".")[-1]
            if len(file_extension)>4:
                file_extension = "png"
            with open(f"downloads/image_{i}.{file_extension}", "wb") as png:
                png.write(requests.get(image, stream=True).content)

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

    def check_image_urls(self, images):
        valid_urls = []
        for i, image_url in enumerate(images):
            if not validators.url(image_url):
                image_url = self.repair_invalid_image_url(image_url)
                if image_url == "0":
                    continue
            valid_urls.append(image_url)
        return valid_urls


    def repair_invalid_image_url(self, url):
        # cztery najczestsze napotkane podczas robienia zadania bledy w url
        tmp_url = url
        if url[0:2] == "//":
            tmp_url = f"http:{url}"
        elif url[0] == "/":
            tmp_url = f"http:/{url}"
        elif url[0:8] != "https://" and url[0:7] != "http://":
            tmp_url = f"http://{url}"

        # wystepujace rzadziej: brak domeny przed adresem i brak przekierowania z http:
        if not validators.url(tmp_url):
            ext = tldextract.extract(self.url)
            ext_list = [part for part in ext if part != ""]
            domain = '.'.join(ext_list[:])
            tmp_url = f"http://{domain}{url}"


        if not validators.url(tmp_url): # jesli usterka nie zostala usunieta
            manual_validate = input(f"URL: {tmp_url} seems to be invalid, do you want to manually repair it? Y/N")
            if manual_validate.lower() == "y":
                while not validators.url(tmp_url) or url == "0":
                    tmp_url = input("Enter correct url or type 0 to end and remove it from list").replace(" ","")
            else:
                tmp_url = "0"

        return tmp_url # should be valid OR 0

