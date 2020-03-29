from flask import Flask, make_response, jsonify
import validators
from flask import request
from flask.views import MethodView
from file_manager import FileManager

app = Flask(__name__)
downloader = FileManager()


class GettingAll(MethodView):

    @staticmethod
    def get():

        answer = "This app dosen't have a Frontend. In order tu communicate with it you can use REST API " \
                 "through comand line, like 'curl', or by third party programs like free 'Postman'. You can also use " \
                 "simple build-in command line user interface, just run 'user_interface.py' while this app is working."\
                 "\nFor manual REST request you need to specify two fields in json body:" \
                 "\nFirst - 'url': '<url_from_which_you_want_to_download>'" \
                 "\nSecond - 'option': 'all' OR 'text' OR 'images', which tells app what you want to download"
        return make_response(jsonify(answer), 200)

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
        return make_response(jsonify(output), 200)

    def put(self):
        # takie jak post
        return self.post()


app.add_url_rule("/", view_func=GettingAll.as_view("GettingAll"))

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=False)
