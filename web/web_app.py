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
app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('https://www.', validators=[validators.required()])


@app.route("/results", methods=['GET,POST'])
def view_results():
    pass


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        print(name)

        if form.validate():

            name_clean = ''.join([
                c for c in '' + name.replace('https://', '').replace('http://', '').replace('www.', '')
                if c.isalpha()
            ])

            @timeit
            def run_command():

                return webserver_get.GetSite(url=name, name_clean=name_clean).run()

            value = 'fakevalue'
            pixel = 'static/{}.png'.format('pixel11')
            if not os.path.exists(value):
                try:
                    result = run_command()
                    if not result:
                        flash('Not a real website.', 'error')
                        oops = './static/oops.gif'
                        return render_template(
                            'index.html', value=oops, pol=pixel, fact=pixel, other=pixel)
                    else:
                        pol = './static/{}_{}.png'.format(name_clean, 'Political')
                        fact = './static/{}_{}.png'.format(name_clean, 'Accuracy')
                        other = './static/{}_{}.png'.format(name_clean, 'Character')
                        n_articles, polarity, subjectivity = result
                        flash('Analysis based on {} most recent articles.'.format(n_articles), 'error')
                        flash('positivity {}:'.format(polarity), 'error')
                        flash('subjectivity {}:'.format(subjectivity), 'error')
                finally:

                    del form
            else:
                pass
            sleep(.1)
            return render_template('index.html', pol=pol, fact=fact, other=other, value=pixel)
            # Save the comment here.

        else:
            flash('All the form fields are required. ')

    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=False, threaded=True)
