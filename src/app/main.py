import streamlit as st
from back import request_categories, request_data
import sys

st.title("TAS Predictor")
st.header("Predict the best possible times of your favorite speedgame.")
st.write("""Your speedgame don't have TASes ? Do you want to know how fast this goofy extension category can be ?
 
This machine learning-driven app will give you answers.""")

game_form = st.form("game_form")
game = game_form.text_input("Type a game :")
game_submitted = game_form.form_submit_button("Get best possible times !")
if game_submitted:
    try:
        categories = request_categories(game)
    except IndexError:
        st.error("Your game has not been found. Try to look for typos.")
        sys.exit("Your game has not been found. Try to look for typos.")
    for category in categories:
        try:
            results = request_data(game, category)
            WR_link = results["WR_link"]
            WR_time = results["WR_time"]
            predicted_time = results["predicted_time"]
            st.subheader(category + ":")
            (
                """
            [Link to world record]("""
                + WR_link
                + """) (time : """
                + WR_time
                + """)
         
            **The best possible time is :** """
                + predicted_time
            )
        except IndexError:
            st.error(
                category
                + " category doesn't have any runs so we can't calculate the best time."
            )
