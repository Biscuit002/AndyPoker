#Andy's Basic Test bot

from typing import List, Dict, Any
import random

from bot_api import PokerBotAPI, PlayerAction, GameInfoAPI
from engine.cards import Card, Rank
from engine.poker_game import GameState


class andys_bot(PokerBotAPI):
    def __init__(self, name):
        super().__init__(name)
    def get_action(self, game_state, hole_cards, legal_actions, min_bet, max_bet):
        #get cards in hand
        card1 = hole_cards[0]
        card2 = hole_cards[1]
        card_value = 0
        
        #define hand strengths through dictionary
        Strengths = {
            "pair": 25
            "high_card": 5
            "ace_high": 20
            "pocket_aces": 200
            "consecutive_numbers": 50
            "same_suit": 25}

        isPair = (card1.Rank.value == card2.rank.value)
        isHighCard = (card1.Rank.value >= Rank.JACK.value or card2.Rank.value >= Rank.JACK.value))
        isAceHigh = (card1.Rank == Rank.ACE or card2.Rank == Rank.ACE)
        isPocketAces = (card1.Rank == Rank.ACE and card2.Rank == Rank.ACE)
        isConsecutive = (abs(card1.Rank.value - card2.Rank.value) == 1)
        isSameSuit = (card1.Suit == card2.Suit)

        # evaluate hand strength
        card_value += strengths["pair"] * isPair
        card_value += strengths["high_card"] * isHighCard
        card_value += strengths["ace_high"] * isAceHigh
        card_value += strengths["pocket_aces"] * isPocketAces
        card_value += strengths["consecutive_numbers"] * isConsecutive
        card_value += strengths["same_suit"] * isSameSuit


        #determine action
        if cardvalue >= 300:
            intendedAction = PlayerAction.ALL_IN
            intendedAmount = max_bet
        elif cardvalue >= 100 and cardValue <= 300:
            intendedAction = PlayerAction.RAISE
            if max_bet >= cardValue:
                intendedAmount = max_bet
            else:
                intendedAmount = cardValue
        else:
            intendedAction = PlayerAction.CHECK
            intendedAmount = 0

        #check if action is currently legal
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