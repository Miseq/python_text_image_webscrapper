from flask import Flask, make_response, jsonify, render_template
import requests
import sys
from flask import request
from scrapper import Scraper
from flask.views import MethodView

app = Flask(__name__)
scraper = Scraper()

class Getting_all(MethodView):

    @staticmethod
    def get():
        return render_template("index.html")

    @staticmethod
    def post():
        r = request.get_json()
        scraper.url = r.get('url')
        output = scraper.get_images()

        return make_response(jsonify(output),200)



app.add_url_rule("/", view_func=Getting_all.as_view("getting_all"))

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=False)
