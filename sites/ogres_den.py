import requests
import re

def get_ogres_den(card_name):
    url = "https://lusearchapi-na.hawksearch.com/sites/starcitygames/?card_name=" + card_name.replace(" ", "%20") + "&ajax=1&json=1&hawkcustom=undefined&hawkvisitorid=1b87d6c5-0cdc-4799-b86d-48d534a6e8f4&callback=jQuery3600791277535178662_1673361209207&_=1673361209208"
    js = requests.get(url).text
    ids = re.findall(r"hawkProductNotify\(\'([\d]*)", js)
    response = requests.get("https://ajax.starcitygames.com/getDiscrepancies/" + ",".join(ids))
    results = response.json().values()
    cards = []
    # WIP
    # for result in results:
        # print(result.keys())
        # cards.append({
        #     "name": card_name,
        #     "store": "face",
        #     "stock": stock,
        #     "link": "https://www.facebook.com/ogresdengamingclub/",
        #     "price": price
        # })
    return cards
