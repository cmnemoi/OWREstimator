from joblib import load
import pandas as pd
from sklearn.base import BaseEstimator
import srcomapi, srcomapi.datatypes as dt
import datetime
from flask import Flask, render_template, request, redirect, url_for


class CustomEncoder(BaseEstimator):

    def __init__(self):
        pass

    def fit(self, documents, y=None):
        return self

    def transform(self, x_dataset):
        #nb_of_runs
        x_dataset['Unpopular'] = x_dataset['nb_of_runs'].apply(lambda x: 1 if x<=3 else 0)
        x_dataset['Somehow_Popular'] = x_dataset['nb_of_runs'].apply(lambda x: 1 if x>3 and x<=7 else 0)
        x_dataset['Popular'] = x_dataset['nb_of_runs'].apply(lambda x: 1 if x>7 and x<=19 else 0)
        x_dataset['Very_Popular'] = x_dataset['nb_of_runs'].apply(lambda x: 1 if x>19 else 0)

        #age
        x_dataset['Young'] = x_dataset['age'].apply(lambda x: 1 if x<=21 else 0)
        x_dataset['Somehow_Old'] = x_dataset['age'].apply(lambda x: 1 if x>21 and x<=28 else 0)
        x_dataset['Old'] = x_dataset['age'].apply(lambda x: 1 if x>28 and x<=31 else 0)
        x_dataset['Very_Old'] = x_dataset['age'].apply(lambda x: 1 if x>31 else 0)

        #coding time to a categorical variable
        x_dataset['Short'] = x_dataset['time'].apply(lambda x: 1 if x<=664.833 else 0)
        x_dataset['Somehow_Long'] = x_dataset['time'].apply(lambda x: 1 if x>664.833 and x<=1226 else 0)
        x_dataset['Long'] = x_dataset['time'].apply(lambda x: 1 if x>1226 and x<=2315 else 0)
        x_dataset['Very_Long'] = x_dataset['time'].apply(lambda x: 1 if x>2315 else 0)
            
        return x_dataset

def requestCategories(name,api):
    src_game = api.search(srcomapi.datatypes.Game, {"name": name})[0]

    leaderboards = {}
    for category in src_game.categories:
        if category.type == 'per-level':
            pass
        #   for level in src_game.levels:
        #     leaderboards[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}/{}?embed=variables".format(src_game.id, category.id,level.id)))
        else:
            leaderboards[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(src_game.id, category.id)))

    categories_names = []
    for lb in leaderboards:
        categories_names.append(lb)

    return categories_names

def request_data(game,user_category,api):
    result = {}
    src_game = api.search(srcomapi.datatypes.Game, {"name": game})[0]

    leaderboards = {}
    for category in src_game.categories:
        if category.type == 'per-level':
            pass
        else:
            leaderboards[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(src_game.id, category.id)))

    #prediction
    pipeline = load('src/time_prediction.joblib')
    nb_of_runs = len(leaderboards[user_category].runs)
    age = datetime.datetime.now().year - src_game.released
    WR_time = leaderboards[user_category].runs[0]["run"].times['primary_t']
    df = pd.DataFrame({'time':WR_time,'age':age,'nb_of_runs':nb_of_runs,}, index=[0])

    predicted_time = str(datetime.timedelta(seconds=pipeline.predict(df)[0]))
    WR_link = leaderboards[user_category].runs[0]["run"].weblink
    WR_time = str(datetime.timedelta(seconds=leaderboards[user_category].runs[0]["run"].times['primary_t']))

    result['predicted_time'] = predicted_time
    result['WR_link'] = WR_link
    result['WR_time'] = WR_time
    
    return result

# start flask
app = Flask(__name__)

# render default webpage
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        user = request.form.get('search')
        return redirect(url_for('categories', game=user))
    else:
        return render_template('home.html')

# # when the user types its game, redirect to the page for selecting categories
# @app.route('/', methods=['POST', 'GET'])
# def get_categories():
#     if request.method == 'POST':
#         user = request.form['search']
#         return redirect(url_for('categories', game=user))

# get the data for the requested query
@app.route('/categories/<game>', methods=['POST', 'GET'])
def categories(game):
    if request.method == 'POST':
        user = request.form['category']
        return redirect(url_for('results', game=game, category=user))
    else:
        return render_template('category.html', game=game, categories=requestCategories(game,api))

# @app.route('/categories/<game>', methods=['POST', 'GET'])
# def get_results():
#     if request.method == 'POST':
#         user = request.form['category']
#         return redirect(url_for('results', category=user))

@app.route('/result/<game>/<category>')
def results(game,category):
    data = request_data(game,category,api)
    return render_template('result.html',categories=requestCategories(game,api),WR_link=data['WR_link'],
    WR_time=data['WR_time'],predicted_time=data['predicted_time'])

api = srcomapi.SpeedrunCom(); api.debug = 1

app.run(debug=True)

