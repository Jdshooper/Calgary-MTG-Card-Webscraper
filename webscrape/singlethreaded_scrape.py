from webscrape.sites import *

def top_cards_from_each(card_name):
    all_cards = list()
    store_list = [get_sentry_box, get_face_to_face, get_er_games, get_wizard_tower, get_kessel_run_games, get_four_o_one]
    for store in store_list:
        cards = store(card_name)
        if len(cards) != 0:
            all_cards.append(sorted(cards, key=lambda i: i['price'])[0])
    all_cards = sorted(all_cards, key=lambda i: i['price'])
    return all_cards
