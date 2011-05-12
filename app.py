#!/usr/bin/python

import sqlite3
import time

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask("skybot")


app.config.from_pyfile('config.cfg')

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.template_filter('ptime')
def ptime(t):
    return time.strftime('%Y.%m.%d', time.gmtime(int(t)))


@app.route("/")
def index():
    return "Hello World!"


#@app.route("/quotes")
#def list_quotes():
#    quotes = g.db.execute('SELECT * FROM quote WHERE deleted = 0 AND chan = ? '
#                          'order by nick asc, time asc', ('#cobol',)).fetchall()
#
#    chan_name = "#cobol"
#    return render_template('list_quotes.html', quotes=quotes, chan_name=chan_name)

@app.route("/quotes/")
@app.route("/quotes/<chanName>")
def list_quotes(chanName=None):
    if chanName == None:
        chan_name = "#cobol"
    else:
        chan_name = "#" + chanName

    quotes = g.db.execute('SELECT * FROM quote WHERE deleted =0 AND chan= ? '
                          'order by nick asc, time asc', (chan_name,)).fetchall()

    return render_template('list_quotes.html', quotes=quotes, chan_name=chan_name)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
