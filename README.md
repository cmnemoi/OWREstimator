# TAS Predictor : Project Overview
An app allowing you to predict the best possible time for a game speedrun. 

* Created a web app that estimates the best possible time of a speedrun (MAE ~ 388 seconds).
* Extracted 3800+ game runs from [Speedrun.com](https://speedrun.com) using its [API](https://github.com/speedruncomorg/api) and Python.
* Scrapped 2000+ game runs from [TASvideos](http://tasvideos.org) using Beautiful Soup and Python.
* Engineering features from the time of the world records, number of runners and released year for each game put on Python, Libre Office Calc/Excel and Streamlit.
* Optimized linear, lasso, ridge, random forest, gradient boost regressor using GridSearchCV to find the best model.
* Built a web app using Streamlit.

# Run it locally
 * Download the project and extract it
 * Run Python 3.9 on a terminal
 * Navigate into the folder you extracted
 * Install the requirements : `pip install -r requirements.txt`
 * Then : `streamlit run src/app/main.py`

# Code and ressources used
**Python version 3.9**
 
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, beautiful soup, flask, streamlit, joblib
 
**Libraries** : [Python library for speedrun.com API](https://github.com/blha303/srcomapi)
 
**Scraper Repository:** https://github.com/kaparker/tutorials/blob/master/pythonscraper/websitescrapefasttrack.py
 
**Scraper Article:** https://blog.lesjeudis.com/web-scraping-avec-python (french)
 
**Flask Productionization:** https://www.analyticsvidhya.com/blog/2020/04/how-to-deploy-machine-learning-model-flask/

# Data collection
## Web scrapping 
Tweaked the web scrapper above to scrape 2000+ games from tasvideos.org. With each game the following :
 * Time of the best TAS
 * Emulator the TAS has been made with
## Speedrun.com API
Used the python library to use speedrun.com API (above) and extract 3800+ runs with the following :
 * game name
 * category
 * platform
 * engine the game has been made with
 * developpers
 * publishers
 * released year
 * number of runners for each game

# Data cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:
 * put the game and category in the same column
 * calculate the age of game from released year
 * removed runs with WR better than collected TAS time
 * created a variable to control outliers : time_difference
   * removed outliers for runs with time_difference > 20
 * added columns coding age and number of runners for each game to categorical variables

# EDA
It revealed that number of runners were a key feature to predict the best possible time.

# Model building
First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 30% (studies shows the best repartition is somewhere near that).
 
I tried different models :
 * Simple linear regression 
 * Multiple linear regression
 * Multiple linear regression with significative feautres (p-values < 0.2 on linear regressions)
 * Lasso Regression
 * Ridge Regression
 * Random Forest Regressor
 * Gradient Boost Regressor

# Model performance
The best model was the Gradient Boost Regressor with a MAE of ~388 seconds on test set.

# Productionization
In this step, I built a flask API web app prototype using the relevant link in reference on a local webserver. The prototype allows the user to type the name of the game, choose the category and returns the link of the world record, its time and the estimated best time.
 
I decided to do the actual app using Streamlit.
![app prototype](https://cdn.discordapp.com/attachments/386686003148226561/859109203310018560/Screenshot_2021-06-28_at_18-32-54_main_Streamlit.png "App prototype")
 
The online version is coming soon.

