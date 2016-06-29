import numpy as np

from variables import HEADERS, LANGUAGES, AD_TYPES, COLORS


# used in do_beta() to choose a page
def select_page(page_item, header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass,
                color_fail, price_pass, price_fail, min_price, max_price):
    n = []
    if page_item == "header":
        n = np.random.beta(header_pass['5'], header_fail['5']), \
            np.random.beta(header_pass['15'], header_fail['15']), \
            np.random.beta(header_pass['35'], header_fail['35'])

        return HEADERS[np.argmax(n)]
    elif page_item == "language":
        n = np.random.beta(language_pass['NL'], language_fail['NL']), \
            np.random.beta(language_pass['EN'], language_fail['EN']), \
            np.random.beta(language_pass['GE'], language_fail['GE'])

        return LANGUAGES[np.argmax(n)]
    elif page_item == "adtype":
        n = np.random.beta(adtype_pass['skyscraper'], adtype_fail['skyscraper']), \
            np.random.beta(adtype_pass['square'], adtype_fail['square']), \
            np.random.beta(adtype_pass['banner'], adtype_fail['banner'])

        return AD_TYPES[np.argmax(n)]
    elif page_item == "color":
        n = np.random.beta(color_pass['green'], color_fail['green']), \
            np.random.beta(color_pass['blue'], color_fail['blue']), \
            np.random.beta(color_pass['red'], color_fail['red']), \
            np.random.beta(color_pass['black'], color_fail['black']), \
            np.random.beta(color_pass['white'], color_fail['white'])

        return COLORS[np.argmax(n)]
    elif page_item == "price":
        for i in xrange(min_price, max_price):
            n.append(np.random.beta(price_pass[i - min_price], price_fail[i - min_price]))
            # n.append(np.random.beta(price_fail[i-minprice], price_pass[i-minprice]))
        return (np.argmax(n) + min_price) * 1.00


# policy 2: try to find a page that would serve most request nums in a run_id.
def do_beta(header_pass, header_fail, language_pass, language_fail, adtype_pass, adtype_fail, color_pass, color_fail,
            price_pass, price_fail, min_price, max_price):
    page = {'header': select_page("header", header_pass, header_fail, language_pass, language_fail, adtype_pass,
                                  adtype_fail, color_pass, color_fail, price_pass, price_fail, min_price, max_price),
            'language': select_page("language", header_pass, header_fail, language_pass, language_fail, adtype_pass,
                                    adtype_fail, color_pass, color_fail, price_pass, price_fail, min_price, max_price),
            'adtype': select_page("adtype", header_pass, header_fail, language_pass, language_fail, adtype_pass,
                                  adtype_fail, color_pass, color_fail, price_pass, price_fail, min_price, max_price),
            'color': select_page("color", header_pass, header_fail, language_pass, language_fail, adtype_pass,
                                 adtype_fail, color_pass, color_fail, price_pass, price_fail, min_price, max_price),
            'price': select_page("price", header_pass, header_fail, language_pass, language_fail, adtype_pass,
                                 adtype_fail, color_pass, color_fail, price_pass, price_fail, min_price, max_price)}
    return page
