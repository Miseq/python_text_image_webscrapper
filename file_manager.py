import os
import datetime
import tldextract
from zipfile import ZipFile
from scrapper import Scraper
from pathlib import Path


class FileManager():
    def __init__(self, url=None):
        self.scraper = Scraper(url)
        self.main_download_dir = Path()
        self.tmp_download_dir = Path(f'{self.main_download_dir}/downloaded')
        self.tmp_imgs_download_dir = Path(f'{self.tmp_download_dir}/images')

    def make_zip_file_name(self, images=False, text=False):
        # file name schema:   domain--date--hour--minute--images(AND/OR)_text.zip
        domain = tldextract.extract(self.scraper.url).domain
        now = datetime.datetime.now()
        date_time_part = f"{now.year}_{now.month}_{now.day}--{now.hour}_{now.minute}--"
        file_name = f"{domain}--{date_time_part}"
        if images == True:
            file_name = f"{file_name}images"
        if text == True:
            file_name = f"{file_name}_text"
        file_name = f"{file_name}.zip"
        return file_name

    def create_logs(self,zip_file_name=None, text=False, imgs_urls= None):
        if imgs_urls == None: # zmieniam tutaj, gdyz nie powinno sie dawa mutowalnych wartosci jako domyslnych arg
            imgs_urls = []
        template_txt = f"{datetime.datetime.now().date()}--Downloaded: " \
                       f"{zip_file_name} in directory: {self.tmp_download_dir}"\
                       f"Text:{text} Number of images: {len(imgs_urls)} \n"
        with open("logs.txt", "w", encoding="utf-8") as file:
            file.write(template_txt)

    def save_to_zip(self, download_images=False, download_text=False):
        self.cleanup() # gdyby zostaly foldery tmp po poprzednim
        text, img_urls = None, None
        if download_text:
            text = self.scraper.get_text_from_website()
        if download_images:
            img_urls = self.scraper.get_images_urls()
        zip_file_name = self.make_zip_file_name(download_images, download_text)
        self.make_tmp_dwnld_dir()  # jesli nie istnieje to tworzy tymczasowy folder pobierania

        with ZipFile(zip_file_name,"w") as zip_file:
            # pobranie obrazow
            if img_urls != None:
                os.mkdir(self.tmp_imgs_download_dir)
                for i, image in enumerate(img_urls):
                    image_path = self.scraper.download_image(image,i, self.tmp_imgs_download_dir)
                    zip_file.write(image_path)
                    os.remove(image_path)

            # pobranie text
            if text != None:
                text_file_path = f"{self.tmp_download_dir}/text.txt"
                with open(text_file_path, "w", encoding="utf-8") as file:
                    file.write(text)
                zip_file.write(text_file_path)
                os.remove(text_file_path)

        self.create_logs(zip_file_name,text,img_urls)
        self.cleanup()
        return f"Items saved in zip_file: {zip_file_name} in dir: {self.tmp_download_dir}"

    def make_tmp_dwnld_dir(self):
        if not os.path.exists(self.tmp_download_dir):
            os.mkdir(self.tmp_download_dir)

    def cleanup(self):
        try:
            if os.path.exists(self.tmp_imgs_download_dir):
                os.rmdir(self.tmp_imgs_download_dir)
            if os.path.exists(self.tmp_download_dir):
                os.rmdir(self.tmp_download_dir)
        except:
            print("Error occured while removing temporary download paths")

    def change_download_path(self):
        #TODO
        pass