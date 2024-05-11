from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import secrets

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = secrets.token_urlsafe(16)
csrf = CSRFProtect(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    class PokeForm(FlaskForm):
        name = StringField('Enter a Pokemon', validators=[DataRequired()])
        submit = SubmitField('Search')

    searchForm = PokeForm()

    if(searchForm.validate_on_submit()):
        return redirect(url_for('detail', query=searchForm.name.data))
    
    return render_template('search.html', form=searchForm)

@app.route('/detail/<query>')
def detail(query):
    raw = requests.get(f'https://pokeapi.co/api/v2/pokemon/{query}/')
    if(raw.status_code == 404):
        return redirect(url_for('search'))
    return render_template('detail.html', data=raw.json())

if __name__ == '__main__':
    app.run(debug=True)