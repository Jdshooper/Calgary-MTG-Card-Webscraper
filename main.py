from webscrape import *
from present import *

def read_card_list(file_name):
    f = open(file_name, "r")
    str = f.read()
    cards = str.split('\n')
    cards.pop() # last newline
    return cards

if __name__ == '__main__':
    # Cards List Regex for Archidekt: \((.*) And 1x
    # Possible other store addition: https://www.ebay.ca/str/4thdimensiongames
    file = "cards_list.txt"
    card_list = read_card_list(file)
    final_list = list()
    
    # TODO: Include this in the webscrape package - get_top_cards_multi(card_list)
    for card in card_list:
        # Legacy for if multithreading isn't working:
        # final_list.append(top_cards_from_each(card))
        # 33.024s - Non-threaded (5 cards)
        # 15.430s - Threaded (5 cards)
        final_list.append(top_cards_from_each_multi(card))

    # write_optimal_results("found_cards.csv", final_list)
    write_results("found_cards.csv", final_list)

