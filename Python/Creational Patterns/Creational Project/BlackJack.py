import random
from enum import Enum
from typing import List, Optional, Tuple


class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Rank(Enum):
    ACE = ("A", 11)
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 10)
    QUEEN = ("Q", 10)
    KING = ("K", 10)

    def __init__(self, symbol, card_value):
        self.symbol = symbol
        self.card_value = card_value


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank.symbol} of {self.suit.value}"

    @property
    def value(self):
        return self.rank.card_value


class CardFactory:
    @staticmethod
    def create_standard_deck() -> List[Card]:
        deck = []
        for suit in Suit:
            for rank in Rank:
                deck.append(Card(suit, rank))
        return deck


class DeckPrototype:
    def __init__(self, cards: List[Card]):
        self.cards = cards.copy()
        self.shuffle()
    
    def clone(self):
        return DeckPrototype(self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self) -> Optional[Card]:
        if not self.cards:
            return None
        return self.cards.pop()
    
    def remaining_cards(self) -> int:
        return len(self.cards)


class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def get_value(self) -> int:
        value = 0
        ace_count = 0
        
        for card in self.cards:
            value += card.value
            if card.rank == Rank.ACE:
                ace_count += 1
        
        # Adjust for aces if needed
        while value > 21 and ace_count > 0:
            value -= 10  # Convert Ace from 11 to 1
            ace_count -= 1
            
        return value
    
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_busted(self) -> bool:
        return self.get_value() > 21
    
    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class HandBuilder:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.hand = Hand()
        return self
    
    def add_card(self, card: Card):
        self.hand.add_card(card)
        return self
    
    def build(self) -> Hand:
        result = self.hand
        self.reset()
        return result


class BalanceSingleton:
    _instance = None
    
    def __init__(self):
        if BalanceSingleton._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() instead.")
        self._balance = 1000  # Default starting balance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def balance(self):
        return self._balance
    
    def add_funds(self, amount: int):
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def place_bet(self, amount: int) -> bool:
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return True
        return False
    
    def win_bet(self, amount: int):
        self.add_funds(amount * 2)  # Return original bet + winnings


class BlackjackGame:
    def __init__(self):
        self.balance = BalanceSingleton.get_instance()
        self.deck_prototype = DeckPrototype(CardFactory.create_standard_deck())
        self.deck = None
        self.player_hand_builder = HandBuilder()
        self.dealer_hand_builder = HandBuilder()
        self.player_hand = None
        self.dealer_hand = None
        self.current_bet = 0
    
    def start_new_game(self):
        self.deck = self.deck_prototype.clone()
        self.player_hand = self.player_hand_builder.reset(). 
        self.dealer_hand = self.dealer_hand_builder.reset().build()
        
        # Deal initial hands
        self.player_hand = self.player_hand_builder.add_card(self.deck.deal_card()).add_card(self.deck.deal_card()).build()
        self.dealer_hand = self.dealer_hand_builder.add_card(self.deck.deal_card()).add_card(self.deck.deal_card()).build()
    
    def place_bet(self, amount: int) -> bool:
        if self.balance.place_bet(amount):
            self.current_bet = amount
            return True
        print(f"Insufficient funds. Current balance: ${self.balance.balance}")
        return False
    
    def player_hit(self):
        card = self.deck.deal_card()
        if card:
            self.player_hand.add_card(card)
            print(f"You drew: {card}")
            print(f"Your hand: {self.player_hand} (Value: {self.player_hand.get_value()})")
            
            if self.player_hand.is_busted():
                print("Busted! You lose.")
                return True
        return False
    
    def dealer_play(self):
        print(f"Dealer's hand: {self.dealer_hand} (Value: {self.dealer_hand.get_value()})")
        
        while self.dealer_hand.get_value() < 17:
            card = self.deck.deal_card()
            if card:
                self.dealer_hand.add_card(card)
                print(f"Dealer draws: {card}")
                print(f"Dealer's hand: {self.dealer_hand} (Value: {self.dealer_hand.get_value()})")
            else:
                break
    
    def determine_winner(self):
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        if self.player_hand.is_blackjack():
            if self.dealer_hand.is_blackjack():
                print("Both have blackjack! It's a push.")
                self.balance.add_funds(self.current_bet)
            else:
                print("Blackjack! You win 1.5x your bet!")
                self.balance.add_funds(int(self.current_bet * 2.5))
        elif self.dealer_hand.is_busted():
            print("Dealer busts! You win!")
            self.balance.win_bet(self.current_bet)
        elif player_value > dealer_value:
            print("You win!")
            self.balance.win_bet(self.current_bet)
        elif player_value < dealer_value:
            print("Dealer wins!")
        else:
            print("It's a push!")
            self.balance.add_funds(self.current_bet)
    
    def play_round(self):
        print("\n--- New Round ---")
        print(f"Current balance: ${self.balance.balance}")
        
        bet = 0
        while bet <= 0:
            try:
                bet = int(input("Place your bet: $"))
                if not self.place_bet(bet):
                    bet = 0
            except ValueError:
                print("Please enter a valid amount.")
        
        self.start_new_game()
        
        # Show initial hands
        print(f"Your hand: {self.player_hand} (Value: {self.player_hand.get_value()})")
        print(f"Dealer's up card: {self.dealer_hand.cards[0]}")
        
        # Check for blackjack
        if self.player_hand.is_blackjack():
            print("You have blackjack!")
            self.dealer_play()
            self.determine_winner()
            return
        
        # Player's turn
        player_busted = False
        while True:
            choice = input("Do you want to hit (h) or stand (s)? ").lower()
            if choice == 'h':
                player_busted = self.player_hit()
                if player_busted:
                    break
            elif choice == 's':
                break

        # Dealer's turn if player didn't bust
        if not player_busted:
            self.dealer_play()
            self.determine_winner()
        
        print(f"Balance: ${self.balance.balance}")


def main():
    print("Welcome to Blackjack!")
    game = BlackjackGame()
    
    while True:
        game.play_round()
        
        if game.balance.balance <= 0:
            print("You're out of money! Game over.")
            break
            
        play_again = input("Play another round? (y/n): ").lower()
        if play_again != 'y':
            print(f"Thanks for playing! Final balance: ${game.balance.balance}")
            break


if __name__ == "__main__":
    main()