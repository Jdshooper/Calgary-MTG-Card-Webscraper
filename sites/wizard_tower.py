from bs4 import BeautifulSoup
import requests

def get_wizard_tower(card_name):
    url = "https://www.kanatacg.com/products/search?query=" + card_name.replace(" ", "+")
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.find_all("table", {"class": "invisible-table"})
    results = []
    if tables:
        results = tables[0].find_all("tr")
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
