import time
from multiprocessing import Pool
import json
from sites import *

# 7.22084s - one card
def top_cards_from_each(card_name):
    all_cards = list()
    cardshop = get_cardshop_tolaria(card_name)
    if len(cardshop) != 0:
        all_cards.append(sorted(cardshop, key=lambda i: i['price'])[0])
    sentry = get_sentry_box(card_name)
    if len(sentry) != 0:
        all_cards.append(sorted(sentry, key=lambda i: i['price'])[0])
    face = get_face_to_face(card_name)
    if len(face) != 0:
        all_cards.append(sorted(face, key=lambda i: i['price'])[0])
    er = get_er_games(card_name)
    if len(er) != 0:
        all_cards.append(sorted(er, key=lambda i: i['price'])[0])
    wizard = get_wizard_tower(card_name)
    if len(wizard) != 0:
        all_cards.append(sorted(wizard, key=lambda i: i['price'])[0])
    kessel = get_kessel_run_games(card_name)
    if len(kessel) != 0:
        all_cards.append(sorted(kessel, key=lambda i: i['price'])[0])
    all_cards = sorted(all_cards, key=lambda i: i['price'])
    return all_cards

def top_card_thread_method(func, card_name):
    results = []
    result = func(card_name)
    if len(result) != 0:
        results.append(sorted(result, key=lambda i: i['price'])[0])
    return results

# 2.940s
def top_cards_from_each_multi(card_name):
    store_list = [get_cardshop_tolaria, get_sentry_box, get_face_to_face, get_er_games, get_wizard_tower, get_kessel_run_games]
    all_cards = list()
    with Pool(processes=4) as pool:
        multiple_results = [pool.apply_async(top_card_thread_method, (store, card_name)) for store in store_list]
        for result in multiple_results:
            try:
                all_cards += result.get(timeout=10)
            except TimeoutError:
                print("We lacked patience and got a multiprocessing.TimeoutError")
    all_cards = sorted(all_cards, key=lambda i: i['price'])
    return all_cards

def read_card_list(file_name):
    f = open(file_name, "r")
    str = f.read()
    return str.split('\n')

def write_results(file_name, cards):
    f = open(file_name, "a")
    for options in cards:
        for option in options:
            f.write(str(option['price']) + "," + option['link'] + ",")
        f.write("\n")
    f.close()
    return

def write_optimal_results(file_name, cards):
    f = open(file_name, "a")
    for card in cards:
        f.write(card['name'] + "," + str(card['price']) + "," + card['link'] + ",")
        f.write("\n")
    f.close()
    return


def process_optimal_price(cards):
    calgary_list = ["cardshop", "sentry", "er"]
    sorted_cards = sorted(cards, key=lambda i: i[0]['store'])
    best_list = list()
    for card in sorted_cards:
        # if the best price is in Calgary, leave it at that or if it's the only place to get the card.
        if card[0]["store"] in calgary_list or len(card[0]) == 1:
            best_list.append(card[0])
            continue

        for i in range(len(card)):
            if i == 0:
                continue
            if card[i]["store"] in calgary_list and card[i]["price"]-card[0]["price"] <= 0.01:
                best_list.append(card[i])
                break
        best_list.append(card[0])
    return best_list

if __name__ == '__main__':
    # Cards List Regex for Archidekt: \((.*) And 1x
    # Possible other store addition: https://www.ebay.ca/str/4thdimensiongames
    file = "cards_list.txt"
    card_list = read_card_list(file)
    # card_list = ["Balduvian Bears"]
    final_list = list()
    for card in card_list:
        final_list.append(top_cards_from_each(card))
        # final_list.append(top_cards_from_each_multi(card))

    # for item in final_list:
    #     print(item)
    # optimal_prices = process_optimal_price(final_list)
    # write_optimal_results("found_cards.csv", optimal_prices)

    write_results("found_cards.csv", final_list)

    # 526.794s - Non-threaded
    # 143.513s - Threaded
