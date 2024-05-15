from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import secrets
import random

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

def random_pokemon_team():
    team = []
    while len(team) < 6:
        poke_id = random.randint(1, 898)  # Assuming there are 898 Pokémon
        if poke_id not in team:
            team.append(poke_id)
    return team

@app.route('/random_team')
def random_team():
    try:
        team = random_pokemon_team()
        sprites = []
        for poke_id in team:
            raw = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}/')
            raw.raise_for_status()
            data = raw.json()
            sprites.append(data['sprites']['front_default'])
        pokemon_data = [{'id': poke_id, 'sprite': sprite} for poke_id, sprite in zip(team, sprites)]
    except requests.exceptions.RequestException as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('home'))

    return render_template('random_team.html', pokemon_data=pokemon_data)

if __name__ == '__main__':
    app.run(debug=True)