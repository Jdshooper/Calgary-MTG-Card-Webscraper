from bs4 import BeautifulSoup
import requests

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
        stock = 0  # WIP: result.find_all("div", {"class": "card-stock"}) # == 0
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
