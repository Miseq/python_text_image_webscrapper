from unittest import TestCase
from file_manager import FileManager
from datetime import datetime
import tldextract
import pathlib
import os


class TestFileManager(TestCase):

    def test_make_zip_file_name(self):
        test_url = "https://semantive.com/pl/"
        test_manager = FileManager(test_url)
        now = datetime.now()
        domain = tldextract.extract(test_url).domain
        correct_form = f"{domain}--{now.year}_{now.month}_{now.day}--{now.hour}_{now.minute}"
        self.assertEqual(test_manager.make_zip_file_name(images=True, text=True), f"{correct_form}--images_text.zip")
        self.assertEqual(test_manager.make_zip_file_name(images=True, text=False), f"{correct_form}--images.zip")
        self.assertEqual(test_manager.make_zip_file_name(images=False, text=True), f"{correct_form}--_text.zip")

    def test_create_logs(self):
        test_manager = FileManager("")
        test_manager.create_logs("test", True, ["test"])
        self.assertTrue(pathlib.Path("logs.txt").exists())
        os.remove("logs.txt")

    def test_save_to_zip(self):
        test_url = "https://www.google.pl"  # szybsze
        test_manager = FileManager(test_url)
        now = datetime.now()
        domain = tldextract.extract(test_url).domain
        file_path = f"{domain}--{now.year}_{now.month}_{now.day}--{now.hour}_{now.minute}--images_text.zip"
        test_manager.save_to_zip(download_text=True, download_images=True)
        self.assertTrue(os.path.exists(file_path))
        os.remove("logs.txt")
        os.remove(file_path)

    def test_create_dir_if_dosent_exist(self):
        test_manager = FileManager("")
        test_manager.create_dir_if_dosent_exist(test_manager.tmp_download_dir)
        self.assertTrue(os.path.exists(test_manager.tmp_download_dir))
        os.rmdir(test_manager.tmp_download_dir)

    def test_cleanup(self):
        test_url = "https://www.google.pl"  # szybsze
        test_manager = FileManager(test_url)
        test_manager.save_to_zip(download_text=True, download_images=True)
        now = datetime.now()
        domain = tldextract.extract(test_url).domain
        file_path = f"{domain}--{now.year}_{now.month}_{now.day}--{now.hour}_{now.minute}--images_text.zip"
        self.assertTrue(not os.path.exists(test_manager.tmp_download_dir))
        os.remove("logs.txt")
        os.remove(file_path)
