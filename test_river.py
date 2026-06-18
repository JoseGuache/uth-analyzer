from hand import deal_hand, evaluate_best_hand, evaluate_five_card_hand
from strategy import river_raise

for _ in range(5):
    player_cards, dealer_cards, community_cards = deal_hand()
    all_cards = player_cards + community_cards
    player_hand = evaluate_best_hand(all_cards)
    board_hand = evaluate_five_card_hand(community_cards)
    decision = river_raise(player_cards, community_cards)

    print("Player cards:", player_cards)
    print("Community cards:", community_cards)
    print("Player best hand:", player_hand)
    print("Board hand:", board_hand)
    print("Raise decision:", decision)
    print("---")