import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client['fighter_details']
mongo_coll = mongo_db['fighters']

find_fighter = mongo_coll.find({"fighter_name": "Zubaira Tukhugov"})

for fighter in find_fighter:
    print(fighter['Height'])