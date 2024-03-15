import json
import pymysql

# Read JSON files
with open("F:\yelp\yelp_academic_dataset_business.json", encoding='utf-8') as f1:
    json_data_business = f1.readlines()
with open("F:\yelp\yelp_academic_dataset_user.json", encoding='utf-8') as f2:
    json_data_users = f2.readlines()
with open("F:\yelp\yelp_academic_dataset_review.json", encoding='utf-8') as f3:
    json_data_reviews = f3.readlines()

# Connect to MySQL database
cnx = pymysql.connect(user='root', password='startyelp', port=8888,
                      host='localhost', database='yelp')
cursor = cnx.cursor()

# Insert JSON data into the restaurant table
for line in json_data_business:
    data1 = json.loads(line.strip())
    categories = data1.get('categories')
    if categories is not None and 'Restaurants' in categories:
        business_id = data1['business_id']
        name = data1['name']
        address = data1['address']
        city = data1['city']
        state = data1['state']
        postal_code = data1['postal_code']
        latitude = data1['latitude']
        longitude = data1['longitude']
        stars = data1['stars']
        review_count = data1['review_count']
        is_open = data1['is_open']
        attributes = json.dumps(data1['attributes'])
        categories = data1['categories']
        hours = json.dumps(data1.get('hours', None))

        # Insert the data into the 'restaurant' table
        with cnx.cursor() as cursor:
            query1 = "INSERT INTO restaurant (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values1 = (
            business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open,
            attributes, categories, hours)
            cursor.execute(query1, values1)

# Insert JSON data into the users table
# for line in json_data_users:
#     data2 = json.loads(line.strip())
#     user_id = data2['user_id']
#     name = data2['name']
#     review_count = data2['review_count']
#     yelping_since = data2['yelping_since']
#     friends = json.dumps(data2['friends'])
#     useful = data2['useful']
#     funny = data2['funny']
#     cool = data2['cool']
#     fans = data2['fans']
#     elite = json.dumps(data2['elite'])
#     average_stars = data2['average_stars']
#     compliment_hot = data2['compliment_hot']
#     compliment_more = data2['compliment_more']
#     compliment_profile = data2['compliment_profile']
#     compliment_cute = data2['compliment_cute']
#     compliment_list = data2['compliment_list']
#     compliment_note = data2['compliment_note']
#     compliment_plain = data2['compliment_plain']
#     compliment_cool = data2['compliment_cool']
#     compliment_funny = data2['compliment_funny']
#     compliment_writer = data2['compliment_writer']
#     compliment_photos = data2['compliment_photos']
#
#     with cnx.cursor() as cursor:
#         query2 = "INSERT INTO users (user_id, name, review_count, yelping_since, friends, useful, funny, cool, fans, elite, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         values2 = (
#             user_id,
#             name,
#             review_count,
#             yelping_since,
#             friends,
#             useful,
#             funny,
#             cool,
#             fans,
#             elite,
#             average_stars,
#             compliment_hot,
#             compliment_more,
#             compliment_profile,
#             compliment_cute,
#             compliment_list,
#             compliment_note,
#             compliment_plain,
#             compliment_cool,
#             compliment_funny,
#             compliment_writer,
#             compliment_photos
#         )
#         cursor.execute(query2, values2)

# Insert JSON data into the review table
# for line in json_data_reviews:
#     data3 = json.loads(line.strip())
#     review_id = data3['review_id']
#     user_id = data3['user_id']
#     business_id = data3['business_id']
#     stars = data3['stars']
#     useful = data3['useful']
#     funny = data3['funny']
#     cool = data3['cool']
#     text = data3['text']
#     date = data3['date']
#
#     with cnx.cursor() as cursor:
#         query3 = "INSERT INTO review (review_id, user_id, business_id, stars, useful, funny, cool, text, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         values3 = (
#             review_id,
#             user_id,
#             business_id,
#             stars,
#             useful,
#             funny,
#             cool,
#             text,
#             date
#         )
#         cursor.execute(query3, values3)


# Commit and close the connection
cnx.commit()
cursor.close()
cnx.close()
