'''Soren DeHaan and Carl Tankersley
   11/15/2021
   CS 257 - Software Design'''

import flask
import json
import psycopg2
import argparse
import api

app = flask.Flask(__name__, static_folder='static',
                  template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "host", type=str, help="host on which to run the service")
    parser.add_argument(
        "port", type=int, help="port on which the service is listening")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    app.run(host=args.host, port=args.port, debug=True)


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/about.html')
def about():
    return flask.render_template('about.html')


@app.route('/careers.html')
def careers():
    return flask.render_template('careers.html')


@app.route('/create.html')
def create():
    return flask.render_template('create.html')


@app.route('/index.html')
def index():
    return flask.render_template('index.html')


@app.route('/video.html')
def video():
    return flask.render_template('video.html')


@app.route('/watch.html')
def watch():
    return flask.render_template('watch.html')


@app.route('/favicon.ico')
def favicon():
    return flask.send_file('static/favicon.ico')


if __name__ == '__main__':
    main()
