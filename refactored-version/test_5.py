import sys
import time

import numpy as np

from beta import do_beta
from beta_page import do_beta_page
from helpers import update_counts, update_counts_price, make_dicts_for_similarity, make_pass_fail_dicts
from similarity import do_similarity
from variables import BLANK, MAX_PRICE, MIN_PRICE

sys.path.append('../aiws-api/')
from aiws import api

api.authenticate('billy-the-kid', 'f2d38030ad785607cb697a1e31150a41')


# store successful context and page serve
# i dont know why i called it vector. they are dictionaries with a list as a value
def store_page(context, context_vector, offer_vector, tmp_offer_vector):
    context_vector['visitor_id'] = np.append(context_vector['visitor_id'], context['context']['visitor_id'])
    context_vector['agent'] = np.append(context_vector['agent'], context['context']['agent'])
    context_vector['os'] = np.append(context_vector['os'], context['context']['os'])
    context_vector['language'] = np.append(context_vector['language'], context['context']['language'])
    context_vector['age'] = np.append(context_vector['age'], context['context']['age'])
    context_vector['referrer'] = np.append(context_vector['referrer'], context['context']['referrer'])
    offer_vector['header'] = np.append(offer_vector['header'], tmp_offer_vector['header'])
    offer_vector['language'] = np.append(offer_vector['language'], tmp_offer_vector['language'])
    offer_vector['adtype'] = np.append(offer_vector['adtype'], tmp_offer_vector['adtype'])
    offer_vector['color'] = np.append(offer_vector['color'], tmp_offer_vector['color'])
    offer_vector['price'] = np.append(offer_vector['price'], tmp_offer_vector['price'])
    return context_vector, offer_vector
    pass


# given all your policies, it selects the winner by drawing a number from beta distr
# returns the page of the winning policy
# p1 is similarity, p2 is beta, p3 is beta_page
def choose_from_policies(p1, p2, p1pass, p1fail, p2pass, p2fail, p3, p3pass, p3fail):
    winning_policy_index = np.argmax([np.random.beta(p1pass, p1fail),
                                      np.random.beta(p2pass, p2fail),
                                      np.random.beta(p3pass, p3fail) if p3 != BLANK else -1])
    offers_by_policies = [p1, p2, p3]
    return offers_by_policies[winning_policy_index], winning_policy_index


# checks if a page is already stored
def check_if_page_in_offer_vector(page, offer_vector):
    ind = []
    b = False
    if len(offer_vector["header"]) > 0:
        h, l, a, c, p = page["header"], page["language"], page["adtype"], page["color"], page["price"]
        for i in xrange(len(offer_vector["header"])):
            if offer_vector["header"][i] == h and \
                    offer_vector["language"][i] == l and \
                    offer_vector["adtype"][i] == a and \
                    offer_vector["color"][i] == c and \
                    offer_vector["price"][i] == p:
                ind.append(i)
                b = True
    return b, ind


# remove all offers in offer and context vectors, that are below threshold
def remove_weak_pages(threshold, offer_vector, context_vector):
    new_context_vector, new_offer_vector = make_dicts_for_similarity()

    to_be_removed = offer_vector["price"] < threshold
    to_be_kept = (to_be_removed != True)
    new_offer_vector["header"] = offer_vector["header"][to_be_kept]
    new_offer_vector["language"] = offer_vector["language"][to_be_kept]
    new_offer_vector["adtype"] = offer_vector["adtype"][to_be_kept]
    new_offer_vector["color"] = offer_vector["color"][to_be_kept]
    new_offer_vector["price"] = offer_vector["price"][to_be_kept]
    new_context_vector["visitor_id"] = context_vector["visitor_id"][to_be_kept]
    new_context_vector["agent"] = context_vector["agent"][to_be_kept]
    new_context_vector["os"] = context_vector["os"][to_be_kept]
    new_context_vector["language"] = context_vector["language"][to_be_kept]
    new_context_vector["age"] = context_vector["age"][to_be_kept]
    new_context_vector["referrer"] = context_vector["referrer"][to_be_kept]
    removed_indexes = np.array(range(0, len(offer_vector["price"])))
    removed_indexes = removed_indexes[to_be_removed]

    return removed_indexes, new_offer_vector, new_context_vector


def show_us_what_you_got(from_run_id=5000, to_run_id=5010):
    run_id_results = []
    req_nums = 10000

    for run_id in xrange(from_run_id, to_run_id):
        header_pass, header_fail, language_pass, language_fail, \
        adtype_pass, adtype_fail, color_pass, \
        color_fail, price_pass, price_fail = make_pass_fail_dicts()
        context_vector, offer_vector = make_dicts_for_similarity()
        min_price, max_price = MIN_PRICE, 30
        # ---
        # make a pass and fail int to store how many times you pass and fail
        # ---
        p1pass, p1fail, p2pass, p2fail, p3pass, p3fail = 1, 1, 1, 1, 1, 1
        successful_prices = []
        ov_pass, ov_fail = [], []
        for repeat_step in xrange(0, 3):
            cumulative_reward = 0
            num_suc = 0
            for request_number in xrange(0, req_nums):
                context = api.get_context(run_id, request_number)

                page1, successful_prices, min_price, max_price = do_similarity(request_number, min_price, max_price,
                                                                               successful_prices,
                                                                               context, context_vector, offer_vector)
                page2 = do_beta(header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail,
                                color_pass, color_fail, price_pass, price_fail, min_price, max_price)
                page3 = do_beta_page(offer_vector, ov_pass, ov_fail)

                # add your new page to make_new_page()
                page, winner = choose_from_policies(page1, page2, p1pass, p1fail, p2pass, p2fail, page3, p3pass, p3fail)
                page['header'] = int(page['header'])  # Sometimes we get a float here.. I couldn't find why. /erdi
                result = api.serve_page(run_id, request_number,
                                        header=int(page['header']),
                                        language=page['language'],
                                        adtype=page['adtype'],
                                        color=page['color'],
                                        price=page['price'])
                cumulative_reward += page['price'] * result['success']

                if result['success']:
                    update_counts(header_pass, page['header'])
                    update_counts(language_pass, page['language'])
                    update_counts(adtype_pass, page['adtype'])
                    update_counts(color_pass, page['color'])
                    update_counts_price(price_pass, page['price'])
                    # if winner =! 3 and if the page is not stored then store the success page
                    bb, indd = check_if_page_in_offer_vector(page, offer_vector)
                    if winner < 3 and not bb:
                        context_vector, offer_vector = store_page(context, context_vector, offer_vector, page)
                        # grow vector as offers get added
                        ov_pass.append(1)
                        ov_fail.append(1)

                    successful_prices.append(page["price"])
                    b, ind = check_if_page_in_offer_vector(page, offer_vector)
                    if b:
                        for i in ind:
                            ov_pass[i] += 1

                    # ---
                    # update the counter of your new policy
                    # ---
                    # update beta p1 p2 p3
                    if winner == 1:
                        p1pass += 1
                    elif winner == 2:
                        p2pass += 1
                    elif winner == 3:
                        p3pass += 1
                    num_suc += 1
                else:
                    # print("FAILURE")
                    # update beta counters
                    update_counts(header_fail, page['header'])
                    update_counts(language_fail, page['language'])
                    update_counts(adtype_fail, page['adtype'])
                    update_counts(color_fail, page['color'])
                    update_counts_price(price_fail, page['price'])

                    b, ind = check_if_page_in_offer_vector(page, offer_vector)
                    if b:
                        for i in ind:
                            ov_fail[i] += 1
                    # ---
                    # update the counter of your new policy
                    # ---
                    # update beta p1 p2 p3
                    if winner == 1:
                        p1fail += 1
                    elif winner == 2:
                        p2fail += 1
                    elif winner == 3:
                        p3fail += 1
                # removing excess weak / cheap pages
                if len(offer_vector["price"]) > 40:
                    prev = len(offer_vector["price"])
                    # threshold = np.mean(successful_prices) #this is thresholding with the mean but i think it will delete too much
                    # threshold = 23
                    threshold = np.median(offer_vector["price"]) if len(offer_vector["price"]) is not 0 else 23
                    newovp, newovf = [], []
                    indx, offer_vector, context_vector = remove_weak_pages(threshold, offer_vector, context_vector)
                    for ii in xrange(prev):
                        if ii not in indx:
                            newovp.append(ov_pass[ii])
                            newovf.append(ov_fail[ii])
                    ov_pass, ov_fail = newovp, newovf
                    if len(offer_vector["price"]) != 0:
                        min_price = int(np.max((np.min((np.mean(offer_vector["price"]) - 1, MAX_PRICE)), MIN_PRICE)))
                        max_price = int(np.min((np.max(offer_vector["price"]) + 1, MAX_PRICE)))
                        print("new prices: %d, %d" % (min_price, max_price))
                if request_number % 100 == 0:
                    print time.time()
                    print "run_id=%d request_number=%d mean_reward=%.3f success_rate=%d:%d price:%d p1-pf:%d-%d p2-pf:%d-%d p3-pf:%d-%d" % \
                          (run_id, request_number, cumulative_reward / (request_number + 1), num_suc, request_number,
                           page["price"], p1pass, p1fail, p2pass, p2fail, p3pass, p3fail)
            if num_suc == 0:
                num_suc = 1
            # you might want to end a print at the end of run_id_results to check the pass-fail ration of your policy
            run_id_results.append(
                (run_id, cumulative_reward / (request_number + 1), num_suc, cumulative_reward / num_suc))
            print("avg per runid: ")
            print(run_id_results)

    pass


if __name__ == "__main__":
    run_id = 5000
    if len(sys.argv) > 1:
        run_id = int(sys.argv[1])
    show_us_what_you_got(run_id, run_id + 1)


# main method. show them what you got
#                    ___
#                . -^   `--,
#               /# =========`-_
#              /# (--====___====\
#             /#   .- --.  . --.|
#            /##   |  * ) (   * ),
#            |##   \    /\ \   / |
#            |###   ---   \ ---  |
#            |####      ___)    #|
#            |######           ##|
#             \#####    ____    /
#              \####   /    \  (
#               `\###  |    |  |
#                 \### \____/  |
#                  \##        |
#                   \###.    .)
#                    `======/
