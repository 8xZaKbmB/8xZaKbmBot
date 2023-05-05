from flask import Flask, render_template
from threading import Thread
from math import floor
import logging

import subprocess
import sys
from threading import Thread

from flask import Flask

SYNTAX = 'Syntax: python {0} <script>'

flask: Flask = Flask('replit_keep_alive', template_folder="misc/templates")
log:   logging.Logger = logging.getLogger('werkzeug')


@flask.route('/')
def index() -> str:
    html_data = render_template('index.html')
    return html_data


def keep_alive() -> None:
    """ Wraps the web server run() method in a Thread object and starts the web server. """
    def run() -> None:
        log.setLevel(logging.ERROR)
        flask.run(host='0.0.0.0', port=8080)
    thread = Thread(target=run)
    thread.start()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("there was a line of code here but i forgot what it was")
    else:
        keep_alive()
        subprocess.call(['python', sys.argv[1]])
