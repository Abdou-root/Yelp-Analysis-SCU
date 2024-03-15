from pyspark.sql.functions import *
from pyspark import HiveContext

hc = HiveContext(sc)
df1 = hc.table('users')
df2 = hc.table('restaurant')
df3 = hc.table('review')

# Clean the 'restaurant' dataset: change the values of categories into 15 types of cuisine
keywords = [
    'American', 'Mexican', 'Italian', 'Japanese', 'Chinese', 'Thai', 'Mediterranean',
    'French', 'Vietnamese', 'Greek', 'Indian', 'Korean', 'Hawaiian', 'African', 'Spanish'
]

if 'category' not in df2.columns:
    df4 = df2.withColumn('category', lit(None))

for keyword in keywords:
    df4 = df4.withColumn('category', when(col('categories').contains(keyword), keyword).otherwise(col('category')))

# Sorting popular users in descending order by rating or number of fans
option3 = [('Average Stars', 'Average Stars'), ('Number Of Fans', 'Number Of Fans')]
selected_options = z.select("user_average_stars", option3)

if "Average Stars" in selected_options:
    selected_df = df1.select('user_id', 'user_name', 'user_average_stars') \
        .orderBy(col('user_average_stars').desc())
    z.show(selected_df)
elif "Number Of Fans" in selected_options:
    selected_df = df1.select('user_id', 'user_name', 'user_fans') \
        .orderBy(col('user_fans').desc())
    z.show(selected_df)
else:
    print("Please select an option.")

# Number of restaurant in each state
state = df4.select('state')\
    .groupBy(col('state').alias('state')) \
    .agg(count('state').alias('State counts')) \
    .orderBy(col('State counts').desc()) \

z.show(state)


# Number of restaurant in each city
city = df4.select('city')\
    .groupBy(col('city').alias('city')) \
    .agg(count('city').alias('City counts')) \
    .orderBy(col('City counts').desc()) \

z.show(city)


# Distributions of franchizes
result = df4.groupBy(col('name').alias('Business Name')) \
    .agg(count('name').alias('counts')) \
    .orderBy(col('counts').desc()) \
    .limit(20)

z.show(result)

# Top-rating restaurants in selected state or US
option1 = [('NJ', 'NJ'), ('AZ', 'AZ'), ('AB', 'AB'), ('NV', 'NV'), ('PA', 'PA'), ('CA', 'CA'), ('ID', 'ID'),
           ('DE', 'DE'), ('IL', 'IL'), ('FL', 'FL'), ('MO', 'MO'), ('TN', 'TN'), ('IN', 'IN'), ('LA', 'LA'),
           ('MT', 'MT')]
print("Top-rating Restaurant in " + " and ".join(z.select("State", option1)))

selected_states = [state for state, _ in option1 if state in z.select("State", option1)]
if not selected_states:
    selected_states = [state for state, _ in option1]
filtered_df = df4.filter(df4.state.isin(selected_states))

top_res = filtered_df.select('name', 'stars', 'review_count', 'city', 'state', 'hours', 'categories',
                             'attributes') \
    .orderBy(col('stars').desc())
z.show(top_res)

# Top-rating Restaurant of selected cuisine
option2 = [('Chinese', 'Chinese'), ('Korean', 'Korean'), ('Japanese', 'Japanese'), ('American', 'American'),
           ('Mexican', 'Mexican'), ('Italian', 'Italian'), ('Indian', 'Indian'), ('Vietnamese', 'Vietnamese'),
           ('Spanish', 'Spanish'), ('Thai', 'Thai'), ('Greek', 'Greek'), ('Mediterranean', 'Mediterranean'),
           ('French', 'French'), ('Hawaiian', 'Hawaiian'), ('African', 'African'), ('Middle_eastern', 'Middle_eastern')]
print("Top-rating Restaurant of", (z.select("Cuisine", option2)), "cuisine")

selected_cuisines = [cuisine for cuisine, _ in option2 if cuisine in z.select("Cuisine", option2)]
if not selected_cuisines:
    selected_cuisines = [cuisine for cuisine, _ in option2]

filtered_df = df4.filter(df4.category.isin(selected_cuisines))

top_cuisine = filtered_df.select('name', 'stars') \
    .orderBy(col('stars').desc())

z.show(top_cuisine)

# Latest review of selected restaurant
selected_id = z.textbox('Please insert your business id: ')
filtered_df = df3.filter(df3.rev_business_id == selected_id)

if filtered_df.count() == 0:
    print('Invalid business id')
else:
    latest_rev = filtered_df.select('rev_user_id', 'rev_stars', 'rev_date', 'rev_text', 'rev_useful', 'rev_funny', 'rev_cool') \
        .orderBy(col('rev_date').desc())

z.show(latest_rev)

# Elite users vs regular users
elite_count = df1.filter(df1.user_elite != "").count()
regular_count = df1.filter(df1.user_elite == "").count()

EliteVsRegularCount_df = z.createDataFrame([
    ("Elite Users", elite_count),
    ("Regular Users", regular_count),
], ["User Type", "Count"])

z.show(EliteVsRegularCount_df)
