import sys
import numpy as np
sys.path.append('../')
import collections
from random import randint
from aiws import api
api.authenticate('billy-the-kid','f2d38030ad785607cb697a1e31150a41')
minprice, maxprice = 20, 50
all_adtypes = ['banner', 'skyscraper','square']
all_lang = ['EN','NL','GE']
all_header = [5,15,35]
all_clr = ['green', 'blue', 'red', 'black', 'white']
BLANK = {'header': 500,
        'language': "ENE",
        'adtype': "bannera",
        'color': "reda",
        'price': "120.00"}

def update_counts(name, item):
    # print("update before: " + str(name)+" "+str(item))
    name[str(item)] += 1
    # print("update after: " + str(name)+" "+str(item))
    pass

def update_counts_price(name, item):
    # print("update before: " + str(name)+" "+str(item))
    # print(str(item))
    ind = int(item-minprice-1)
    name[ind] += 1
    # print("update after: " + str(name)+" "+str(item))
    pass

def make_storage_for_beta():
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
    return header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail

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

def do_beta(header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail):
    page = {'header': select_policy("header", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail),
              'language': select_policy("language", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail),
              'adtype': select_policy("adtype", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail),
              'color': select_policy("color", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail),
              'price': select_policy("price", header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)}
    return page
    pass

def make_vecs_for_similarity():
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
    return context_vector, offer_vector

    pass

def adjust_price(suc_price, dif_pl, dif_su):
    avg_price = np.ceil(sum(suc_price)/len(suc_price))
    if avg_price-dif_su < minprice:
        min_price = minprice
    else:
        min_price = avg_price - dif_su
    if avg_price+dif_pl > maxprice:
        max_price = maxprice
    else:
        max_price = avg_price + dif_pl
    return min_price, max_price
    pass

#ri = run_id, rn = request_number, mipr=min price, mapr=max price
def bounded_random(mipr, mapr, suc_price):
    page = {'header': all_header[randint(0,2)],
              'language': all_lang[randint(0,2)],
              'adtype': all_adtypes[randint(0,2)],
              'color': all_clr[randint(0,4)],
              'price': randint(mipr, mapr) * 1.00}
    return page, suc_price
    pass

#find page based on similarity
def find_page(context, context_vector, offer_vector, suc_price):
    vecindex = 0 #TODO maybe change this to random?
    vecindex = randint(0, len(context_vector['age']))
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

    page = {'header': offer_vector['header'][vecindex],
              'language': offer_vector['language'][vecindex],
              'adtype': offer_vector['adtype'][vecindex],
              'color': offer_vector['color'][vecindex],
              'price': offer_vector['price'][vecindex]}
    return page, suc_price
    pass

#rn=request_number, suc_pols=successful stored policies
#num_suc=number of successes in total, n=to keep track of where we are
#mipr, mapr=minprice, maxprice
#suc_price=array of successful prices, c=context, cv=contextvector, ov=offervector
def do_similarity(rn, mipr, mapr, suc_price, c, cv, ov):
    f1, f2, f3, f4 = 100, 200, 300, 201
    suc_pols = len(ov['price'])

    if rn < f1 or (rn>f1 and rn<f2) or (rn>f2 and rn<f3) or (rn>f3 and suc_pols<f4):
        page, suc_price = bounded_random(mipr, mapr, suc_price)
        return page, suc_price, mipr, mapr
    elif rn == f1 or rn==f2 or rn==f3:
        dif_su = 1
        dif_pl = 7 - (rn/100) * 2
        # print("dif_pl: "+str(dif_pl))
        mipr, mapr = adjust_price(suc_price, dif_pl, dif_su)
        page, suc_price = bounded_random(mipr, mapr, suc_price)
        suc_price = []
        return page, suc_price, mipr, mapr
    elif rn > f3 and suc_pols > f4-2:
        page, suc_price = find_page(c, cv, ov, suc_price)
        return page, suc_price, mipr, mapr
    else:
        print("BOO")
    pass

#store successful context and page serve
def store_page(context, context_vector, offer_vector, tmp_offer_vector):
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
    return context_vector, offer_vector
    pass

#1p1 is similarity, p2 is beta
def make_new_page(p1, p2, p1pass, p1fail, p2pass, p2fail, p3, p3pass, p3fail):
    # print p1
    # print p2
    if p3 == BLANK:
        p3pass, p3fail = 1, 1
    b1, b2, b3 = np.random.beta(p1pass, p1fail), np.random.beta(p2pass, p2fail), np.random.beta(p3pass, p3fail)
    if p3 == BLANK:
        b3 = 0
    # print("b1, b2: "+str(b1)+" "+str(b2))
    if b1 > b2 and b1 > b3:
        # print("p1 wins")
        return p1, 1
    elif b2 > b1 and b2 > b3:
        # print("p2 wins")
        return p2, 2
    elif b3 > b1 and b3 > b2:
        # print("p2 wins")
        return p3, 3
    pass

#samples from beta distribution, gets pairs of a and b from a list of policies that keeps growing
#ov=offervector, ov_pass=if page got chosen and passed, ov_fail=if page got chosen and failed
def do_beta_page(ov, ov_pass, ov_fail):
    #only choose page this way if we have more than 50 pages stored
    if len(ov["header"]) > 49:
        bets = np.random.beta(ov_pass, ov_fail)
        bets = bets.tolist()
        ind = bets.index(max(bets))
        page = {"header": ov["header"][ind],
                "language": ov["language"][ind],
                "adtype": ov["adtype"][ind],
                "color": ov["color"][ind],
                "price": ov["price"][ind]}
        return page
    else:
        page = BLANK
        return page
    pass

def check_if_page_in_ov(page, ov):
    ind = []
    b = False
    if len(ov["header"]) > 0:
        h, l, a, c, p = page["header"], page["language"], page["adtype"], page["color"], page["price"]
        for i in xrange(len(ov["header"])):
            if ov["header"][i] == h and ov["language"][i] == l and ov["adtype"][i] == a and ov["color"][i] == c and ov["price"][i] == p:
                ind.append(i)
                b = True

    # if ind == []:
    #     print "page not in offer vector"

    return b, ind
    pass

#remove all offers in ov and cv that are below [t]hreshold
def remove_weak_pages(t, ov, cv):
    ind = []
    n = 0
    for i in ov["price"]:
        if i < t:
            ind.append(n)
        n += 1

    for i in ind:
        ov["header"].pop(i)
        ov["language"].pop(i)
        ov["adtype"].pop(i)
        ov["color"].pop(i)
        ov["price"].pop(i)
        cv["visitor_id"].pop(i)
        cv["agent"].pop(i)
        cv["os"].pop(i)
        cv["language"].pop(i)
        cv["age"].pop(i)
        cv["referrer"].pop(i)
    #return the vector with the indices at which to remove the items. need to remove them in
    # the thing that keeps track of pass and fail of p3
    return ind, ov, cv
    pass


def show_us_what_you_got():
    avg_runid = []
    req_nums = 10000

    for run_id in xrange(5000, 5010):
        cumulative_reward = 0
        num_suc = 0
        header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail = make_storage_for_beta()
        context_vector, offer_vector = make_vecs_for_similarity()
        mipr, mapr = minprice, maxprice
        p1pass, p1fail, p2pass, p2fail, p3pass, p3fail = 1, 1, 1, 1, 1, 1
        suc_price = []
        ov_pass, ov_fail = [], []

        for request_number in xrange(0, req_nums):
            context = api.get_context(run_id, request_number)

            page1, suc_price, mipr, mapr = do_similarity(request_number, mipr, mapr, suc_price, context, context_vector, offer_vector)
            page2 = do_beta(header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail, price_pass, price_fail)
            page3 = do_beta_page(offer_vector, ov_pass, ov_fail)

            page, winner = make_new_page(page1, page2, p1pass, p1fail, p2pass, p2fail, page3, p3pass, p3fail)
            # page = page2

            result = api.serve_page(run_id, request_number,
                                    header=page['header'],
                                    language=page['language'],
                                    adtype=page['adtype'],
                                    color=page['color'],
                                    price=page['price'])
            cumulative_reward += page['price'] * result['success']

            if result['success']:
                # print("SUCCESS")
                #update beta counters
                update_counts(header_pass, page['header'])
                update_counts(language_pass, page['language'])
                update_counts(adtype_pass, page['adtype'])
                update_counts(color_pass, page['color'])
                update_counts_price(price_pass, page['price'])
                #update similarity vectors
                # tmp_offer_vector = {'header': page["header"],
                #                     'language': page["language"],
                #                     'adtype': page["adtype"],
                #                     'color': page["color"],
                #                     'price': page["price"]}
                # if winner =! 3 and if the page is not stored then store the success page
                bb, indd = check_if_page_in_ov(page, offer_vector)
                if winner < 3 and not bb:
                    context_vector, offer_vector = store_page(context, context_vector, offer_vector, page)
                    #grow vector as offers get added
                    ov_pass.append(2) # 2 because 1 is if it is an option, +1 because it was already successful once
                    ov_fail.append(1)
                suc_price.append(page["price"])
                b, ind = check_if_page_in_ov(page, offer_vector)
                if b:
                    for i in ind:
                        ov_pass[i] += 1

                #update beta p1 p2 p3
                if winner == 1:
                    p1pass += 1
                elif winner == 2:
                    p2pass += 1
                elif winner == 3:
                    p3pass += 1
                num_suc += 1
            else:
                # print("FAILURE")
                #update beta counters
                update_counts(header_fail, page['header'])
                update_counts(language_fail, page['language'])
                update_counts(adtype_fail, page['adtype'])
                update_counts(color_fail, page['color'])
                update_counts_price(price_fail, page['price'])

                b, ind = check_if_page_in_ov(page, offer_vector)
                if b:
                    for i in ind:
                        ov_fail[i] += 1

                #update beta p1 p2 p3
                if winner == 1:
                    p1fail += 1
                elif winner == 2:
                    p2fail += 1
                elif winner == 3:
                    p3fail += 1

            if len(offer_vector["price"]) > 40:
                indx, offer_vector, context_vector = remove_weak_pages(23, offer_vector, context_vector)
                for ii in indx:
                    thingy = ov_pass.pop(ii)
                    thingy = ov_fail.pop(ii)

            print("run_id="+str(run_id)+" request_number="+str(request_number)+" mean_reward="+str(cumulative_reward/req_nums)+" success rate="+str(num_suc)+":"+str(request_number)+" p1-pf: "+str(p1pass)+","+str(p1fail)+" p2-pf: "+str(p2pass)+","+str(p2fail)+" p3-pf: "+str(p3pass)+","+str(p3fail))
            print("num_suc: "+str(num_suc))
            print("price: " + str(page["price"]))
        #to prevent division by 0
        if num_suc == 0:
            num_suc = 1
        avg_runid.append((run_id, cumulative_reward/req_nums, num_suc, cumulative_reward/num_suc))
        print("avg per runid: ")
        print(avg_runid)

    pass


if __name__ == "__main__":
    show_us_what_you_got()
