from flask import Flask, make_response, jsonify
import requests
import sys
from bs4 import BeautifulSoup as bs
from scrapper import get_source
from flask.views import MethodView

app = Flask(__name__)

class Getting_all(MethodView):

    @staticmethod
    def get():
        return 'Hello mordo'

    @staticmethod
    def put():
        print(get_source('https://text.npr.org'))



app.add_url_rule("/", view_func=Getting_all.as_view("getting_all"))

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=False)
