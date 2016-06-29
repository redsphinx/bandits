# minimum price and maximum price to be used for all policies
MIN_PRICE, MAX_PRICE = 20, 50
# all the elements options we have for serving a page
AD_TYPES = ['banner', 'skyscraper', 'square']
LANGUAGES = ['EN', 'NL', 'GE']
HEADERS = [5, 15, 35]
COLORS = ['green', 'blue', 'red', 'black', 'white']
# a "nonsense" page serve for use in make_new_page() and do_beta_page()
BLANK = {'header': 500,
         'language': "ENE",
         'adtype': "bannera",
         'color': "reda",
         'price': "120.00"}

