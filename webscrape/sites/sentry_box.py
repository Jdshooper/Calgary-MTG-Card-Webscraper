from bs4 import BeautifulSoup
import requests

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
