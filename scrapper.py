from bs4 import BeautifulSoup as bs
import sys
import requests

def get_source(url):
    r = requests.get(url)
    if r.status_code == 200:
        return bs(r.text)
    else:
        print("Cosik nie dziala")
