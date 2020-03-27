from bs4 import BeautifulSoup as bs
import requests
import os
import datetime
import tldextract
import validators
from zipfile import ZipFile

class Scraper:
    def __init__(self):
        self._url = None
        self.status_ok = 200
        self.status_error = 400
        self.soup = bs(features="html.parser")

    @property
    def url(self):
        return self._url


    @url.setter
    def url(self, new_url):
        self._url = new_url


    def get_text_from_website(self):
        # TODO sprawdzic czy przez pobranie tylko <p> bd lepiej albo inaczej niz .text
        r = requests.get(self.url)
        if r.status_code == 200:
            data = bs(r.text)
        else:
            return "cosik nie dzialaa"
        txt_only = data.get_text()
        return txt_only

    def get_images_urls(self):

        r = requests.get(self.url)
        scrap = bs(features="html.parser")
        if r.status_code == 200:
            data = bs(r.text)
        else:
            return "cosik nie dzialaa"
        imgs = data.find_all("img",{"src":True})
        imgs_urls = [ link['src'] for link in imgs if link['src'] != ""]
        valid_urls = self.check_image_urls(imgs_urls)

        return valid_urls

    def make_zip_file_name(self, images=None, text=None):

        domain = tldextract.extract(self.url).domain
        now = datetime.datetime.now()
        date_time_part = f"{now.year}_{now.month}_{now.day}--{now.hour}"
        file_name = f"{domain}--{date_time_part}"
        if images == True:
            file_name = f"{file_name}_images"
        if text == True:
            file_name = f"{file_name}_text"
        file_name = f"{file_name}.zip"
        return file_name

    def download_image(self, img, img_number):

        file_extension = img.split(".")[-1]
        if len(file_extension) > 5:
            file_extension = "png"
        file_path = f"downloaded/images/image_{img_number}.{file_extension}"
        with open(file_path, "wb") as png:
            png.write(requests.get(img, stream=True).content)

        return file_path

    def save_to_zip(self, download_images=False, download_text=False):
        #TODO dodac pliki txt opisujace skad pobrane, i inne info
        text, img_urls = None, None
        if download_text:
            text = self.get_text_from_website()
        if download_images:
            img_urls = self.get_images_urls()
        file_name = self.make_zip_file_name(download_images, download_text)
        self.make_tmp_dwnld_dir()  # jesli nie istnieje to tworzy tymczasowy folder pobierania

        with ZipFile(file_name,"w") as zip_file:
            # pobranie obrazow
            if img_urls != None:
                os.mkdir(f'downloaded/images')
                for i, image in enumerate(img_urls):
                    image_path = self.download_image(image,i)
                    zip_file.write(image_path)
                    os.remove(image_path)

            # pobranie text
            if text != None:
                text_file_path = "downloaded/text.txt"
                with open(text_file_path, "w", encoding="utf-8") as file:
                    file.write(text)
                zip_file.write(text_file_path)
                os.remove(text_file_path)

        os.rmdir('downloaded/images')
        os.rmdir('downloaded')

    def make_tmp_dwnld_dir(self):
        if not os.path.exists('downloaded'):
            os.mkdir('downloaded')

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
        url = url.replace(" ","")
        tmp_url = url # zdarzylo sie kilka razy
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
            manual_validate = input(f"URL for image: {tmp_url} seems to be invalid. \n"
                                    f"Do you want to manually repair it? Y/N")
            if manual_validate.lower() == "y":
                while not validators.url(tmp_url) or url == "0":
                    tmp_url = input("Enter correct url or type 0 to end and remove it from list").replace(" ","")
            else:
                tmp_url = "0"

        return tmp_url # should be valid OR 0

    def make_specific_dwnld_dir(self):
        # naming style: domain_name-date-time
        # TODO do wywalenia?
        domain_part = tldextract.extract(self.url).domain
        now = datetime.datetime.now()
        date_time_part = f"{now.year}_{now.month}_{now.day}--{now.hour}_{now.min}"
        dir_name = f"{domain_part}--{date_time_part}"
        if not os.path.exists('downloaded/dir_name'):
            os.mkdir('downloaded/dir_name')