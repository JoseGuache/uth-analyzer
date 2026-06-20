from hand import deal_hand
from strategy import dealer_beats_player_count

player_cards, dealer_cards, community_cards = deal_hand()
beats, total = dealer_beats_player_count(player_cards, community_cards)

print("Player Cards:", player_cards)
print("Community:", community_cards)
print(f"Dealer beats player in {beats}/{total} combos")
print(f"Win probability: {1 - beats/total: .2%}")