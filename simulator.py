from hand import deal_hand, evaluate_best_hand, get_rank_value
from strategy import preflop_raise, flop_raise, river_raise
from payouts import TRIPS_PAYOUTS, BLIND_PAYOUTS, ULTIMATE_PAIRS_PAYOUTS

def compare_hands(player_cards, dealer_cards, community_cards):
    player_best = evaluate_best_hand(player_cards + community_cards)
    dealer_best = evaluate_best_hand(dealer_cards + community_cards)

    dealer_qualifies = dealer_best[0] >= 2

    if player_best[0] > dealer_best[0]:
        result = 'player_wins'
    elif player_best[0] < dealer_best[0]:
        result = 'dealer_wins'
    else:
        if player_best[1] > dealer_best[1]:
            result = 'player_wins'
        elif player_best[1] < dealer_best[1]:
            result = 'dealer_wins'
        else:
            result = 'tie'

    return {
        'result': result,
        'dealer_qualifies': dealer_qualifies
    }

def get_hand_name(score):
    hand_names = {
        10: 'royal_flush',
        9: 'straight_flush',
        8: 'quads',
        7: 'full_house',
        6: 'flush',
        5: 'straight',
        4: 'trips',
        3: 'two_pair',
        2: 'one_pair',
        1: 'high_card'
    }
    return hand_names.get(score, 'high_card')

def evaluate_ultimate_pairs(player_cards):
    c1 ,c2 = player_cards
    r1 ,r2 = get_rank_value(c1), get_rank_value(c2)
    suited = c1[1] == c2[1]
    ranks = sorted([r1, r2], reverse=True)

    if ranks == [14, 14]:
        return 'pair_of_aces'
    if ranks == [14,13] and suited:
        return 'ak_suited'
    if ranks[0] == ranks[1] and ranks [0] in [13,12,11]:
        return 'kk_qq_jj'
    if ranks[0] == 14 and ranks[1] in [12, 11] and suited:
        return 'aq_aj_suited'
    if ranks == [14, 13] and not suited:
        return 'ak_unsuited'
    if ranks[0] == 14 and ranks[1] in [12, 11] and not suited:
        return 'aq_aj_unsuited'
    if ranks[0] == ranks[1]:
        return 'pair_2s_10s'
    return None

def calculate_payout(ante, play_bet, result, dealer_qualifies, player_cards, community_cards):
    net = 0

    # Main bets
    if result == 'player_wins':
        if dealer_qualifies:
            net += ante  # ante pays 1:1
        net += play_bet

        all_cards = player_cards + community_cards
        hand_score = evaluate_best_hand(all_cards)[0]
        blind_hand = get_hand_name(hand_score)
        if blind_hand in BLIND_PAYOUTS:
            net += ante * BLIND_PAYOUTS[blind_hand]
            
    elif result == 'dealer_wins':
        net -= ante
        net -= play_bet
        net -= ante  # blind loses
    
    return net

def simulate_hand(ante, trips_bet, pairs_bet):
    player_cards, dealer_cards, community_cards = deal_hand()

    # Determine play bet
    if preflop_raise(player_cards):
        play_bet = ante * 4
        raise_street = 'preflop'
    elif flop_raise(player_cards, community_cards):
        play_bet = ante * 2
        raise_street = 'flop'
    elif river_raise(player_cards, community_cards):
        play_bet = ante * 1
        raise_street = 'river'
    else:
        play_bet = 0
        raise_street = 'fold'

    if raise_street == 'fold':
        net = -ante * 2   # lose ante and blind
        comparison = {'result': 'folded', 'dealer_qualifies': None}
    else:
        comparison = compare_hands(player_cards, dealer_cards, community_cards)
        net = calculate_payout(ante, play_bet, comparison['result'], comparison['dealer_qualifies'], player_cards, community_cards)

    if trips_bet > 0 or pairs_bet > 0:
        all_cards = player_cards + community_cards
        hand_score = evaluate_best_hand(all_cards)[0]

        if trips_bet > 0:
            trips_hand = get_hand_name(hand_score)
            if trips_hand in TRIPS_PAYOUTS:
                net += trips_bet * TRIPS_PAYOUTS[trips_hand]
            else:
                net -= trips_bet

        if pairs_bet > 0:
            pairs_result = evaluate_ultimate_pairs(player_cards)
            if pairs_result in ULTIMATE_PAIRS_PAYOUTS:
                net += pairs_bet * ULTIMATE_PAIRS_PAYOUTS[pairs_result]
            else:
                net -= pairs_bet

    return {
        'player_cards': player_cards,
        'dealer_cards': dealer_cards,
        'community_cards': community_cards,
        'play_bet': play_bet,
        'raise_street': raise_street,
        'net': net,
    }