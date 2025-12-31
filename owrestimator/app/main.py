import os
import sys

import streamlit as st
from back import predict_tas_time

from owrestimator.app.speedrun_com_gateway import get_game_categories

st.title("TAS Predictor")
st.header("Predict the best possible times of your favorite speedgame.")
st.write("""Your speedgame don't have TASes ? Do you want to know how fast this goofy extension category can be ?
 
This machine learning-driven app will give you answers.""")

game_form = st.form("game_form")
game = game_form.text_input("Type a game :")
game_submitted = game_form.form_submit_button("Get best possible times !")
if game_submitted:
    try:
        categories = get_game_categories(game)
    except IndexError:
        st.error("Your game has not been found. Try to look for typos.")
        sys.exit("Your game has not been found. Try to look for typos.")
    for category in categories:
        try:
            world_record_predicton = predict_tas_time(game, category)
            st.subheader(category + ":")
            (
                """
            [Link to world record]("""
                + world_record_predicton.WR_link
                + """) (time : """
                + world_record_predicton.WR_time
                + """)
         
            **The best possible time is :** """
                + world_record_predicton.predicted_time
            )
        except IndexError:
            st.error(
                category
                + " category doesn't have any runs so we can't calculate the best time."
            )
        except AttributeError as e:
            st.error("Something went wrong. Please try again : " + str(e) + os.getcwd())
            sys.exit()
