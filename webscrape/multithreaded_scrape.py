from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from webscrape.sites import *

def top_card_thread_method(func, card_name):
    results = []
    result = func(card_name)
    if len(result) != 0:
        results.append(sorted(result, key=lambda i: i['price'])[0])
    return results

def top_cards_from_each_multi(card_name):
    store_list = [get_sentry_box, get_face_to_face, get_er_games, get_wizard_tower, get_kessel_run_games, get_four_o_one]
    all_cards = list()
    with ThreadPool(processes=cpu_count()) as pool:
        multiple_results = [pool.apply_async(top_card_thread_method, (store, card_name)) for store in store_list]
        for result in multiple_results:
            try:
                all_cards += result.get(timeout=10)
            except TimeoutError:
                print("We lacked patience and got a multiprocessing.TimeoutError")
    all_cards = sorted(all_cards, key=lambda i: i['price'])
    return all_cards
