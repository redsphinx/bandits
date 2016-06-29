from pymongo import MongoClient


agents = {'Mozilla Firefox': 0, 'Google Chrome': 1, 'Safari': 2, 'Opera': 3, 'Internet Explorer': 4}
oses = {'Windows': 0, 'OSX': 1, 'Android': 2, 'iOS': 3, 'Linux': 4}
languages = {'NL': 0, 'EN': 1, 'GE': 2, 'Other': 3}
referrers = {'Google': 0, 'Bing': 1, 'Other': 2}

client = MongoClient('localhost', 27017)
db = client.aiws
training_collection = db.training

run_ids = training_collection.distinct("run_id")
print run_ids

language_map = {"EN": "EN", "NL": "NL", "GE": "GE", "Other": "EN"}
os_header_map = {"Windows": 35, "OSX": 15, "Android": 5, "iOS": 5, "Linux": 35}

banner_dict = {'skyscraper': 0, 'square': 0, 'banner': 0}
count = 0
misfits = []
for truth in training_collection.find({"run_id": 150}):
    context = truth["context"]["context"]
    results = truth["results"]
    banners = set()
    for result in results:
        banners.add(result[2])
    misfits.append((context, banners))
