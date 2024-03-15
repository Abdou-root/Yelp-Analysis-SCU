import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from dbConnection import run_query
import os

st.set_page_config(
    page_title="Restaurant Insights",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to:", ["Home", "Analysis", "Business Recommendation", "Data Tables", "About"])

# Define data tables
users_table = run_query("SELECT * FROM users LIMIT 20")
restaurant_table = run_query("SELECT * FROM restaurant LIMIT 20")
review_table = run_query("SELECT * FROM review LIMIT 20")

restaurants_per_state = run_query("""
SELECT state, COUNT(state) AS `State counts`
FROM restaurant
GROUP BY state
ORDER BY `State counts` DESC
LIMIT 30;
""")

restaurants_per_city = run_query("""
SELECT city, COUNT(city) AS `City counts`
FROM restaurant
GROUP BY city
ORDER BY `City counts` DESC;
""")

distribution_of_franchises = run_query("""
SELECT name AS `Business Name`, COUNT(name) AS `counts`
FROM restaurant
GROUP BY name
ORDER BY `counts` DESC
LIMIT 20;
""")

# Page content
if selected_page == "Home":
    st.title("Welcome to the Streamlit App!")
    st.write("This is the home page. Feel free to explore other sections.")

elif selected_page == "User Analysis":
    st.title("Data Analysis")
    # Add your analysis content here

elif selected_page == "Business Recommendation":
    st.title("Business Recommendations")
    # Add your business recommendations here

elif selected_page == "Data Tables":
    st.title("Data Tables")
    st.subheader("Users Table")
    st.dataframe(users_table)

    st.subheader("Restaurant Table")
    st.dataframe(restaurant_table)

    st.subheader("Review Table")
    st.dataframe(review_table)

    st.subheader("Restaurants per State")
    st.dataframe(restaurants_per_state, use_container_width=True)

    st.subheader("Restaurants per City")
    st.dataframe(restaurants_per_city, use_container_width=True)

    st.subheader("Distribution of Franchises")
    st.dataframe(distribution_of_franchises, use_container_width=True)

elif selected_page == "About":
    st.title("About")
    st.write("This section provides information about the app and its purpose.")


