from bs4 import BeautifulSoup as Bs
import requests
import tldextract
import validators
from pathlib import Path


class Scraper:
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url):
        self._url = new_url

    def get_data_from_website(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            return Bs(r.text, features="html.parser")
        else:
            return None

    def get_text_from_website(self):
        data = self.get_data_from_website()
        if data is not None:
            txt_only = data.get_text()  # najbardziej optymalne i elastyczne rozwiazania jakie znalazlem
            return txt_only
        else:
            return data

    def get_images_urls(self):
        data = self.get_data_from_website()
        if data is not None:
            imgs = data.find_all("img", {"src": True})
            imgs_urls = [link['src'] for link in imgs if link['src'] != ""]
            valid_urls = self.check_image_urls(imgs_urls)
            return valid_urls
        else:
            return data
        
    @staticmethod
    def download_image(img, img_number, download_path):

        file_extension = img.split(".")[-1]
        if len(file_extension) > 5:
            file_extension = "png"
        file_path = Path(f"{download_path}/image_{img_number}.{file_extension}")
        with open(file_path, "wb") as png:
            png.write(requests.get(img, stream=True).content)

        return file_path

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
        url = url.replace(" ", "")
        tmp_url = url  # zdarzylo sie kilka razy
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

        if not validators.url(tmp_url):  # jesli usterka nie zostala usunieta to usuwamy z listy linkow
            tmp_url = "0"

        return tmp_url  # should be valid OR 0
