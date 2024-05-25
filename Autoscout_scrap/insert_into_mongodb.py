import pandas as pd
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://pass:word@cluster0.qrysphu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(CONNECTION_STRING)

db = client['mydatabase']

collection = db['mycollection']


df = pd.read_excel('merged_file.xlsx')


data = df.to_dict(orient='records')

collection.insert_many(data)

print("Data uploaded successfully")
