""" 
This module is the entry point for Flask. It handles the webpage templates and routing,
and triggers the webserver_get.py module to process new sites.
"""

import json
import os
import subprocess
from time import ctime, sleep
import subprocess
import requests
from flask import Flask, flash, render_template, request
from numpy.random import randint
from wtforms import Form, TextField, validators

import webserver_get
from helpers import timeit

app = Flask(__name__)
app.config.from_object(__name__)
app.config["CACHE_TYPE"] = "null"

app.config['SECRET_KEY'] = randint(0, 10000000)


class ReusableForm(Form):
    name = TextField('https://www.', validators=[validators.required()])


@app.route("/resume", methods=['GET', 'POST'])
def res():
    return render_template('resume.html')


@app.route("/heatmap", methods=['GET', 'POST'])
def heatmap():
    import make_map
    make_map.run()
    return render_template('mymap.html')


@app.route("/data", methods=['GET', 'POST'])
def show_ip_table():
    import pandas_table
    pandas_table.run()
    return render_template('data.html')


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']

        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        subprocess.call(['python3', 'mongo_ip.py', ip, name])

        name = name.replace('https://', '').replace('http://', '').replace('www.', '').lower()
        name_clean = ''.join([c for c in name if c.isalpha()])

        @timeit
        def run_command():
            return webserver_get.GetSite(url=name, name_clean=name_clean).run()

        pixel = 'static/{}.png'.format('pixel11')

        # try:
        result = run_command()
        # except Exception as e:
        #     print(e)
        #     print(e.__traceback__.tb_lineno.real)
        #     result = False

        oops = './static/img/icons/loading.gif'
        if not result or result == 'ConnectionError':

            flash(''' 
                Sorry, that request didn't work - no results to display. ''', 'error')
            flash(''' 
                You'll have to rely your own excellent judgement for now. ''', 'error')
            flash('''Good luck!''', 'error')
            return render_template('index.html', value=oops, pol=oops, fact=oops, other=oops)
        else:
            n_articles, polarity, subjectivity, word_count, hashed = result
            pol = './static/{}_{}.png'.format(hashed, 'Political')
            fact = './static/{}_{}.png'.format(hashed, 'Accuracy')
            other = './static/{}_{}.png'.format(hashed, 'Character')

            if word_count > 1000:
                word_count = str(word_count)[:-3] + ' thousand'
            flash('Analysis based on {} most recent articles.'.format(n_articles), 'error')
            # flash('positivity {}:'.format(polarity), 'error')
            # flash('subjectivity {}:'.format(subjectivity), 'error')

        return render_template(
            'index.html',
            pol=pol,
            fact=fact,
            other=other,
            value=pixel,
            positiviy=polarity,
            subjectivity=subjectivity,
            url_name=name)

    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
