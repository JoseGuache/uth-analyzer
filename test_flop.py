from hand import deal_hand, evaluate_best_hand
from strategy import preflop_raise, flop_raise, river_raise

fold_count = 0
total = 0
for _ in range(2000):
    player_cards, dealer_cards, community_cards = deal_hand()
    if preflop_raise(player_cards):
        continue   # only care about hands that reach the flop decision
    if flop_raise(player_cards, community_cards):
        continue
    total+= 1
    if not river_raise(player_cards, community_cards):
        fold_count += 1

print(f"Reached river: {total}")
print(f"Folded at river: {fold_count}")
print(f"Fold rate among river-reachers: {fold_count/total:.2%}")