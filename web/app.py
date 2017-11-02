import os

from time import sleep

from flask import Flask, flash, render_template, request

import webserver_get
from wtforms import Form, TextField, validators
from helpers import timeit

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
#app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('https://www.', validators=[validators.required()])


@app.route("/result", methods=['POST'])
def result():
    urlchecked = request.form['name']

    if request.method == 'POST':
        name = request.form['name']

        name_clean = ''.join([
            c for c in '' + name.replace('https://', '').replace('http://', '').replace('www.', '')
            if c.isalpha()
        ])
        pixel = './static/{}.png'.format('pixel11')
        pol = './static/{}_{}.png'.format(name_clean, 'Political')
        fact = './static/{}_{}.png'.format(name_clean, 'Accuracy')
        other = './static/{}_{}.png'.format(name_clean, 'Character')

    return render_template('index.html', pol=pol, fact=fact, other=other, value=pixel)


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        print("POOP")

        name_clean = ''.join([
            c for c in '' + name.replace('https://', '').replace('http://', '').replace('www.', '')
            if c.isalpha()
        ])

        @timeit
        def run_command():
            print('farts!!!!!!')
            return webserver_get.GetSite(url=name, name_clean=name_clean).run()

        pixel = 'static/{}.png'.format('pixel11')

        result = run_command()
        sleep(.5)
        if not result:
            flash('Not a real website.', 'error')
            oops = './static/oops.gif'
            return render_template('index.html', value=oops, pol=oops, fact=oops, other=oops)
        else:
            pol = './static/{}_{}.png'.format(name_clean, 'Political')
            fact = './static/{}_{}.png'.format(name_clean, 'Accuracy')
            other = './static/{}_{}.png'.format(name_clean, 'Character')
            n_articles, polarity, subjectivity = result
            flash('Analysis based on {} most recent articles.'.format(n_articles), 'error')
            flash('positivity {}:'.format(polarity), 'error')
            flash('subjectivity {}:'.format(subjectivity), 'error')

        sleep(.5)
        return render_template('index.html', pol=pol, fact=fact, other=other, value=pixel, positiviy=polarity, subjectivity=subjectivity, url_name=name)
        # return render_template(url_for('result', results_form=form))

        # Save the comment here.

    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=False, threaded=True)
