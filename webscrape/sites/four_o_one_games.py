import requests
import json

def get_four_o_one(card_name):
    url = "https://api.fastsimon.com/full_text_search?request_source=v-next&src=v-next&UUID=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&uuid=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&store_id=17041809&cdn_cache_key=1673196776&api_type=json&facets_required=1&products_per_page=18&narrow=[[%22In+Stock%22,%22True%22],[%22Category%22,%22Magic:+The+Gathering+Singles%22]]&q=" + card_name.replace(" ", "+") + "&page_num=1&sort_by=relevency&with_product_attributes=true"
    response = requests.get(url)
    results = response.json()['items']
    cards = []
    for result in results:
        title = result['l']
        if card_name.lower() not in title.lower():
            continue
        if " art " not in card_name.lower() and " art " in title.lower():
            continue
        stock = 1
        price = float(result['p'])
        link = "https://store.401games.ca" + result['u']
        cards.append({
            "name": card_name,
            "store": "four",
            "stock": stock,
            "link": link,
            "price": price
        })
    return cards
