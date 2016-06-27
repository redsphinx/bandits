import sys

import numpy as np

sys.path.append('../aiws-api/')
from aiws import api

# import fakeapi as api
api.authenticate('billy-the-kid', 'f2d38030ad785607cb697a1e31150a41')

agents = {'Mozilla Firefox': 0, 'Google Chrome': 1, 'Safari': 2, 'Opera': 3, 'Internet Explorer': 4}
oses = {'Windows': 0, 'OSX': 1, 'Android': 2, 'iOS': 3, 'Linux': 4}
languages = {'NL': 0, 'EN': 1, 'GE': 2, 'Other': 3}
referrers = {'Google': 0, 'Bing': 1, 'Other': 2}

opts = {
    'header': [5, 15, 35],
    'language': ['NL', 'EN', 'GE'],
    'adtype': ['skyscraper', 'square', 'banner'],
    'color': ['green', 'blue', 'red', 'black', 'white'],
    'price': [10., 20., 30., 40., 50.],
}

language_map = {"EN": "EN", "NL": "NL", "GE": "GE", "Other": "EN"}
os_header_map = {"Windows": 35, "OSX": 15, "Android": 5, "iOS": 5, "Linux": 35}

EXPLORATION_STEPS = 50
EXPLORATION_PRICE = 9.99


def schwifty(from_run_id=0, to_run_id=20):
    for run_id in xrange(from_run_id, to_run_id):
        # color_map = {'green': 0, 'blue': 1, 'red': 2, 'black': 3, 'white': 4}
        color_tries = np.ones((2, 5))

        prices = np.array([49.99, 44.99, 39.99, 34.99, 29.99, 24.99, 19.99, 15.99, 9.99, 5.99, 0.99])
        price_tries = np.ones((2, len(prices)))

        # adtype_map = {'skyscraper': 0, 'square': 1, 'banner': 2}
        adtype_tries = np.ones((2, 3))
        count = 0
        for retry in [0, 1]:
            cumulative_reward = 0
            success_count = 0
            for request_number in xrange(0, 10000):
                context = api.get_context(run_id, request_number)["context"]

                language = language_map[str(context["language"])]
                header = os_header_map[str(context["os"])]

                color_index = np.argmax(np.random.beta(color_tries[0, :], color_tries[1, :]))
                color = opts["color"][color_index]

                adtype_index = np.argmax(np.random.beta(adtype_tries[0, :], adtype_tries[1, :]))
                adtype = opts["adtype"][adtype_index]
                exploration = count < EXPLORATION_STEPS
                if exploration:
                    price = EXPLORATION_PRICE
                else:
                    price_index = np.argmax(
                        np.multiply(np.random.beta(price_tries[0, :], price_tries[1, :]), np.log(prices)))
                    price = prices[price_index]
                result = api.serve_page(run_id, request_number,
                                        header=header,
                                        language=language,
                                        adtype=adtype,
                                        color=color,
                                        price=price)
                cumulative_reward += price * result['success']
                ab = 0 if result["success"] else 1
                if not exploration:
                    price_tries[ab, price_index] += 1
                adtype_tries[ab, adtype_index] += 1
                color_tries[ab, color_index] += 1
                success_count += result['success']
                if request_number % 100 == 0:
                    print "%.2f, %d/%d" % (
                    cumulative_reward / (request_number + 1), success_count, (request_number + 1))
                count += 1


if __name__ == "__main__":
    arg_run_id = 5000
    if len(sys.argv) > 1:
        arg_run_id = int(sys.argv[1])
        schwifty(arg_run_id, arg_run_id + 1)
    else:
        schwifty()
