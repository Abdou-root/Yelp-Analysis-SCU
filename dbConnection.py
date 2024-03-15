import pymysql.cursors
from cachetools import cached, TTLCache

# helper function to execute queries onto the streamlit web app

# 1 hour cache of max 100 elements
cache = TTLCache(maxsize=100, ttl=3600)

@cached(cache)
def run_query(query):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='startyelp',
        database='yelp',
        port=8888,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result
