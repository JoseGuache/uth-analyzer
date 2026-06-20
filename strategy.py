from hand import deal_hand, evaluate_best_hand, evaluate_five_card_hand, get_rank_value
from itertools import combinations

def get_remaining_cards(player_cards, community_cards):
    from deck import SUITS, RANKS
    full_deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    used = player_cards + community_cards
    return[card for card in full_deck if card not in used]

def dealer_beats_player_count(player_cards, community_cards):
    remaining = get_remaining_cards(player_cards, community_cards)
    player_best = evaluate_best_hand(player_cards + community_cards)

    beats = 0
    total = 0
    for dealer_hand in combinations(remaining, 2):
        dealer_best = evaluate_best_hand(list(dealer_hand) + community_cards)
        total += 1
        if dealer_best[0] > player_best[0]:
            beats += 1
        elif dealer_best[0] == player_best[0] and dealer_best[1] > player_best[1]:
            beats += 1

    return beats, total

def preflop_raise(player_cards):
    r1, r2 = get_rank_value(player_cards[0]), get_rank_value(player_cards[1])
    ranks = sorted([r1, r2], reverse=True)
    high, low = ranks[0], ranks[1]
    suited = player_cards[0][1] == player_cards[1][1]

    if high == low:  # any pair
        return True
    if high == 14:  # any ace
        return True
    if high == 13 and low >= 6:  # K6 or better
        return True
    if high == 12 and low >= 8:  #Q8 or better
        return True
    if high == 11 and low == 10: # J10
        return True
    return False

def flop_raise(player_cards, community_cards):
    flop = community_cards[:3]
    all_cards = player_cards + flop
    hand_score = evaluate_best_hand(all_cards)[0]

    # Two pair or better
    if hand_score >= 3:
        return True
    
    # Hidden pair (pair using at least one hole card)
    p1, p2 = get_rank_value(player_cards[0]), get_rank_value(player_cards[1])
    board_ranks = [get_rank_value(c) for c in flop]
    if p1 == p2:
        return True
    if p1 in board_ranks or p2 in board_ranks:
        return True
        
    # Four to a flush
    suits = [card[1] for card in all_cards]
    for suit in set(suits):
        if suits.count(suit) >=4:
            return True
    
    # Open ended straight draw with at least oone overcard to board
    ranks = sorted(set([get_rank_value(card) for card in all_cards]), reverse=True)
    board_max = max(board_ranks)
    player_ranks = [p1, p2]
    has_overcard = any(r > board_max for r in player_ranks)

    for i in range(len(ranks) - 3):
        if ranks[i] - ranks[i+3] == 3:
            if has_overcard:
                return True
    
    # Gunshot with two overcards
    for i in range(len(ranks) - 3):
        if ranks[i] - ranks[i+3] == 4 and len(set(ranks[i:i+4])) == 4:
            overcards = sum(1 for r in player_ranks if r > board_max)
            if overcards >= 2:
                return True
        
    return False

def river_raise(player_cards, community_cards):
    p1, p2 = get_rank_value(player_cards[0]), get_rank_value(player_cards[1])
    board_ranks = [get_rank_value(c) for c in community_cards]

    # Always raise with a hidden pair
    if p1 == p2 or p1 in board_ranks or p2 in board_ranks:
        return True
    
    all_cards = player_cards + community_cards
    hand_score = evaluate_best_hand(all_cards)[0]
    if hand_score >= 3:
        return True
    
    beats, total = dealer_beats_player_count(player_cards, community_cards)
    win_probability = 1 - (beats / total)
    
    return win_probability > 0.5