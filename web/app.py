import os

from time import sleep, ctime

from flask import Flask, flash, render_template, request

import webserver_get
from wtforms import Form, TextField, validators
from helpers import timeit
import mongo_ip

# App config.

app = Flask(__name__)
app.config.from_object(__name__)
app.config["CACHE_TYPE"] = "null"

from numpy.random import randint
app.config['SECRET_KEY'] = randint(0, 10000000)


class ReusableForm(Form):
    name = TextField('https://www.', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']

        ip_log = {'ip': request.remote_addr, 'time': ctime(), 'request': name}
        mongo_ip.insert('ip_logs', ip_log)

        name = name.replace('https://', '').replace('http://', '').replace('www.', '').lower()
        name_clean = ''.join([c for c in name if c.isalpha()])

        @timeit
        def run_command():
            return webserver_get.GetSite(url=name, name_clean=name_clean).run()

        pixel = 'static/{}.png'.format('pixel11')

        result = run_command()
        sleep(.5)
        oops = './static/img/icons/loading.gif'
        if not result or result == 'ConnectionError':

            flash(''' 
                Sorry, that request didn't work - no results to display. ''', 'error')
            flash(''' 
                You'll have to rely your own excellent judgement for now. ''', 'error')
            flash('''Good luck!''', 'error')
            return render_template('index.html', value=oops, pol=oops, fact=oops, other=oops)
        else:
            pol = './static/{}_{}.png'.format(name_clean, 'Political')
            fact = './static/{}_{}.png'.format(name_clean, 'Accuracy')
            other = './static/{}_{}.png'.format(name_clean, 'Character')

            n_articles, polarity, subjectivity, word_count = result

            if word_count > 1000:
                word_count = str(word_count)[:-3] + ' thousand'
            flash('Analysis based on {} words from {} most recent articles.'.format(
                word_count, n_articles), 'error')
            flash('positivity {}:'.format(polarity), 'error')
            flash('subjectivity {}:'.format(subjectivity), 'error')

        sleep(.5)
        return render_template(
            'index.html',
            pol=pol,
            fact=fact,
            other=other,
            value=pixel,
            positiviy=polarity,
            subjectivity=subjectivity,
            url_name=name)
        # return render_template(url_for('result', results_form=form))

        # Save the comment here.

    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=False, threaded=True)
