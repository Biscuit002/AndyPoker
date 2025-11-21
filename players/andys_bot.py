#Andy's Test bot (iteration of aggressive)

from typing import List, Dict, Any
import random

from bot_api import PokerBotAPI, PlayerAction, GameInfoAPI
from engine.cards import Card, Rank
from engine.poker_game import GameState


class andys_bot(PokerBotAPI):
    def __init__(self, name):
        super().__init__(name)
    def get_action(self, game_state, hole_cards, legal_actions, min_bet, max_bet):
        card1 = hole_cards[0]
        card2 = hole_cards[1]

        cardvalue = card1.rank.value + card2.rank.value
        #Determine action
        if cardvalue >= 20:
            intendedAction = PlayerAction.ALL_IN
            intendedAmount = max_bet
        else:
            intendedAction = PlayerAction.CHECK
            intendedAmount = 0

        #Check if action is currently legal
        if intendedAction in legal_actions:
            return intendedAction, intendedAmount
        elif PlayerAction.RAISE in legal_actions:
            return PlayerAction.RAISE, max_bet
        elif PlayerAction.CALL in legal_actions:
            return PlayerAction.CALL,0
        elif PlayerAction.CHECK in legal_actions:
            return PlayerAction.CHECK, 0
        elif PlayerAction.ALL_IN in legal_actions:
            return PlayerAction.ALL_IN, max_bet
        else:
            return PlayerAction.FOLD, 0
    def hand_complete(self, game_state, hand_result):
        pass