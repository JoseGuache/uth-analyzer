import random

SUITS = ['hearts','diamonds','clubs','spades']
RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

def build_deck():
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            deck.append((rank, suit))
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def deal_card(deck):
    return deck.pop()