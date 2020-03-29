from unittest import TestCase
from scrapper import Scraper
import os
from pathlib import Path


class TestScraper(TestCase):

    def test_get_data_from_website(self):
        test_url = "https://semantive.com/pl/"
        test_scraper = Scraper(test_url)
        self.assertIsNotNone(test_scraper.get_data_from_website())

    def test_get_text_from_website(self):
        test_url = "https://semantive.com/pl/"
        test_scraper = Scraper(test_url)
        text = test_scraper.get_text_from_website()
        self.assertTrue(isinstance(text, str))

    def test_get_images_urls(self):
        test_url = "https://semantive.com/pl/"
        test_scraper = Scraper(test_url)
        img_urls_list = test_scraper.get_images_urls()
        self.assertTrue(isinstance(img_urls_list, list))
        self.assertTrue(len(img_urls_list) > 0)

    def test_download_image(self):
        test_url = "https://semantive.com/pl/"
        test_scraper = Scraper(test_url)
        test_image_urls = test_scraper.get_images_urls()
        file_path = test_scraper.download_image(test_image_urls[0],0, Path(""))
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

    def test_repair_invalid_image_url(self):
        correct_url = "http://semantive.com/pl/" # dodaje zawsze http ktore jest pewniejsze - przekierowanie
        test_url_repr = "semantive.com/pl/"
        test_url_repr_2 = " http://semantive.com/pl/"  # spacja na poczatku
        test_url_unrepr = "httwww://semantive.com/pl/" # powinien zwrocic "0"
        url_dict = {test_url_repr: correct_url, test_url_repr_2: correct_url, test_url_unrepr: "0"}
        for item in url_dict:
            test_scraper = Scraper("")
            output = test_scraper.repair_invalid_image_url(item)
            self.assertEqual(output, url_dict[item])