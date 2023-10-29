def write_results(file_name, cards):
    f = open(file_name, "a")
    for options in cards:
        f.write("\"" + options[0]['name'] + "\",")
        for option in options:
            f.write(str(option['price']) + "," + option['link'] + ",")
        f.write("\n")
    f.close()
    return

def process_optimal_price(cards):
    calgary_list = ["sentry", "er"]
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


def write_optimal_results(file_name, cards):
    optimal_cards = process_optimal_price(cards)
    f = open(file_name, "a")
    for card in optimal_cards:
        f.write(card['name'] + "," + str(card['price']) + "," + card['link'] + ",")
        f.write("\n")
    f.close()
    return



