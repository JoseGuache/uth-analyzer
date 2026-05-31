from itertools import combinations
from deck import build_deck, shuffle_deck, deal_card

RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

def get_rank_value(card):
    rank, suit = card
    return RANK_VALUES[rank]

def get_suit(card):
    rank, suit = card
    return suit

def deal_hand():
    deck = build_deck()
    deck = shuffle_deck(deck)

    player_cards = [deal_card(deck), deal_card(deck)]
    dealer_cards = [deal_card(deck), deal_card(deck)]
    community_cards = [deal_card(deck) for _ in range(5)]

    return player_cards, dealer_cards, community_cards

def evaluate_best_hand(cards):
    best = None
    for combo in combinations(cards, 5):
        result = evaluate_five_card_hand(combo)
        if best is None or result[0] > best[0]:
            best = result
    return best

def evaluate_five_card_hand(cards):
    ranks = sorted([get_rank_value(card) for card in cards], reverse=True)
    suits = [get_suit(card) for card in cards]

    is_flush = len(set(suits)) == 1
    is_straight = (max(ranks) - min(ranks) == 4) and (len(set(ranks)) == 5)

    # Special case: A-2-3-4-5 striaght (wheel)
    if set(ranks) == {14,2,3,4,5}:
        is_straight = True
        ranks = [5,4,3,2,1]

    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    counts = sorted(rank_counts.values(), reverse=True)

    if is_flush and ranks == [14,13,12,11,10]:
        return (10, ranks)
    if is_flush and is_straight:
        return (9, ranks)
    if counts [0] == 4:
        return (8, ranks)
    if counts [0] == 3 and counts [1] ==2:
        return (7, ranks)
    if is_flush:
        return (6, ranks)
    if is_straight:
        return (5,ranks)
    if counts [0] == 3:
        return (4, ranks)
    if counts [0] == 2 and counts [1] == 2:
        return (3,ranks)
    if counts [0] == 2:
        return (2, ranks)
    return (1, ranks)