import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from dbConnection import run_query
import os


st.set_page_config(page_title="Tastify", page_icon="🍔")
st.markdown('<style>%s</style>' % open('styles.css').read(), unsafe_allow_html=True)

# BULK Tables queries
users_table = run_query("SELECT * FROM users LIMIT 20")
restaurant_table = run_query("SELECT * FROM restaurant LIMIT 20")
review_table = run_query("SELECT * FROM review LIMIT 20")

# MySQL queries to run for data analysis
restaurants_per_state = run_query("""
SELECT state, COUNT(state) AS `State counts`
FROM restaurant
GROUP BY state
ORDER BY `State counts` DESC
LIMIT 30;
""")
# Number of restaurants per city
restaurants_per_city = run_query("""
SELECT city, COUNT(city) AS `City counts`
FROM restaurant
GROUP BY city
ORDER BY `City counts` DESC;
 """)
# Distribution of franchizes
distribution_of_franchizes = run_query("""
SELECT name AS `Business Name`, COUNT(name) AS `counts`
FROM restaurant
GROUP BY name
ORDER BY `counts` DESC
LIMIT 20;
""")

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

# Streamlit Setup
if __name__ == "__main__":
    st.sidebar.image("images/logo.png", use_column_width=True)

    app_mode = st.sidebar.radio("", ["🏠 Home", "🍽️ User Recommendation", "🍳 Business Recommendation", "📋 Review Analysis", "📊 Data Tables", "📌 About"])

    if app_mode == "🏠 Home":
        st.markdown("<h1 style='text-align: center;'>Yelp Data Analysis by #Team 01</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Welcome to Tastify!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Find nearby restaurants, explore top-rated eateries, and read reviews. If you're a business owner, we'll connect you with highly-rated users to boost exposure.</p>", unsafe_allow_html=True)
        # Add content for the home page
        st.image("images/bg.jpg", use_column_width=True)

    elif app_mode == "🍽️ User Recommendation":

        # Most popular franchizes
        df_franchizes = pd.DataFrame(distribution_of_franchizes)
        st.write("**Most Popular franchizes:**")
        st.dataframe(df_franchizes, use_container_width=True)
        # Pie chart
        fig = px.pie(df_franchizes, values='counts', names='Business Name', title='Pie Chart Representation')
        st.plotly_chart(fig)

        # Reading data from csv's for top rated restaurants
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

        # Reading Data
        custom_names1, custom_named_dataframes1 = read_csv_files_in_directory(directory1)
        custom_names2, custom_named_dataframes2 = read_csv_files_in_directory(directory2)

        # SelectBox for directory1
        selected_dataframe1 = st.selectbox('**Select a cuisine type:**', custom_names1)

        # Displaying top rated restaurants per cuisine
        st.write("**Top Rated Restaurants in the selected cuisine**")
        st.dataframe(custom_named_dataframes1[selected_dataframe1], use_container_width=True)
        df_top_per_cuisine = custom_named_dataframes1[selected_dataframe1]

        # Bar Chart
        fig = px.bar(df_top_per_cuisine, x='name', y='stars', title='Top Rated Restaurants')

        # Display the bar chart using Streamlit
        st.plotly_chart(fig)

        # Display a selectbox for the user to choose a dataframe from directory2
        selected_dataframe2 = st.selectbox('Select a state:', custom_names2)
        st.write(f"**Top Rated Restaurants in the selected location**")
        st.dataframe(custom_named_dataframes2[selected_dataframe2], use_container_width=True)


    elif app_mode == "🍳 Business Recommendation":
        # Most popular users according to fans
        st.subheader("**Most Popular Users per Fans**")
        top_user_fans = 'dataset/popular_user_fans.csv'
        df_top_fans = pd.read_csv(top_user_fans, error_bad_lines=False, nrows=100)
        st.dataframe(df_top_fans, use_container_width=True)

        # Most popular users according to average stars
        top_user_stars = 'dataset/popular_user_stars.csv'
        df_top_stars = pd.read_csv(top_user_stars, error_bad_lines=False, nrows=100)
        st.subheader("**Most Popular Users per Average Stars**")
        st.dataframe(df_top_stars, use_container_width=True)

        # Display number of restaurants per state
        df_perState = pd.DataFrame(restaurants_per_state)
        st.subheader("Number of restaurants per state")
        fig_per_state = px.bar(df_perState, x='state', y='State counts', title='Restaurants per State')
        st.plotly_chart(fig_per_state)

        # Display number of restaurants per city
        df_perCity = pd.DataFrame(restaurants_per_city)
        st.subheader("Number of Restaurants per city:")
        fig_per_city = px.bar(df_perCity, x='city', y='City counts', title='Restaurants per City')
        st.plotly_chart(fig_per_city)

        # Concatenate the DataFrames to create the final DataFrame and display it
        EliteVsRegularCount_df = pd.DataFrame(regular_vs_elite)
        EliteVsRegularCount_df.index = ['Elite', 'Regular']
        st.title("Counts of Elite vs Regular Users:")
        st.write(EliteVsRegularCount_df)

        # Get Most Recent Reviews for a certain restaurant
        st.title("Fetch Reviews by Business ID")
        # Input field for business id
        selected_id = st.text_input('Please insert a business id:')
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



    elif app_mode == "📋 Review Analysis":
        def display_data(cuisine_name):
            image_path = f"images/{cuisine_name.lower()}.png"
            st.write(f"Word Cloud for {cuisine_name} Cuisine")
            st.image(image_path, caption=cuisine_name, use_column_width=True)

        st.header("Data extracted from each cuisine")
        # Determine the cuisine selected by the user
        cuisine = st.selectbox("Select Cuisine",
                               ["Mexican", "Japanese", "Chinese", "Thai", "Vietnamese", "French", "Italian"])

        # Display the corresponding word cloud for the selected cuisine
        display_data(cuisine)

        # Function to display recommendations for each cuisine in a card-like layout
        def display_cuisine_recommendations(cuisine, recommendations):
            st.write(f"## Recommendations for {cuisine}")
            st.markdown(f"<div style='width: 700px'>{recommendations}</div>", unsafe_allow_html=True)
        # Streamlit app
        st.title("Review Analysis")

        # Display recommendations for each cuisine
        cuisine_recommendations = {
            "Mexican": """
                    Mexican cuisine delights with its bold flavors and warm hospitality. 
                    Prioritizing freshness and friendly service is essential for restaurants
                    to create a memorable dining experience. Avoiding serving cold dishes 
                    or neglecting cleanliness is crucial, as it can detract from enjoyment.
                    By focusing on delicious fare and attentive service, Mexican restaurants
                    can ensure a positive reputation and keep patrons coming back for more.    
               """,
            "Japanese": """
                    In Japanese restaurants, besides prioritizing delicious cooking, using fresh
                    ingredients is crucial. Additionally, creating innovative twists on 
                     traditional dishes can attract customers and diversify the menu. 
                     Regarding service, training waitstaff to provide friendly and attentive
                     care while avoiding mistakes like serving the wrong food is essential. 
                     In terms of management, investing in technology to preserve ingredients'
                     freshness and responding to customer feedback for improvements are recommended strategies.
               """,
            "Chinese": """
                    Delicious and authentic food should be the top priority for Chinese restaurants,
                    aiming to garner high ratings. Offering flavors that are both hot and savory without
                    being overly sour or bland is key. Improving cooking methods, especially for greasy
                    dishes, and using fresh ingredients can enhance the dining experience. Service-wise,
                    training waiters to deliver professional, efficient, and courteous service is crucial
                    for customer satisfaction. Moreover, maintaining reasonable prices can attract more patrons..
                       """,
            "Thai": """
                    Taste reigns supreme in Thai cuisine, with customers preferring fresh, flavorful dishes
                    that aren't overly sour or bland. Variety is appreciated, while mushy or greasy textures
                    are generally disliked. Monitoring local preferences and adjusting recipes accordingly
                    is recommended. Regarding service, prompt and attentive care is essential, as customers
                    dislike slow service. Additionally, maintaining reasonable prices and a comfortable 
                    environment are key factors for success..
                       """,
            "Vietnamese": """
                    Vietnamese restaurants should prioritize cleanliness and a pleasant atmosphere, as these
                    factors heavily influence customer reviews. Offering tender, generously portioned dishes
                    made with fresh ingredients is essential for attracting and retaining customers. Addressing
                    issues such as slow or rude service through professional training can significantly improve
                    the dining experience. Maintaining reasonable prices further enhances customer satisfaction
                    and loyalty.
                       """,
            "French": """
                    Cleanliness and ambiance significantly impact customer perceptions in French restaurants. 
                    Providing tender, generously portioned dishes made with fresh ingredients can attract and
                    retain customers. Additionally, addressing service issues such as incorrect orders or slow 
                    service is crucial for maintaining customer satisfaction. Training waitstaff to be courteous
                    and professional can mitigate these issues and improve overall dining experiences. Moreover,
                    maintaining reasonable prices can enhance customer loyalty.
                       """,
            "Italian": """
                    Cleanliness and ambiance play a significant role in customer satisfaction in Italian restaurants.
                    Offering tender, generously portioned dishes made with fresh ingredients is essential for attracting
                    and retaining customers. Additionally, addressing service issues such as incorrect orders or slow service 
                    is crucial for maintaining customer satisfaction. Training waitstaff to be courteous and professional 
                    can mitigate these issues and improve overall dining experiences. Moreover, maintaining reasonable prices 
                    can enhance customer loyalty.
                       """,
        }

        for cuisine, recommendations in cuisine_recommendations.items():
            display_cuisine_recommendations(cuisine, recommendations)

    elif app_mode == "📊 Data Tables":
        st.title("Data Tables")
        # Display tables function
        def display_tables():
            # Display Users Table
            st.subheader("Users Table")
            df_users = pd.DataFrame(users_table)
            st.dataframe(df_users.head(20))

            # Display Restaurant Table
            st.subheader("Restaurant Table")
            df_restaurant = pd.DataFrame(restaurant_table)
            st.dataframe(df_restaurant.head(20))

            # Display Review Table
            st.subheader("Review Table")
            df_review = pd.DataFrame(review_table)
            st.dataframe(df_review.head(20))

            # Display Most Popular Franchizes
            st.subheader("Most Popular Franchizes")
            df_franchizes = pd.DataFrame(distribution_of_franchizes)
            st.dataframe(df_franchizes.head(20))

            st.subheader("Elite Vs Regular Count Table")
            EliteVsRegularCount_df_display = pd.DataFrame(EliteVsRegularCount_df)
            st.dataframe(EliteVsRegularCount_df_display.head(20))

            st.subheader("Top Stars Table")
            df_top_stars_display = pd.DataFrame(df_top_stars)
            st.dataframe(df_top_stars_display.head(20))

            st.subheader("Top Fans Table")
            df_top_fans_display = pd.DataFrame(df_top_fans)
            st.dataframe(df_top_fans_display.head(20))

            st.subheader("Top Per Cuisine Table")
            df_top_per_cuisine_display = pd.DataFrame(df_top_per_cuisine)
            st.dataframe(df_top_per_cuisine_display.head(20))



        # Call display_tables function
        display_tables()
    elif app_mode == "📌 About":

        st.title("📌 About")

        st.title("Project Manager")

        st.write("Name: **Muza**")
        st.write("Github: [muzcodes](https://github.com/muzcodes)")
        st.write("Email: mujahidshubhro@gmail.com")

        st.title("Co-Developers")

        st.write("Name: **Abdessamad Grine**")
        st.write("Github: [Abdou-root](https://github.com/Abdou-root)")
        st.write("Email: grineabdessamed2003@gmail.com")

        st.write("Name: **Nicholes**")
        st.write("Github: [REDZY6](https://github.com/REDZY6)")
        st.write("Email: nccynicholeschin@gmail.com")

        st.write("Name: **Hebe**")
        st.write("Github: [LazyDaizy03](https://github.com/LazyDaizy03)")
        st.write("Email: hbeebe030330@gmail.com")


