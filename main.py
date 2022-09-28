from bs4 import BeautifulSoup
import requests
import time
from multiprocessing import Pool
import json

def get_cardshop_tolaria(card_name):
    url = "https://www.cardshoptolaria.com/product-list?keyword=" + card_name.replace(" ", "+")
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all("div", {"class": "item_data"})
    cards = []
    for result in results:
        if not result.find_all("p", {"class": "stock"}):
            continue
        stock = result.find_all("p", {"class": "stock"})[0].text
        # In stock filter
        if stock == "Not available":
            continue
        # Title check
        title = result.find_all("span", {"class": "goods_name"})[0].text
        if card_name.lower() not in title.lower():
            continue
        if " art " not in card_name.lower() and " art " in title.lower():
            continue

        amount_in_stock = int(stock.split(" ")[1])

        # Get price
        price = float(result.find_all("span", {"class": "figure"})[0].text[2:])

        # Get link
        link = result.a['href']
        cards.append({
            "name": card_name,
            "store": "cardshop",
            "stock": amount_in_stock,
            "link": link,
            "price": price
        })
    return cards

def get_sentry_box(card_name):
    url = "https://sentryboxcards.com/search?s=" + card_name.replace(" ", "+") + "&t=sn"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all("div", {"class": "cardBox"})
    cards = []
    for result in results:
        info = result.find_all("div", {"class": "cbInfo"})[0]

        stock = int(info.find_all("span")[0].text)
        # In stock filter
        if stock == 0:
            continue

        # Get price
        price = float(info.find_all("span")[2].text)

        # Get link
        link = "https://sentryboxcards.com/" + result.a['href']
        cards.append({
            "name": card_name,
            "store": "sentry",
            "stock": stock,
            "link": link,
            "price": price
        })
    return cards

def get_face_to_face(card_name):
    url = "https://www.facetofacegames.com/search.php?search_query=" + card_name.replace(" ", "%20") + "&section=product&_bc_fsnf=1&in_stock=1"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all("li", {"class": "product"})
    cards = []
    for result in results:
        title = result.find_all("h4", {"class": 'card-title'})[0].a
        if card_name.lower() not in title.text.lower():
            continue
        if " art " not in card_name.lower() and " art " in title.text.lower():
            continue
        stock = 0  # result.find_all("div", {"class": "card-stock"}) # == 0
        price = float(result.article['data-product-price'])
        link = title["href"]
        cards.append({
            "name": card_name,
            "store": "face",
            "stock": stock,
            "link": link,
            "price": price
        })
    return cards

def get_er_games(card_name):
    url = "https://ergames.ca/search?q=*" + card_name.replace(" ", "+") + "*"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all("div", {"class": "product Norm"})
    cards = []
    for result in results:
        price = result.find_all("p", {"class": 'productPrice'})[0].text.strip()
        # In stock filter
        if price == "Sold Out":
            continue
        title = result.find_all("p", {"class": 'productTitle'})[0].text
        if card_name.lower() not in title.lower():
            continue
        if " art " not in card_name.lower() and " art " in title.lower():
            continue
        stock = 0
        link = "https://ergames.ca" + result.find_all("a", {"class": 'productLink'})[0]["href"]
        if "aries" in price:
            price = float(result.find_all("div", {"class": 'addNow single'})[0].p.text.split(" ")[-1][1:])
        else:
            price = float(price[1:].split('\n')[0])
        cards.append({
            "name": card_name,
            "store": "er",
            "stock": stock,
            "link": link,
            "price": price
        })
    return cards

def get_kessel_run_games(card_name):
    url = "https://kesselrungames.ca/search?q=*" + card_name.replace(" ", "+") + "*"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all("div", {"class": "product Norm"})
    cards = []
    for result in results:
        price = result.find_all("p", {"class": 'productPrice'})[0].text.strip()
        # In stock filter
        if price == "Sold Out":
            continue
        title = result.find_all("p", {"class": 'productTitle'})[0].text
        if card_name.lower() not in title.lower():
            continue
        if " art " not in card_name.lower() and " art " in title.lower():
            continue

        stock = 0
        link = "https://kesselrungames.ca" + result.find_all("a", {"class": 'productLink'})[0]["href"]
        if "aries" in price:
            price = float(result.find_all("div", {"class": 'addNow single'})[0].p.text.split(" ")[-1][1:])
        else:
            price = float(price[1:].split('\n')[0])
        cards.append({
            "name": card_name,
            "store": "kessel",
            "stock": stock,
            "link": link,
            "price": price
        })
    return cards

def get_wizard_tower(card_name):
    url = "https://www.kanatacg.com/products/search?query=" + card_name.replace(" ", "+")
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all("table", {"class": "invisible-table"})[0].find_all("tr")
    cards = []
    for result in results:
        in_stock_text = result.find_all("td", {"class": "variantInfo"})[0].text
        if "No conditions in stock" in in_stock_text:
            continue
        link_base = result.find_all("td")[1].find_all("a")
        if len(link_base) == 0:
            continue
        title = link_base[0].text
        if card_name.lower() not in title.lower():
            continue
        if " art " not in card_name.lower() and " art " in title.lower():
            continue
        link = "https://www.kanatacg.com" + link_base[0]['href']
        price = float(result.find_all("td", {"width": "13%"})[0].text.split(" ")[1])
        stock = result.find_all("td", {"width": "10%"})[0].text
        cards.append({
            "name": card_name,
            "store": "wizard",
            "stock": stock,
            "link": link,
            "price": price
        })
    return cards

# TODO: add https://store.401games.ca/pages/search-results?q=whim%20of%20volrath&page_num=3
def get_four_o_one(card_name):
    return

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
    # wizard = get_wizard_tower(card_name)
    # if len(wizard) != 0:
    #     all_cards.append(sorted(wizard, key=lambda i: i['price'])[0])
    # kessel = get_kessel_run_games(card_name)
    # if len(kessel) != 0:
    #     all_cards.append(sorted(kessel, key=lambda i: i['price'])[0])
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
