from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

class ReusableForm(Form):
    handle = TextField('Handle', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        handle = request.form['handle']
        print(handle)

    if form.validate():
        # Save the comment here.
        flash(handle)
    else:
        flash('ADSA_EOH_2019 ')

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()
