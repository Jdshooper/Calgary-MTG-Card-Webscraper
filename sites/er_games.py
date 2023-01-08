from bs4 import BeautifulSoup
import requests

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
