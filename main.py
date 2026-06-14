from simulator import simulate_hand

def run_simulation(num_hands, ante, trips_bet, pairs_bet):
    total_net = 0
    results = []

    for _ in range(num_hands):
        outcome = simulate_hand(ante, trips_bet, pairs_bet)
        total_net += outcome['net']
        results.append(outcome)

    print(f"hands played: {num_hands}")
    print(f"Total net: {total_net}")
    print(f"Average net per hand: {total_net / num_hands: .2f}")

    from collections import Counter
    streets = Counter([r['raise_street'] for r in results])
    print(streets)

    return results

if __name__ == "__main__":
    run_simulation(num_hands=10000, ante=5, trips_bet=0, pairs_bet=0)