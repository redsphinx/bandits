import sys
import numpy as np
sys.path.append('../')

from aiws import api
api.authenticate('TEAM NAME','TEAM PASSWORD')

def test_random_requests():
    run_id = 0

    cumulative_reward = 0
    n = 1000

    for request_number in xrange(n):

        context = api.get_context(run_id, request_number)
        print context['context'].values()


        offer = {
            'header': [5, 15, 35],
            'language': ['NL', 'EN', 'GE'],
            'adtype': ['skyscraper', 'square', 'banner'],
            'color': ['green', 'blue', 'red', 'black', 'white'],
            'price': map(lambda x: 1+float(x)/10.,range(490))
        }
        # Random choice
        offer = {key: np.random.choice(val) for key, val in offer.iteritems()}

        result = api.serve_page(run_id, request_number,
            header=offer['header'],
            language=offer['language'],
            adtype=offer['adtype'],
            color=offer['color'],
            price=offer['price'])

        print result, offer['price'] * result['success']
        cumulative_reward += offer['price'] * result['success']

    mean_reward = cumulative_reward / n
    print "Mean reward: %.2f euro" % mean_reward

if __name__ == "__main__":
    test_random_requests()
