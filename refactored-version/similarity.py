from random import randint

import numpy as np

# make dictionaries to store contexts and successful page serves
from variables import MIN_PRICE, MAX_PRICE, HEADERS, LANGUAGES, AD_TYPES, COLORS


# rn=request_number
def do_similarity(request_number, min_price, max_price, successful_prices, context, context_vector, offer_vector):
    # tweak these to mess with the exploration / exploitation
    # phase_one_iterations = num iterations first exploration phase,
    # same for phase_two_iterations and phase_three_iterations
    # policies_required_to_finish_exploration = number of successful policies you want to have stored.
    # this ends the exploration phase
    phase_one_iterations = 100
    phase_two_iterations = 200
    phase_three_iterations = 300
    policies_required_to_finish_exploration = 201
    successful_policies = len(offer_vector['price'])

    if request_number < phase_one_iterations or \
            (phase_one_iterations < request_number < phase_two_iterations) or \
            (phase_two_iterations < request_number < phase_three_iterations) or \
            (request_number > phase_three_iterations and successful_policies < policies_required_to_finish_exploration):
        page = bounded_random(min_price, max_price)
        return page, successful_prices, min_price, max_price
    elif request_number == phase_one_iterations or request_number == phase_two_iterations or request_number == phase_three_iterations:
        dif_su = 1
        dif_pl = 7 - (request_number / 100) * 2
        # min_price, max_price = adjust_price(successful_prices, dif_pl, dif_su)
        page = bounded_random(min_price, max_price)
        successful_prices = []
        return page, successful_prices, min_price, max_price
    elif request_number > phase_three_iterations and successful_policies > policies_required_to_finish_exploration - 2:
        page, successful_prices = find_page(context, context_vector, offer_vector, successful_prices)
        return page, successful_prices, min_price, max_price
    else:
        print("BOO")
    pass


# used in do_similarity() to generate random pages
# ri = run_id, rn = request_number, mipr=min price, mapr=max price
def bounded_random(min_price, max_price):
    page = {'header': HEADERS[randint(0, 2)],
            'language': LANGUAGES[randint(0, 2)],
            'adtype': AD_TYPES[randint(0, 2)],
            'color': COLORS[randint(0, 4)],
            'price': randint(min_price, max_price) * 1.00}
    return page


# find page in context_vector based on similarity
def find_page(context, context_vector, offer_vector, suc_price):
    vecindex = randint(0, len(context_vector['age']))
    maxprice = -100
    tmp = 0
    tmp_context_vector = {'visitor_id': context['context']['visitor_id'],
                          'agent': context['context']['agent'],
                          'os': context['context']['os'],
                          'language': context['context']['language'],
                          'age': context['context']['age'],
                          'referrer': context['context']['referrer']}

    for x in xrange(0, len(context_vector['age'])):
        tmpprice = offer_vector['price'][x]
        simscore = 0
        if tmp_context_vector['agent'] == context_vector['agent'][x]:
            simscore += 1
        if tmp_context_vector['os'] == context_vector['os'][x]:
            simscore += 1
        if tmp_context_vector['language'] == context_vector['language'][x]:
            simscore += 1
        if tmp_context_vector['age'] == context_vector['age'][x]:
            simscore += 1
        if tmp_context_vector['referrer'] == context_vector['referrer'][x]:
            simscore += 1
        if simscore > tmp and tmpprice > maxprice:
            tmp = simscore
            maxprice = tmpprice
            vecindex = x

    page = {'header': offer_vector['header'][vecindex],
            'language': offer_vector['language'][vecindex],
            'adtype': offer_vector['adtype'][vecindex],
            'color': offer_vector['color'][vecindex],
            'price': offer_vector['price'][vecindex]}
    return page, suc_price


# used in do_similarity() to adjust price during exploration phase
# def adjust_price(successful_prices, dif_pl, dif_su):
    # avg_price = np.ceil(sum(successful_prices) / len(successful_prices))
    # if avg_price - dif_su < MIN_PRICE:
    #     min_price = MIN_PRICE
    # else:
    #     min_price = int(avg_price - dif_su)
    # if avg_price + dif_pl > MAX_PRICE:
    #     max_price = MAX_PRICE
    # else:
    #     max_price = int(avg_price + dif_pl)
    # return min_price, max_price
