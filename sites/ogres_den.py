import requests
import re

def get_ogres_den(card_name):
    url = "https://lusearchapi-na.hawksearch.com/sites/starcitygames/?search_query=" + card_name.replace(" ", "%20") + "&ajax=1&json=1&hawkcustom=undefined&hawkvisitorid=15898d94-97ce-43cc-bc0d-7cfbee1d8219&callback=jQuery36006769074421169514_1675212952555&_=1675212952556"
    print("url = " + url)
    js = requests.get(url).text
    ids = re.findall(r"hawkProductNotify\(\'([\d]*)", js)
    if len(ids) == 0:
        print(card_name + " not found at Ogres Den")
        return [];
    ajax_url = "https://ajax.starcitygames.com/getDiscrepancies/" + ",".join(ids)
    response = requests.get(ajax_url)


    results = response.json().values()
    cards = []
    # WIP
    for result in results:
        card_name = result['name']
        link = "https://starcitygames.com" + result['path']
        for key in result.keys():
            if key.isnumeric():
                card_info = result[key]
                price = card_info['price'] * 1.3 # Convert from USD to CAD
                cards.append({
                    "name": card_name,
                    "store": "ogre",
                    "stock": 'goto https://www.facebook.com/ogresdengamingclub/ to check',
                    "link": link,
                    "price": price
                })
                break; # only need first

    return cards
