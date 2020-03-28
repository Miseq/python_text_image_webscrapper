from flask import Flask, make_response, jsonify, render_template
import validators
from flask import request
from flask.views import MethodView
from file_manager import FileManager

app = Flask(__name__)
downloader = FileManager()

class Getting_all(MethodView):

    @staticmethod
    def get():
        #TODO wywalic albo dac opis korzystania jako odpowiedz
        return render_template("index.html")

    @staticmethod
    def post():
        r = request.get_json()
        downloader.scraper.url = r.get('url')
        if validators.url(downloader.scraper.url):
            download_option = r.get('option')
            if download_option == "all":
                output = downloader.save_to_zip(download_images=True, download_text=True)
            elif download_option == "text":
                output = downloader.save_to_zip(download_text=True)
            elif download_option == "images":
                output = downloader.save_to_zip(download_images=True)
            else:
                output = "Nie podano rodzaju pobiernaia, wpisz jedno: 'option': 'all'/'text'/'images'"
        else:
            output = "URL jest bledny!"
        return make_response(jsonify(output),200)


    def put(self):
        # takie jak post
        return self.post()


app.add_url_rule("/", view_func=Getting_all.as_view("getting_all"))

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=False)
