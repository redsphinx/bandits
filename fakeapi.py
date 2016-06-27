from pymongo import MongoClient

agents = {'Mozilla Firefox': 0, 'Google Chrome': 1, 'Safari': 2, 'Opera': 3, 'Internet Explorer': 4}
oses = {'Windows': 0, 'OSX': 1, 'Android': 2, 'iOS': 3, 'Linux': 4}
languages = {'NL': 0, 'EN': 1, 'GE': 2, 'Other': 3}
referrers = {'Google': 0, 'Bing': 1, 'Other': 2}

client = MongoClient('localhost', 27017)
db = client.aiws
training_collection = db.training

run_ids = training_collection.distinct("run_id")

def authenticate(key, password):
    pass

def get_record(run_id, request_number):
    return training_collection.find({"run_id": run_ids[run_id]}).skip(request_number % 100).next()


def get_context(run_id, request_number):
    return get_record(run_id, request_number)["context"]


def serve_page(run_id, request_number, header, language, adtype, color, price):
    ctx = get_record(run_id, request_number)
    results = ctx["results"]
    for result in results:
        if result[0] == header and result[1] == language and result[2] == adtype and result[3] == color and result[4] < price:
            return {'success': True}
    return {'success': False}
