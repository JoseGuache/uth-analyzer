from hand import deal_hand, evaluate_best_hand, evaluate_five_card_hand, get_rank_value

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
    all_cards = player_cards + community_cards[:3]
    hand_score = evaluate_best_hand(all_cards)[0]

    # Any made hand
    if hand_score >= 2:
        return True
    
    # Check for flush draw (4 cards of same suit)
    suits = [card[1] for card in all_cards]
    for suit in set(suits):
        if suits.count(suit) >= 4:
            return True
        
    # Check for open ended straight draw
    ranks = sorted(set([get_rank_value(card) for card in all_cards]), reverse=True)
    for i in range(len(ranks) - 3):
        if ranks [i] - ranks[i+3] == 3:
            return True
        
    return False

def river_raise(player_cards, community_cards):
    all_cards = player_cards + community_cards
    player_hand = evaluate_best_hand(all_cards)
    board_hand = evaluate_five_card_hand(community_cards)

    if player_hand[0] > board_hand[0]:
        return True
    if player_hand[0] == board_hand[0] and player_hand [1] > board_hand[1]:
        return True
    return False