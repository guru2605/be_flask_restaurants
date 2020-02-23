import os

SECRET = os.environ['SECRET']

# MONGO CONFIG
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = int(os.environ['MONGO_PORT'])
MONGO_DBNAME = os.environ['MONGO_DBNAME']

# MONGO COLLECTIONS
MONGO_COL_HOTELS = 'hotels'
MONGO_COL_USERS = 'users'
