from bs4 import BeautifulSoup
import requests

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
