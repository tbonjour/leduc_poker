from leduc.state import Leduc as State
from leduc.card import Card
from leduc.hand_eval import leduc_eval as eval
from itertools import permutations
from leduc.players.random_player import RandomPlayer
from leduc.players.call_player import CallPlayer
from leduc.players.raise_player import RaisePlayer
from leduc.players.rule_player import RulePlayer

import random
import numpy as np

'''Leduc Hold'em is a toy poker game sometimes used in academic research (first introduced in Bayes' Bluff: Opponent 
Modeling in Poker). It is played with a deck of six cards, comprising two suits of three ranks each (often the king, 
queen, and jack - in our implementation, the ace, king, and queen). The game begins with each player being dealt one 
card privately, followed by a betting round. Then, another card is dealt face-up as a community (or board) card, and 
there is another betting round. Finally, the players reveal their private cards. If one player's private card is the 
same rank as the board card, he or she wins the game; otherwise, the player whose private card has the higher rank 
wins.'''

'''
Leduc Hold'em is a poker variant where each player is dealt a card from a deck of 3 cards in 2 suits. The first round 
consists of a pre-flop betting round. The second round consists of a post-flop betting round after one board card is 
dealt. There is a two bet maximum per round, with raise sizes of 2 and 4 for each round. Each player antes 1 before 
the game starts.'''


def play_game(players):
    num_cards = len(players) + 1
    cards = [Card(14, 1), Card(13, 1), Card(12, 1), Card(14, 2), Card(13, 2), Card(12, 2)]
    all_combos = [list(t) for t in set(permutations(cards, num_cards))]
    card = np.random.choice(len(all_combos))
    state = State(all_combos[card], len(players), eval, players)
    while state.terminal is False:
        print('*' * 30)
        print('Player Turn', state.turn)
        curr_player = state.players[state.turn]
        print('Current Player', curr_player.name)
        if not curr_player.folded:
            action = curr_player.select_action(state.valid_actions(curr_player), state.get_current_state())
            print('Action', action)
            state = state.take(action)
            for i, player in enumerate(state.players):
                print('pl', player.name, ' bets', player.bets)
        else:
            state.turn += 1

    payout = state.utility()
    print('*' * 30)
    # print('Payout', payout)
    print('Current Amounts', [p.amount for p in players])
    winners = np.argwhere(payout == np.amax(payout)).flatten().tolist()
    # winners
    # print(winners)
    winner_names = []
    if len(winners) > 1:
        for winner in winners:
            winner_names.append(state.players[winner].name)
        print('Winners are', winner_names, '\n')
    else:
        winner_names.append(state.players[winners[0]].name)
        print('Winner is', state.players[winners[0]].name, '\n')
    # return # state.players[np.argmax(payout)]
    return winner_names


def rotate(lst, n):
    n = n % len(lst)
    return lst[n:] + lst[:n]


def play_multiple_rotations(players, num_rotations=None):
    rotation_winners = {}
    for player in players:
        if player.name not in rotation_winners:
            rotation_winners[player.name] = 0
    if num_rotations is None:
        num_rotations = len(players)
    for rotation in range(num_rotations):
        print('-------- Rotation', rotation, '--------')

        current_rot = rotate(players, rotation)
        print('Current in-game positions', current_rot, '\n')
        if all(x > 1 for x in [p.amount for p in current_rot]):
            winners = play_game(current_rot)
        else:
            break
        # print('WINNERS', winners)
        for winner in winners:
            rotation_winners[winner] += 1
        for player in players:
            player.bets = 1
            player.folded = False
            player.raised = False
    # print('Rotation Winners:', rotation_winners)
    print(current_rot)
    return rotation_winners


def play_multiple_games(players, num_games=10, seed=2):
    """Play multiple games. For each game we shuffle the player order and then play multiple rotations
    in a given order. Number of rotations is equal to the number of players. For instance, if 3 players are
    to play multiple games, and the number of games is 10, then there will be a total of 3 * 10 hands played.
    Attributes
        players:    a list of players that are going to play the games
        num_games:  int value denoting the total numbers of games to play
        seed: random seed for reproducibility
    """
    total_games_winners = {}
    for player in players:
        if player.name not in total_games_winners:
            total_games_winners[player.name] = 0
    random.seed(seed)
    for game in range(num_games):
        print('-------- Game', game, '--------')
        random.shuffle(players)
        print('Initial game positions: ', players, '\n')
        if all(x > 1 for x in [p.amount for p in players]):
            rotation_winners = play_multiple_rotations(players)
        for player_name in total_games_winners:
            total_games_winners[player_name] += rotation_winners[player_name]
        print()
    # print('Final Win Count: ', total_games_winners)
    print(players)


players = [RulePlayer('Rule A'), RulePlayer('Rule B'), RulePlayer('Rule C')]
play_multiple_games(players, 10)
