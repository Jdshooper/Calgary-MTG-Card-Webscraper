from bs4 import BeautifulSoup
import requests

def legacy_webscrape(card_name):
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


def api_call(card_name):
    url = "https://essearchapi-na.hawksearch.com/api/v2/search"
    obj = {"Keyword":card_name,"FacetSelections":{},"ClientGuid":"30c874915d164f71bf6f84f594bf623f","IndexName":"","ClientData":{"VisitorId":"efd4eb8d-d42c-41ca-8c5c-8a3b91ec2c54"}}
    response = requests.post(url, obj)
    cards = []
    
    if "Results" not in response.json():
        return cards
    
    results = response.json()["Results"]
    for result in results:
        info = result["Document"]
        if info["inventory_level"][0] == "0":
            continue

        if "Art Series" in info["true set"][0]:
            continue

        link = info["url_detail"][0]
        stock = 0
        price = 9999999
        for condition in info["hawk_child_attributes"]:
            condition_stock = float(condition["child_inventory_level"][0])
            if condition_stock == 0:
                continue
            
            condition_price = float(condition["child_price_retail"][0])
            if condition_price < price:
                price = condition_price

            condition_sale_price = float(condition["child_price_sale"][0])
            if condition_sale_price != 0 and condition_sale_price < price:
                price = condition_sale_price
        
        cards.append({
            "name": card_name,
            "store": "face",
            "stock": stock,
            "link": link,
            "price": price
        })
    return cards


def get_face_to_face(card_name):
    # return legacy_webscrape(card_name)
    return api_call(card_name)

