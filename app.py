import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from dbConnection import run_query
import os

directory1 = 'dataset/top_rating_restaurant_cuisine'
directory2 = 'dataset/top_rating_restaurant_state'

def read_csv_files_in_directory(directory):
    files = os.listdir(directory)
    csv_files = [file for file in files if file.endswith('.csv')]
    custom_names = []
    dataframes = {}

    # Iterate over each CSV file and read it using pandas
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        # Extract custom name from the filename (without extension)
        custom_name = os.path.splitext(csv_file)[0]
        custom_names.append(custom_name)
        try:
            df = pd.read_csv(file_path, error_bad_lines=False)
            # Assign the dataframe to the custom name in the dictionary
            dataframes[custom_name] = df
        except pd.errors.ParserError as e:
            print(f"Error reading file {csv_file}: {e}")

    return custom_names, dataframes



# Call the function to read CSV files in the directories and get custom names and dataframes
custom_names1, custom_named_dataframes1 = read_csv_files_in_directory(directory1)
custom_names2, custom_named_dataframes2 = read_csv_files_in_directory(directory2)

# Display a selectbox for the user to choose a dataframe from directory1
selected_dataframe1 = st.selectbox('Select a dataframe from directory1:', custom_names1)

# Display the selected dataframe from directory1 along with column names
st.write(f"Data from file {selected_dataframe1}:")
st.write(custom_named_dataframes1[selected_dataframe1].head())

# Display a selectbox for the user to choose a dataframe from directory2
selected_dataframe2 = st.selectbox('Select a dataframe from directory2:', custom_names2)

# Display the selected dataframe from directory2 along with column names
st.write(f"Data from file {selected_dataframe2}:")
pd.set_option('display.max_columns', None)
st.dataframe(custom_named_dataframes2[selected_dataframe2].head())  # Displaying only the first few rows for better readability

# Load CSV files
top_user_fans = 'dataset/popular_user_fans.csv'
df_top_fans = pd.read_csv(top_user_fans, error_bad_lines=False)
st.dataframe(df_top_fans.head())


top_user_stars = run_query("SELECT user_id, name, average_stars FROM users ORDER BY average_stars DESC LIMIT 10;")

df_top_stars=pd.DataFrame(top_user_stars)
st.write("Top users per average stars:")
st.dataframe(df_top_stars)


# Add any other visualizations or components as needed

# Run the Streamlit app
if __name__ == "__main__":
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a page", ["Home", "Analysis", "About"])

    if app_mode == "Home":
        st.title("Welcome to Yelp Data Analysis")
        # Add content for the home page

    elif app_mode == "Analysis":
        st.title("Yelp Data Analysis")
        # Add content for the analysis page

    elif app_mode == "About":
        st.title("About")
        # Add content for the about page

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

distribution_of_franchizes = run_query("""
SELECT name AS `Business Name`, COUNT(name) AS `counts`
FROM restaurant
GROUP BY name
ORDER BY `counts` DESC
LIMIT 20;
""")

df_users = pd.DataFrame(users_table)
st.write("Users Table head:")
st.dataframe(df_users)

df_restaurant = pd.DataFrame(restaurant_table)
st.write("Restaurant Table head:")
st.dataframe(df_restaurant)

df_review = pd.DataFrame(review_table)
st.write("Review Table head:")
st.dataframe(df_review)

df_perState = pd.DataFrame(restaurants_per_state)
st.write("Number of restaurants per state")
st.dataframe(df_perState )

df_perCity = pd.DataFrame(restaurants_per_city)
st.write("Number of Restaurants per city:")
st.dataframe(df_perCity)

df_franchizes = pd.DataFrame(distribution_of_franchizes)
st.write("Most Popular franchizes:")
st.dataframe(df_franchizes)




# Count the number of elite users
regular_vs_elite = run_query("""
SELECT
    CASE WHEN LENGTH(elite) > 3 THEN 'Elite User'
         ELSE 'Regular User' END AS User_Type,
    COUNT(*) AS Count
FROM
    USERS
GROUP BY
    CASE WHEN LENGTH(elite) > 3 THEN 'Elite User'
         ELSE 'Regular User' END
""")
# Concatenate the DataFrames to create the final DataFrame
EliteVsRegularCount_df = pd.DataFrame(regular_vs_elite)

# Rename index
EliteVsRegularCount_df.index = ['Elite', 'Regular']

st.write("Counts of Elite vs Regular Users:")
st.write(EliteVsRegularCount_df)

# Title for the Streamlit app
st.title("Fetch Reviews by Business ID")

# Input field for business id
selected_id = st.text_input('Please insert your business id:')

# Check if input is provided
if selected_id:
    # SQL query to fetch reviews for the selected business id
    query = f"""
        SELECT user_id, stars, date, text, useful, funny, cool
        FROM review
        WHERE business_id = '{selected_id}'
        ORDER BY date DESC
        LIMIT 10;
    """

    # Execute the query
    latest_review = run_query(query)

    # Check if any results are returned
    if latest_review is not None:
        # Display results in a table
        df_latest_review = pd.DataFrame(latest_review)
        st.write("Latest Reviews:")
        st.write(df_latest_review)
    else:
        # Display message for invalid business id
        st.write("Invalid business id")
