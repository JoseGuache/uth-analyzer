from simulator import simulate_hand
from collections import Counter

def run_simulation(num_hands, ante, trips_bet, pairs_bet):
    total_net = 0
    results = []
    fold_samples = 0

    for _ in range(num_hands):
        outcome = simulate_hand(ante, trips_bet, pairs_bet)
        total_net += outcome['net']
        results.append(outcome)
        
        if outcome['raise_street'] == 'fold' and fold_samples < 5:
            print("FOLD HAND:")
            print("player:", outcome['player_cards'])
            print("Community:", outcome['community_cards'])
            print("---")
            fold_samples += 1

    print("LOOP FINISHED")

    print(f"hands played: {num_hands}")
    print(f"Total net: {total_net}")
    print(f"Average net per hand: {total_net / num_hands: .2f}")

    streets = Counter([r['raise_street'] for r in results])
    print(streets)

    return results

if __name__ == "__main__":
    run_simulation(num_hands=1000, ante=5, trips_bet=0, pairs_bet=0)