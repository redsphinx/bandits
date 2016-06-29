import numpy as np

from variables import MIN_PRICE, MAX_PRICE


# used in show_us_what_you_got() to update the pass-fail
# count on all the page serve elements except price for policy 2 (do_beta())
def update_counts(name, item):
    name[str(item)] += 1


# used in show_us_what_you_got() to update the pass-fail count on the price serve element for policy 2
def update_counts_price(name, item):
    ind = int(item - MIN_PRICE - 1)
    name[ind] += 1


def make_dicts_for_similarity():
    context_vector = {'visitor_id': np.array([]),
                      'agent': np.array([]),
                      'os': np.array([]),
                      'language': np.array([]),
                      'age': np.array([]),
                      'referrer': np.array([])}
    offer_vector = {'header': np.array([]),
                    'language': np.array([]),
                    'adtype': np.array([]),
                    'color': np.array([]),
                    'price': np.array([])}
    return context_vector, offer_vector


# makes dictionary with the page elements containing pass-fail counts
# used in show_us_what_you_got()
def make_pass_fail_dicts():
    # store how many times something has been chosen with success and how many times with failure
    header_pass = {'5': 1, '15': 1, '35': 1}
    header_fail = {'5': 1, '15': 1, '35': 1}
    language_pass = {'NL': 1, 'EN': 1, 'GE': 1}
    language_fail = {'NL': 1, 'EN': 1, 'GE': 1}
    adtype_pass = {'skyscraper': 1, 'square': 1, 'banner': 1}
    adtype_fail = {'skyscraper': 1, 'square': 1, 'banner': 1}
    color_pass = {'green': 1, 'blue': 1, 'red': 1, 'black': 1, 'white': 1}
    color_fail = {'green': 1, 'blue': 1, 'red': 1, 'black': 1, 'white': 1}
    price_pass = []
    price_fail = []
    for i in xrange(MIN_PRICE, MAX_PRICE + 1):
        price_pass.append(1)
        price_fail.append(1)
    return header_pass, header_fail, \
           language_pass, language_fail, \
           adtype_pass, adtype_fail, \
           color_pass, color_fail, \
           price_pass, price_fail
