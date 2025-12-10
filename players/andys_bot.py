#Andy's Basic Test bot
#This is a test edit

from typing import List, Dict, Any
from collections import Counter
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

		#Initialize list of available cards
		availiable_cards = [card1, card2]

		#Initialize variables as false
		isPair = False
		isHighCard = False
		isAceHigh = False
		isPocketAces = False
		isConsecutive = False
		isSameSuit = False
		is2and7 = False
		isFlush = False
		isStraight = False
		isThreeOfAKind = False
		isTwoPair = False
		isFullHouse = False
		isFourOfAKind = False
		isStraightFlush = False
		isRoyalFlush = False

		#Initialize hand strength value
		card_value = 0

		#access to current round
		current_round = game_state.round_name

		#access to community cards
		community_cards = game_state.community_cards

		#access to current bet
		current_bet = game_state.current_bet

		#define hand strengths through dictionary
		strengths = {
			"pair": 25,
			"high_card": 1,
			"ace_high": 20,
			"pocket_aces": 200,
			"consecutive_numbers": 50,
			"same_suit": 25,
			"2and7": -50,
			"flush": 100,
			"straight": 100,
			"three_of_a_kind": 75,
			"two_pair": 50,
			"full_house": 150,
			"four_of_a_kind": 200,
			"straight_flush": 250,
			"royal_flush": 1000}
		if current_round == "preflop":
			pass
		elif current_round == "flop":
			#add first 3 community cards after flop
			availiable_cards.append(community_cards[0])
			availiable_cards.append(community_cards[1])
			availiable_cards.append(community_cards[2])
		elif current_round == "turn":
			availiable_cards.append(community_cards[3])
		elif current_round == "river":
			availiable_cards.append(community_cards[4])
		#preflop hand evaluation
		isPair = (card1.rank.value == card2.rank.value)
		isHighCard = (card1.rank.value >= Rank.JACK.value or card2.rank.value >= Rank.JACK.value)
		isAceHigh = (card1.rank == Rank.ACE or card2.rank == Rank.ACE)
		isPocketAces = (card1.rank == Rank.ACE and card2.rank == Rank.ACE)
		isConsecutive = (abs(card1.rank.value - card2.rank.value) == 1)
		isSameSuit = (card1.suit == card2.suit)
		is2and7 = ((card1.rank == Rank.TWO and card2.rank == Rank.SEVEN) or (card1.rank == Rank.SEVEN and card2.rank == Rank.TWO))
		#post-flop hand evaluation
		if not current_round == "preflop":
			availiable_cards_sorted = sorted(availiable_cards, key=lambda card: card.rank.value)
			suits = [card.suit for card in availiable_cards_sorted]
			ranks = [card.rank.value for card in availiable_cards_sorted]
			isStraight = False #Initialize as false
			isStraightFlush = False
			isPair = any(count >= 2 for count in Counter(ranks).values())
			isFlush = max(Counter(suits).values()) >= 5
			isThreeOfAKind = (3 in Counter(ranks).values())
			isTwoPair = sum(1 for count in Counter(ranks).values() if count >= 2) >= 2
			isFullHouse = (3 in Counter(ranks).values()) and (2 in Counter(ranks).values())
			isFourOfAKind = 4 in Counter(ranks).values()
			for i in range(len(ranks) - 4): #Straight check logic (need to update)
				if (ranks[i + 4] - ranks[i]) == 4:
					isStraight = True
					if suits[i] == suits[i+1] == suits[i+2] == suits [i+3] == suits[i+4]:
						isStraightFlush = True
						break
			isRoyalFlush = isStraightFlush and all(rank >= 10 for rank in ranks) #need to update
		# evaluate hand strength
		card_value += (strengths["pair"] * isPair
		+ strengths["high_card"] * isHighCard
		+ strengths["ace_high"] * isAceHigh
		+ strengths["pocket_aces"] * isPocketAces
		+ strengths["consecutive_numbers"] * isConsecutive
		+ strengths["same_suit"] * isSameSuit
		+ strengths["2and7"] * is2and7 #worst hand in poker
		#post-flop evaluations
		+ strengths["flush"] * isFlush
		+ strengths["straight"] * isStraight
		+ strengths["three_of_a_kind"] * isThreeOfAKind
		+ strengths["two_pair"] * isTwoPair
		+ strengths["full_house"] * isFullHouse
		+ strengths["four_of_a_kind"] * isFourOfAKind
		+ strengths["straight_flush"] * isStraightFlush
		+ strengths["royal_flush"] * isRoyalFlush)
		#determine action
		if card_value >= 100:
			intendedAction = PlayerAction.ALL_IN
			intendedAmount = max_bet
		elif card_value >= 75:
			intendedAction = PlayerAction.RAISE
			intendedAmount = clamp(int(max_bet * 0.02) + current_bet, min_bet, max_bet)
		elif card_value >= 50:
			intendedAction = PlayerAction.RAISE
			intendedAmount = clamp(int(max_bet * 0.01) + current_bet, min_bet, max_bet)
		elif card_value >= 25:
			intendedAction = PlayerAction.RAISE
			intendedAmount = clamp(int(max_bet * 0.005) + current_bet, min_bet, max_bet)
		elif card_value >= 0:
			intendedAction = PlayerAction.CHECK
			intendedAmount = 0
		else:
			intendedAction = PlayerAction.FOLD
			intendedAmount = 0

		self.logger.info("card value: " + str(card_value))
		self.logger.info("intended action: " + str(intendedAction))
		self.logger.info("legal actions: " + str(legal_actions))
		self.logger.info("current bet: " + str(current_bet))
		self.logger.info("intended amount: " + str(intendedAmount))
		# check if action is currently legal
		if intendedAction in legal_actions:
			legal_actions.clear()
			legal_actions.append(intendedAction)
			return intendedAction, intendedAmount
		elif current_bet >= 400 and PlayerAction.FOLD in legal_actions and not card_value >= 50:
			return PlayerAction.FOLD, 0
		elif is2and7 == True and PlayerAction.FOLD in legal_actions:
			return PlayerAction.FOLD, 0
		elif card_value < 0:
			if PlayerAction.FOLD in legal_actions:
				return PlayerAction.FOLD, 0
		elif PlayerAction.CHECK in legal_actions:
			return PlayerAction.CHECK, 0
		elif PlayerAction.CALL in legal_actions:
			if current_bet <= 75 or card_value >= 50:
				return PlayerAction.CALL, current_bet
			elif PlayerAction.FOLD in legal_actions:
				return PlayerAction.FOLD, 0
		elif PlayerAction.RAISE in legal_actions:
			return PlayerAction.RAISE, intendedAmount
		elif PlayerAction.ALL_IN in legal_actions:
			return PlayerAction.ALL_IN, intendedAmount
		else:
			return PlayerAction.FOLD, 0

	def hand_complete(self, game_state, hand_result):
		pass

def clamp(value, min_value, max_value):
	return max(min_value, min(value, max_value), max_value)






