import sys
import numpy as np
sys.path.append('../')
import collections
from random import randint
import time
import csv


from aiws import api
api.authenticate('billy-the-kid','f2d38030ad785607cb697a1e31150a41')

minprice, maxprice = 20,50

#store how many times something has been chosen with success and how many times with failure
#header_pass = {'5': 1, '15': 1, '35': 1}
#header_fail = {'5': 1, '15': 1, '35': 1}
#language_pass = {'NL': 1, 'EN': 1, 'GE': 1}
#language_fail = {'NL': 1, 'EN': 1, 'GE': 1}
#adtype_pass = {'skyscraper': 1, 'square': 1, 'banner': 1}
#adtype_fail = {'skyscraper': 1, 'square': 1, 'banner': 1}
#color_pass = {'green': 1, 'blue': 1, 'red': 1, 'black': 1, 'white': 1}
#color_fail = {'green': 1, 'blue': 1, 'red': 1, 'black': 1, 'white': 1}
#price_pass = []
#price_fail = []
#for i in xrange(minprice, maxprice):
#    price_pass.append(1)
#    price_fail.append(1)


def reset_counts(hp, hf, lp, lf, ap, af, cp, cf, pp, pf ):
    hp = {'5': 1, '15': 1, '35': 1}
    hf = {'5': 1, '15': 1, '35': 1}
    lp = {'NL': 1, 'EN': 1, 'GE': 1}
    lf = {'NL': 1, 'EN': 1, 'GE': 1}
    ap = {'skyscraper': 1, 'square': 1, 'banner': 1}
    af = {'skyscraper': 1, 'square': 1, 'banner': 1}
    cp = {'green': 1, 'blue': 1, 'red': 1, 'black': 1, 'white': 1}
    cf = {'green': 1, 'blue': 1, 'red': 1, 'black': 1, 'white': 1}
    pp = []
    pf = []
    for i in xrange(minprice, maxprice):
        pp.append(1)
        pf.append(1)
    pass


# update counts on the page serve items
def update_counts(name, item):
    # print("update before: " + str(name)+" "+str(item))
    name[item] += 1
    # print("update after: " + str(name)+" "+str(item))
    pass


def update_counts_price(name, item):
    # print("update before: " + str(name)+" "+str(item))
    ind = int(item-minprice)
    name[ind] += 1
    # print("update after: " + str(name)+" "+str(item))
    pass

def select_policy(page_item, header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail):
    n = []
    if page_item == "header":
        n = np.random.beta(header_pass['5'], header_fail['5']),np.random.beta(header_pass['15'], header_fail['15']), np.random.beta(header_pass['35'], header_fail['35'])
        # n = np.random.beta(header_fail['5'], header_pass['5']),np.random.beta(header_fail['15'], header_pass['15']), np.random.beta(header_fail['35'], header_pass['35'])
        ind = n.index(max(n))
        i = 0
        for item in header_pass:
            if i == ind:
                return item
            i += 1
    elif page_item == "language":
        # n = np.random.beta(language_pass['NL'], language_fail['NL']),np.random.beta(language_pass['EN'], language_fail['EN']), np.random.beta(language_pass['GE'], language_fail['GE'])
        n = np.random.beta(language_fail['NL'], language_pass['NL']),np.random.beta(language_fail['EN'], language_pass['EN']), np.random.beta(language_fail['GE'], language_pass['GE'])
        ind = n.index(max(n))
        i = 0
        for item in language_pass:
            if i == ind:
                return item
            i += 1
    elif page_item == "adtype":
        n = np.random.beta(adtype_pass['skyscraper'], adtype_fail['skyscraper']),np.random.beta(adtype_pass['square'], adtype_fail['square']), np.random.beta(adtype_pass['banner'], adtype_fail['banner'])
        # n = np.random.beta(adtype_fail['skyscraper'], adtype_pass['skyscraper']),np.random.beta(adtype_fail['square'], adtype_pass['square']), np.random.beta(adtype_fail['banner'], adtype_pass['banner'])
        ind = n.index(max(n))
        i = 0
        for item in adtype_pass:
            if i == ind:
                return item
            i += 1
    elif page_item == "color":
        n = np.random.beta(color_pass['green'], color_fail['green']),np.random.beta(color_pass['blue'], color_fail['blue']), np.random.beta(color_pass['red'], color_fail['red']), np.random.beta(color_pass['black'], color_fail['black']), np.random.beta(color_pass['white'], color_fail['white'])
        # n = np.random.beta(color_fail['green'], color_pass['green']),np.random.beta(color_fail['blue'], color_pass['blue']), np.random.beta(color_fail['red'], color_pass['red']), np.random.beta(color_fail['black'], color_pass['black']), np.random.beta(color_fail['white'], color_pass['white'])
        ind = n.index(max(n))
        i = 0
        for item in color_pass:
            if i == ind:
                return item
            i += 1
    elif page_item == "price":
        for i in xrange(minprice, maxprice):
            n.append(np.random.beta(price_pass[i-minprice], price_fail[i-minprice]))
            # n.append(np.random.beta(price_fail[i-minprice], price_pass[i-minprice]))
        return (n.index(max(n))+minprice) * 1.00
    pass



#store a policy and context
def store_policy(context, context_vector, offer_vector, tmp_offer_vector):
###{{{
    context_vector['visitor_id'].append(context['context']['visitor_id'])
    context_vector['agent'].append(context['context']['agent'])
    context_vector['os'].append(context['context']['os'])
    context_vector['language'].append(context['context']['language'])
    context_vector['age'].append(context['context']['age'])
    context_vector['referrer'].append(context['context']['referrer'])
    offer_vector['header'].append(tmp_offer_vector['header'])
    offer_vector['language'].append(tmp_offer_vector['language'])
    offer_vector['adtype'].append(tmp_offer_vector['adtype'])
    offer_vector['color'].append(tmp_offer_vector['color'])
    offer_vector['price'].append(tmp_offer_vector['price'])
    # offer_vector['header'].append(offer_header)
    # offer_vector['language'].append(offer_language)
    # offer_vector['adtype'].append(offer_adtype)
    # offer_vector['color'].append(offer_color)
    # offer_vector['price'].append(offer_price)
    pass
###}}}


def store_policy_only(offer_vector, tmp_offer_vector):
###{{{
    offer_vector['header'].append(tmp_offer_vector['header'])
    offer_vector['language'].append(tmp_offer_vector['language'])
    offer_vector['adtype'].append(tmp_offer_vector['adtype'])
    offer_vector['color'].append(tmp_offer_vector['color'])
    offer_vector['price'].append(tmp_offer_vector['price'])
    # print("policy stored")
    pass
###}}}


#compare with known contexts, find most similar context with highest price and take the offer
def find_policy(context, context_vector, offer_vector):
###{{{
    # simscore = 0
    vecindex = 0
    maxprice = -100
    tmp = 0
    tmp_context_vector = {'visitor_id': context['context']['visitor_id'],
                          'agent': context['context']['agent'],
                          'os': context['context']['os'],
                          'language': context['context']['language'],
                          'age': context['context']['age'],
                          'referrer': context['context']['referrer']}

    for x in xrange(0,len(context_vector['age'])):
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
        # if tmp > simscore and tmpprice > maxprice:
            # simscore = tmp
            # vecindex = x
            # maxprice = offer_vector['price'][x]

    policy = {'header': offer_vector['header'][vecindex],
              'language': offer_vector['language'][vecindex],
              'adtype': offer_vector['adtype'][vecindex],
              'color': offer_vector['color'][vecindex],
              'price': offer_vector['price'][vecindex]}
    return policy
    pass
###}}}


# price_min = minimum price, price_max= maximum price, rand_trials=number of random trials, lang_def=set language to context language
def train_it(price_min, price_max, rand_trials, lang_def, run_id, iters, offer_vector, context_vector, cumulative_reward, n):
###{{{
    k = rand_trials*10000
    for request_number in xrange(n):

        print "iters=" + str(iters) + " run_id=" + str(run_id) + " request_number=" + str(request_number)
        if iters < k:
            print("successful policies: " + str(len(offer_vector['price'])))
            # print(str(offer_vector['price']))
            if len(offer_vector['price']) > 1:
                print("avg successful price: "+str(sum(offer_vector['price'])/len(offer_vector['price'])))

            context = api.get_context(run_id, request_number)

            if lang_def:
                #some heuristics
                if context['context']['language'] == 'Other':
                    offer_language = 'EN'
                else:
                    offer_language = context['context']['language']
            else:
                all_lang = ['EN','NL','GE']
                offer_language = all_lang[randint(0,2)]

            all_adtypes = ['banner', 'skyscraper','square']
            offer_adtype = all_adtypes[randint(0,2)]
            all_header = [5,15,35]
            offer_header = all_header[randint(0,2)]
            pos_clr = ['green', 'blue', 'red', 'black', 'white']
            offer_color = pos_clr[randint(0,4)]
            offer_price = randint(price_min, price_max) * 1.00

            result = api.serve_page(run_id, request_number,
                                    header=offer_header,
                                    language=offer_language,
                                    adtype=offer_adtype,
                                    color=offer_color,
                                    price=offer_price)
            cumulative_reward += offer_price * result['success']
            mean_reward = cumulative_reward / n
            print "Mean reward: %.2f euro" % mean_reward

            if result['success']:
                context_vector['visitor_id'].append(context['context']['visitor_id'])
                context_vector['agent'].append(context['context']['agent'])
                context_vector['os'].append(context['context']['os'])
                context_vector['language'].append(context['context']['language'])
                context_vector['age'].append(context['context']['age'])
                context_vector['referrer'].append(context['context']['referrer'])
                offer_vector['header'].append(offer_header)
                offer_vector['language'].append(offer_language)
                offer_vector['adtype'].append(offer_adtype)
                offer_vector['color'].append(offer_color)
                offer_vector['price'].append(offer_price)

            iters += 1
        #endif
        else:
            policy = find_policy(context, context_vector, offer_vector)
            result = api.serve_page(run_id, request_number,
                                    header=policy['header'],
                                    language=policy['language'],
                                    adtype=policy['adtype'],
                                    color=policy['color'],
                                    price=policy['price'])
            cumulative_reward += policy['price'] * result['success']
            mean_reward = cumulative_reward / n
            print "Mean reward: %.2f euro" % mean_reward
    pass
###}}}


def adjust_price(suc_price, dif_pl, dif_su):
###{{{
    avg_price = np.ceil(sum(suc_price)/len(suc_price))
    if avg_price-dif_su < 0:
        min_price = 0
    else:
        min_price = avg_price - dif_su
    if avg_price+dif_pl > 50:
        max_price = 50
    else:
        max_price = avg_price + dif_pl
    return min_price, max_price
    pass
###}}}


def run_stuff_1(run_id, request_number, all_adtypes, all_header, all_clr, all_lang, min_price, max_price, cumulative_reward, n, suc_price, success, context_vector, offer_vector, avg_suc_price):
###{{{
    tstart = time.clock()
    context = api.get_context(run_id, request_number)
    offer_adtype = all_adtypes[randint(0,2)]
    offer_header = all_header[randint(0,2)]
    offer_color = all_clr[randint(0,4)]
    offer_language = all_lang[randint(0,2)]
    offer_price = randint(min_price, max_price) * 1.00

    result = api.serve_page(run_id, request_number,
                            header=offer_header,
                            language=offer_language,
                            adtype=offer_adtype,
                            color=offer_color,
                            price=offer_price)
    tstop = time.clock()
    ttime = tstop - tstart
    cumulative_reward += offer_price * result['success']
    # print(cumulative_reward)
    # mean_reward = cumulative_reward / n
    # print "Mean reward: %.2f euro" % mean_reward

    if result['success']:
        tmp_offer_vector = {'header': offer_header,
                        'language': offer_language,
                        'adtype': offer_adtype,
                        'color': offer_color,
                        'price': offer_price}
        store_policy(context, context_vector, offer_vector, tmp_offer_vector)
        suc_price.append(offer_price)
        success += 1
        avg_suc_price.append(cumulative_reward / success)
        # print("price= "+str(offer_price))
    #endif
    if success == 0:
        sss = 1
    else:
        sss = success
    print("run_id="+str(run_id)+" request_number="+str(request_number)+" mean_reward="+str(cumulative_reward/(request_number+1))+" min, max="+str(min_price)+","+str(max_price)+" success rate="+str(success)+":"+str(request_number)+" avg_succes_price:"+str(cumulative_reward/sss))
    return success, ttime, cumulative_reward, avg_suc_price
    pass
###}}}


def run_stuff_2(run_id, request_number, all_adtypes, all_header, all_clr, all_lang, min_price, max_price, cumulative_reward, n, context_vector, offer_vector, success, avg_suc_price):
###{{{
    tstart = time.clock()
    context = api.get_context(run_id, request_number)
    offer_adtype = all_adtypes[randint(0,2)]
    offer_header = all_header[randint(0,2)]
    offer_color = all_clr[randint(0,4)]
    offer_language = all_lang[randint(0,2)]
    offer_price = randint(min_price, max_price) * 1.00

    result = api.serve_page(run_id, request_number,
                            header=offer_header,
                            language=offer_language,
                            adtype=offer_adtype,
                            color=offer_color,
                            price=offer_price)
    tstop = time.clock()
    ttime = tstop - tstart
    cumulative_reward += offer_price * result['success']
    # print(cumulative_reward)
    # mean_reward = cumulative_reward / n
    # print "Mean reward: %.2f euro" % mean_reward

    if result['success']:
        tmp_offer_vector = {'header': offer_header,
                        'language': offer_language,
                        'adtype': offer_adtype,
                        'color': offer_color,
                        'price': offer_price}
        store_policy(context, context_vector, offer_vector, tmp_offer_vector)
        success += 1
        avg_suc_price.append(cumulative_reward / success)
        # print("price= "+str(offer_price))
    #endif
    if success == 0:
        sss = 1
    else:
        sss = success
    print("run_id="+str(run_id)+" request_number="+str(request_number)+" mean_reward="+str(cumulative_reward/(request_number+1))+" min, max="+str(min_price)+","+str(max_price)+" success rate="+str(success)+":"+str(request_number)+" avg_succes_price:"+str(cumulative_reward/sss))
    return len(offer_vector['price']), success, ttime, cumulative_reward, avg_suc_price
    pass
###}}}


def run_each_n_times(run_id, request_number, n, offer_vector, suc_pols, big_offer_vector):
    # print("...enter run_each_n_times...")

    context = api.get_context(run_id, request_number)

    for it in xrange(n):
        offer = {
            'header': [5, 15, 35],
            'language': ['NL', 'EN', 'GE'],
            'adtype': ['skyscraper', 'square', 'banner'],
            'color': ['green', 'blue', 'red', 'black', 'white'],
            'price': [randint(20, 50)*1.00]
            # 'price': map(lambda x: 1+float(x)/10.,range(490))
        }
        # Random choice
        offer = {key: np.random.choice(val) for key, val in offer.iteritems()}

        result = api.serve_page(run_id, request_number,
            header=offer['header'],
            language=offer['language'],
            adtype=offer['adtype'],
            color=offer['color'],
            price=offer['price'])

        tmp_offer_vector = {'header': offer['header'],
                        'language': offer['language'],
                        'adtype': offer['adtype'],
                        'color': offer['color'],
                        'price': offer['price']}
        # print("tmp_offer_vector=")
        # print(tmp_offer_vector)
        store_policy_only(offer_vector, tmp_offer_vector)
        suc_pols[it] = result['success']

    #endfor
    policy = {'header': offer_vector['header'][0],
              'language': offer_vector['language'][0],
              'adtype': offer_vector['adtype'][0],
              'color': offer_vector['color'][0],
              'price': offer_vector['price'][0]}
    suc = []
    maxprice = 0
    for i in xrange(n):
        if suc_pols[i]: #if success
            suc.append(i)
    #endif
    if not suc: #if list is empty
        # print("failure: no known or generated successful policy")
        # print("len suc="+str(len(suc)))
        # print("policy=")
        # print(policy)
        return policy
    else:
        # print("len suc="+str(len(suc)))
        for i in xrange(len(suc)):
            if offer_vector['price'][i] >= maxprice:
                maxprice = offer_vector['price'][i]
                policy = {'header': offer_vector['header'][i],
                          'language': offer_vector['language'][i],
                          'adtype': offer_vector['adtype'][i],
                          'color': offer_vector['color'][i],
                          'price': offer_vector['price'][i]}
            #endif
        #endfor
        store_policy_only(big_offer_vector, policy)
    #endif

    # print("policy=")
    # print(policy)
    # print("...exit run_each_n_times...")
    return policy
    pass


def train_it_smart(cumulative_reward, run_id, context_vector, offer_vector, success, avg_suc_price):
###{{{
    max_price = 50
    min_price = 20
    # n = 10000
    n = 0
    all_adtypes = ['banner', 'skyscraper','square']
    all_lang = ['EN','NL','GE']
    all_header = [5,15,35]
    all_clr = ['green', 'blue', 'red', 'black', 'white']

    suc_price = []
    total_serve_time = []
    total_suc_price = []
    request_number = 0


    #adjust prices
    for request_number in xrange(0,100):
        success, ttime, cumulative_reward, avg_suc_price  = run_stuff_1(run_id, request_number, all_adtypes, all_header, all_clr, all_lang, min_price, max_price, cumulative_reward, n, suc_price, success, context_vector, offer_vector, avg_suc_price)
        n += 1
        total_serve_time.append(ttime)

    min_price, max_price = adjust_price(suc_price, 5, 0)
    suc_price = []

    for request_number in xrange(100, 200):
        success, ttime, cumulative_reward, avg_suc_price = run_stuff_1(run_id, request_number, all_adtypes, all_header, all_clr, all_lang, min_price, max_price, cumulative_reward, n, suc_price, success, context_vector, offer_vector, avg_suc_price)
        n += 1
        total_serve_time.append(ttime)
    min_price, max_price = adjust_price(suc_price, 3, 0)
    suc_price = []

    for request_number in xrange(200, 300):
        success, ttime, cumulative_reward, avg_suc_price = run_stuff_1(run_id, request_number, all_adtypes, all_header, all_clr, all_lang, min_price, max_price, cumulative_reward, n, suc_price, success, context_vector, offer_vector, avg_suc_price)
        n += 1
        total_serve_time.append(ttime)
    min_price, max_price = adjust_price(suc_price, 1, 0)
    #gather successful policies
    request_number = 300
    suc_pols = 0
    while suc_pols < 201:
        suc_pols, success, ttime, cumulative_reward, avg_suc_price = run_stuff_2(run_id, request_number, all_adtypes, all_header, all_clr, all_lang, min_price, max_price, cumulative_reward, n, context_vector, offer_vector, success, avg_suc_price)
        request_number += 1
        n += 1
        total_serve_time.append(ttime)
    #endwhile

    beg = request_number + 1
    for request_number in xrange(beg, 10000):
    # for request_number in xrange(beg, 2000):
        context = api.get_context(run_id, request_number)
        tstart = time.clock()
        policy = find_policy(context, context_vector, offer_vector)
        result = api.serve_page(run_id, request_number,
                                header=policy['header'],
                                language=policy['language'],
                                adtype=policy['adtype'],
                                color=policy['color'],
                                price=policy['price'])
        tstop = time.clock()
        ttime = tstop - tstart
        total_serve_time.append(ttime)
        cumulative_reward += policy['price'] * result['success']
        print(cumulative_reward)
        if result['success']:
            success += 1
            avg_suc_price.append(cumulative_reward / success)

            # print("price= "+str(policy['price']))
        print("run_id="+str(run_id)+" request_number="+str(request_number)+" mean_reward="+str(cumulative_reward/request_number)+" min, max="+str(min_price)+","+str(max_price)+" success rate="+str(success)+":"+str(request_number)+" avg_succes_price:"+str(cumulative_reward/success))
        n += 1
        # mean_reward = cumulative_reward / n
        # print "Mean reward: %.2f euro" % mean_reward
    #endfor
    mean_reward = cumulative_reward / n
    print "Mean reward: %.2f euro" % mean_reward
    return success, cumulative_reward, total_serve_time, avg_suc_price
    pass
###}}}


def try_all_suc_policies(all_policies, run_id, request_number):
    # print("...enter try_all_suc_policies...")
    policy = {'header': [],
                'language': [],
                'adtype': [],
                'color': [],
                'price': []}
    ind = len(all_policies['price'])
    offer_vector = {'header': [],
                'language': [],
                'adtype': [],
                'color': [],
                'price': []}

    for i in xrange(ind):
        result = api.serve_page(run_id, request_number,
                                header=all_policies['header'][i],
                                language=all_policies['language'][i],
                                adtype=all_policies['adtype'][i],
                                color=all_policies['color'][i],
                                price=all_policies['price'][i])
        if result['success']:
            tmp_offer_vector = {'header': all_policies['header'][i],
                            'language': all_policies['language'][i],
                            'adtype': all_policies['adtype'][i],
                            'color': all_policies['color'][i],
                            'price': all_policies['price'][i]}
            store_policy_only(offer_vector, tmp_offer_vector)

    #endfor
    if len(offer_vector['price'])>0:
        # print("--> we have a successful policy stored")
        maxprice = 0
        for i in xrange(len(offer_vector['price'])):
            if offer_vector['price'][i] >= maxprice:
                maxprice = offer_vector['price'][i]
                policy = {'header': offer_vector['header'][i],
                          'language': offer_vector['language'][i],
                          'adtype': offer_vector['adtype'][i],
                          'color': offer_vector['color'][i],
                          'price': offer_vector['price'][i]}
                # print("stored successful policy found")
            #endif
        #endfor
    #endif
    # print("...exit try_all_suc_policies...")
    return policy
    pass

#"combination of 2 and 4"
def test_gabi_5():

    pass


#"thompson sampling"
def test_gabi_4():
    policy_blank = {'header': [],
                    'language': [],
                    'adtype': [],
                    'color': [],
                    'price': []}
    #summary: avg score, success, price
    avg_runid = []

    #for run_id in xrange(5000, 5010):
    for run_id in xrange(0, 10):
        cumulative_reward = 0
        num_suc = 0
        req_nums = 10000
        #store how many times something has been chosen with success and how many times with failure
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
        for i in xrange(minprice, maxprice):
            price_pass.append(1)
            price_fail.append(1)



        #reset_counts(header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)
        for request_number in xrange(req_nums):
            policy = {'header': [select_policy("header", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)],
                        'language': [select_policy("language", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)],
                        'adtype': [select_policy("adtype", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)],
                        'color': [select_policy("color", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)],
                        'price': [select_policy("price", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)]}
            # print policy
            result = api.serve_page(run_id, request_number,
                                    header=policy['header'],
                                    language=policy['language'],
                                    adtype=policy['adtype'],
                                    color=policy['color'],
                                    price=policy['price'])
            cumulative_reward += policy['price'][0] * result['success']

            if result['success']:
                # print("SUCCESS")
                update_counts(header_pass, policy['header'][0])
                update_counts(language_pass, policy['language'][0])
                update_counts(adtype_pass, policy['adtype'][0])
                update_counts(color_pass, policy['color'][0])
                update_counts_price(price_pass, policy['price'][0])
                num_suc += 1
            else:
                # print("FAILURE")
                update_counts(header_fail, policy['header'][0])
                update_counts(language_fail, policy['language'][0])
                update_counts(adtype_fail, policy['adtype'][0])
                update_counts(color_fail, policy['color'][0])
                update_counts_price(price_fail, policy['price'][0])

            print("run_id="+str(run_id)+" request_number="+str(request_number)+" mean_reward="+str(cumulative_reward/req_nums)+" success rate="+str(num_suc)+":"+str(request_number))

        avg_runid.append((run_id, cumulative_reward/req_nums, num_suc, cumulative_reward/num_suc))
        print("avg per runid: ")
        print(avg_runid)

    pass

#"cheating"
def test_gabi_3():
    policy_blank = {'header': [],
                'language': [],
                'adtype': [],
                'color': [],
                'price': []}
    n = 10
    for run_id in xrange(5000, 5010):
        testids = 10000
        cumulative_reward = 0
        # big_context_vector = {'visitor_id': [],
                          # 'agent': [],
                          # 'os': [],
                          # 'language': [],
                          # 'age': [],
                          # 'referrer': []}
        big_offer_vector = {'header': [],
                        'language': [],
                        'adtype': [],
                        'color': [],
                        'price': []}

        for request_number in xrange(testids):
            policy = {'header': [],
                        'language': [],
                        'adtype': [],
                        'color': [],
                        'price': []}
            #first test all successful policies
            if len(big_offer_vector['price'])>0:
                # print("...checking all stored successful policies")
                policy = try_all_suc_policies(big_offer_vector, run_id, request_number) #not a vector lol
                # print("---policy 1")
                # print(policy)
            #endif
            if policy == policy_blank: #no successful policies for this context
                # print("--> we found no successful policies in storage")
                #if none of them return success, try the new ones
                suc_pols = [0]*n
                # context_vector = {'visitor_id': [],
                                  # 'agent': [],
                                  # 'os': [],
                                  # 'language': [],
                                  # 'age': [],
                                  # 'referrer': []}
                offer_vector = {'header': [],
                                'language': [],
                                'adtype': [],
                                'color': [],
                                'price': []}
                policy = run_each_n_times(run_id, request_number, n, offer_vector, suc_pols, big_offer_vector)
            #endif
            result = api.serve_page(run_id, request_number,
                                    header=policy['header'],
                                    language=policy['language'],
                                    adtype=policy['adtype'],
                                    color=policy['color'],
                                    price=policy['price'])
            # print("---policy 2")
            # print(policy)
            cumulative_reward += policy['price'] * result['success']
            print("run_id="+str(run_id)+" request_number="+str(request_number)+" mean_reward="+str(cumulative_reward/testids)+" big off vec="+str(len(big_offer_vector['price'])))
            # print("given policy=")
            # print(policy)
            # print("success="+str(result['success']))

        #endfor

    #endfor
    pass

#"similarity"
def test_gabi_2():
###{{{

    avg_runid = []
    # for run_id in xrange(0, 10):
    for run_id in xrange(5000, 5010):
        # iters = 0
        context_vector = {'visitor_id': [],
                          'agent': [],
                          'os': [],
                          'language': [],
                          'age': [],
                          'referrer': []}
        offer_vector = {'header': [],
                        'language': [],
                        'adtype': [],
                        'color': [],
                        'price': []}
        cumulative_reward = 0
        # success = 0
        avg_suc_price = []

        success, cumulative_reward, tot_time, avg_suc_price = train_it_smart(cumulative_reward, run_id, context_vector, offer_vector, 0, avg_suc_price)

        myfile = open("avg_success_price_"+str(run_id)+".csv", 'wb')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(avg_suc_price)

        avg_runid.append((run_id, cumulative_reward/10000, success, cumulative_reward/success, sum(tot_time)/10000))
        # avg_runid.append((run_id, cumulative_reward/2000, success, cumulative_reward/success, sum(tot_time)/2000))
        print("avg per runid: ")
        print(avg_runid)
    pass
###}}}

#"handcrafted"
def test_gabi():
###{{{
    for run_id in xrange(5000, 5009+1):
        iters = 0
        context_vector = {'visitor_id': [],
                          'agent': [],
                          'os': [],
                          'language': [],
                          'age': [],
                          'referrer': []}
        offer_vector = {'header': [],
                        'language': [],
                        'adtype': [],
                        'color': [],
                        'price': []}
        cumulative_reward = 0
        n = 10000

        supersuck = [5006,5007,5008]
        suck = [5000,5001]
        avg = [5004,5005]
        epic = [5002,5003,5009]

        # for request_number in xrange(n):
        if run_id in epic:
            #price_min, price_max, rand_trials, lang_def, request_number, run_id, iters, offer_vector, context_vector):
            train_it(45, 50, 0.2, True, run_id, iters, offer_vector, context_vector, cumulative_reward, n)

        elif run_id in avg:
            train_it(25, 50, 0.25, False, run_id, iters, offer_vector, context_vector, cumulative_reward, n)

        elif run_id in suck:
            train_it(10, 40, 0.25, False, run_id, iters, offer_vector, context_vector, cumulative_reward, n)

        elif run_id in supersuck:
            train_it(1, 30, 0.25, False, run_id, iters, offer_vector, context_vector, cumulative_reward, n)
    pass
###}}}


def test_random_requests():
###{{{
    for run_id in xrange(5000,5010):
        #run_id = 0

        cumulative_reward = 0
        n = 10000

        for request_number in xrange(n):
            print(randint(1,50)*1.00)
            print "run_id="+str(run_id)+" request_number="+str(request_number)
            context = api.get_context(run_id, request_number)
            #print context['context'].values()
            print context['context']['language']


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

            #print result, offer['price'] * result['success']
            cumulative_reward += offer['price'] * result['success']

        mean_reward = cumulative_reward / n
        print "Mean reward: %.2f euro" % mean_reward
        pass
###}}}

if __name__ == "__main__":
    #test_random_requests()

    # test_gabi_4()
    #test_gabi_3()
    test_gabi_2()
    # test_gabi()
