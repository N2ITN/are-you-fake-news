from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
import subprocess
import sys
from cosine_finder import *
import io
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
import shlex


class ReusableForm(Form):
    name = TextField('https://www.', validators=[validators.required()])


from time import sleep
import json


@app.route("/results", methods=['GET,POST'])
def view_results():
    pass


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        print(name)

        if form.validate():

            def run_command(name):

                return get(name)

            im_name = ''.join([
                c for c in '' + name.replace('https://', '').replace('http://', '').replace('www.', '')
                if c.isalpha()
            ])

            value = 'static/{}.png'.format(im_name)

            print(value)
            if not os.path.exists(value):
                try:
                    f = run_command(name)
            #         json.dump(f, open(value[:-4] + '.json', 'w'))
            #         for _ in f:

            #             flash(_)
                finally:

                    del form
            else:
                pass
                # for _ in json.load(open(value[:-4] + '.json')):
            # flash(_)
            return render_template('index.html', value=value)
            # Save the comment here.

        else:
            flash('All the form fields are required. ')

    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
