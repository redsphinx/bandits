import numpy as np

from variables import BLANK


# samples from beta distribution, gets pairs of a and b from a list of policies that keeps growing
# ov=offervector, ov_pass=if page got chosen and passed, ov_fail=if page got chosen and failed
def do_beta_page(offer_vector, offer_vector_pass, offer_vector_fail):
    # only choose page this way if we have more than 50 pages stored
    if len(offer_vector["header"]) > 49:
        bets = np.random.beta(offer_vector_pass, offer_vector_fail)
        bets = bets.tolist()
        ind = bets.index(max(bets))
        page = {"header": offer_vector["header"][ind],
                "language": offer_vector["language"][ind],
                "adtype": offer_vector["adtype"][ind],
                "color": offer_vector["color"][ind],
                "price": offer_vector["price"][ind]}
        return page
    else:
        page = BLANK
        return page