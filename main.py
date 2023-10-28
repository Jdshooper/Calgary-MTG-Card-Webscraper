from webscrape import top_cards_from_each_multi
from webscrape import top_cards_from_each

def read_card_list(file_name):
    f = open(file_name, "r")
    str = f.read()
    cards = str.split('\n')
    cards.pop() # last newline
    return cards

def write_results(file_name, cards):
    f = open(file_name, "a")
    for options in cards:
        for option in options:
            f.write(str(option['price']) + "," + option['link'] + ",")
        f.write("\n")
    f.close()
    return

def write_optimal_results(file_name, cards):
    f = open(file_name, "a")
    for card in cards:
        f.write(card['name'] + "," + str(card['price']) + "," + card['link'] + ",")
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

if __name__ == '__main__':
    # Cards List Regex for Archidekt: \((.*) And 1x
    # Possible other store addition: https://www.ebay.ca/str/4thdimensiongames
    file = "cards_list.txt"
    card_list = read_card_list(file)
    final_list = list()
    for card in card_list:
        # Legacy for if multithreading isn't working:
        # final_list.append(top_cards_from_each(card))
        # 33.024s - Non-threaded (5 cards)
        # 15.430s - Threaded (5 cards)
        final_list.append(top_cards_from_each_multi(card))

    # for item in final_list:
    #     print(item)
    # optimal_prices = process_optimal_price(final_list)
    # write_optimal_results("found_cards.csv", optimal_prices)

    write_results("found_cards.csv", final_list)

