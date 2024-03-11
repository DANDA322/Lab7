import pymongo
import json

client = pymongo.MongoClient("mongodb://mongo:secret@localhost:27017")

db = client["db"]

stadiums = db["stadiums"]
singers = db["singers"]
concerts = db["concerts"]
singer_in_concert = db["singer_in_concert"]


json_file_path = 'data/concert_singer.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)

stadiums.insert_many(data["stadium"])
singers.insert_many(data["singer"])
concerts.insert_many(data["concert"])
singer_in_concert.insert_many(data["singer_in_concert"])

client.close()
