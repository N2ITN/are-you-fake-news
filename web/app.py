"""
This module is the entry point for Flask. It handles the webpage templates and routing,
and triggers the webserver_get.py module to process new sites.
"""

import json
import os
import subprocess
from time import ctime, sleep

import tldextract
import boto3
import requests
from flask import Flask, flash, render_template, request
from numpy.random import randint

import webserver_get
from helpers import timeit
from wtforms import Form, TextField, validators

s3 = boto3.resource('s3')
bucket = s3.Bucket('fakenewsimg')

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CACHE_TYPE'] = 'null'

app.config['SECRET_KEY'] = randint(0, 10000000)
blacklist = ['mediabiasfactcheckcom']


class ReusableForm(Form):
    name = TextField('https://www.', validators=[validators.required()])


@app.route('/resume', methods=['GET', 'POST'])
def res():
    return render_template('resume.html')


@app.route('/heatmap', methods=['GET', 'POST'])
def heatmap():
    import make_map
    make_map.run()
    return render_template('mymap.html')


@app.route('/data', methods=['GET', 'POST'])
def show_ip_table():
    import pandas_table
    pandas_table.run()
    return render_template('data.html')


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']

        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        subprocess.call(['python3', 'mongo_ip.py', ip, name])

        name = name.replace('https://', '').replace('http://', '').replace('www.', '').lower()
        name_clean = ''.join(tldextract.extract(name))

        if name_clean in blacklist:
            oops = './static/img/icons/loading.gif'
            flash('''
                Sorry, that request didn't work - no results to display. ''', 'error')
            flash('''
                You'll have to rely your own excellent judgement for now. ''', 'error')
            flash('''Good luck!''', 'error')
            return render_template(
                'index.html', value=oops, pol=oops, fact=oops, other=oops, url_name=name)

        @timeit
        def run_command():
            return webserver_get.GetSite(url=name, name_clean=name_clean).run()

        pixel = 'static/{}.png'.format('pixel11')
        ''' DEBUG !!!
        try:

            result = run_command()
        except Exception as e:
            print(e)
            result = None
        DEBUG !!! '''
        result = run_command()
        oops = './static/img/icons/loading.gif'
        if not result or result == 'ConnectionError':

            flash('''
                Sorry, that request didn't work - no results to display. ''', 'error')
            flash('''
                You'll have to rely your own excellent judgement for now. ''', 'error')
            flash('''Good luck!''', 'error')
            return render_template(
                'index.html', value=oops, pol=oops, fact=oops, other=oops, url_name=name)
        else:
            n_articles, name_clean = result
            pol = '{}_{}.png'.format(name_clean, 'Political')
            fact = '{}_{}.png'.format(name_clean, 'Accuracy')
            other = '{}_{}.png'.format(name_clean, 'Character')
            static = './static/'
            try:
                [bucket.download_file(_, static + _) for _ in [pol, fact, other]]
            except Exception as e:
                print(e)
                from mongo_query_results import del_TLD
                del_TLD(name_clean)

            flash('Analysis based on {} most recent articles.'.format(n_articles), 'error')

        return render_template(
            'index.html',
            pol=static + pol,
            fact=static + fact,
            other=static + other,
            value=pixel,
            positiviy='',
            subjectivity='',
            url_name=name,
        )

    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
