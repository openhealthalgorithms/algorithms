# from sqlalchemy import create_engine
from pymongo import MongoClient

client = MongoClient("mongodb://oha:32LazySnails@128.199.199.111:27017")

db = client.ohaDataStore

cursor = db.data.find({})
print(db)

for document in cursor:
    print(document)

# engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
