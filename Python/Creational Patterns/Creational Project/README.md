# Understanding the Blackjack Game: Design Patterns Guide

This guide explains how our object-oriented Blackjack game is structured and how it implements several design patterns. If you're learning about design patterns, this will help you understand how they work in a practical application.

## Overview of the Game Structure

Our Blackjack game is organized into several classes, each with a specific responsibility:

1. **Card, Suit, Rank**: Basic building blocks representing playing cards
2. **Hand**: Manages a collection of cards (for player or dealer)
3. **Design pattern classes**: Special classes implementing specific software design patterns
4. **BlackjackGame**: The main class that coordinates gameplay

## Design Patterns Explained

### 1. Singleton Pattern (BalanceSingleton)

The Singleton pattern ensures a class has only one instance and provides a global point to access it.

```python
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
```

**Key Features:**
- Private instance variable `_instance` tracks the single instance
- Private constructor (`__init__`) prevents direct instantiation
- Class method `get_instance()` controls access to the instance
- First call creates the instance; subsequent calls return the existing instance

**In our game:** Used to manage the player's balance across the game, ensuring we always refer to the same balance object.

**Usage example:**
```python
# Wrong way - raises an exception
# balance = BalanceSingleton()

# Correct way
balance = BalanceSingleton.get_instance()
```

### 2. Factory Pattern (CardFactory)

The Factory pattern creates objects without specifying the exact class of object to be created.

```python
class CardFactory:
    @staticmethod
    def create_standard_deck() -> List[Card]:
        deck = []
        for suit in Suit:
            for rank in Rank:
                deck.append(Card(suit, rank))
        return deck
```

**Key Features:**
- Centralizes object creation logic
- Hides implementation details of how objects are created
- Makes code more maintainable by isolating creation logic

**In our game:** Used to create a standard deck of 52 cards without the client needing to know how to create each card.

**Usage example:**
```python
deck = CardFactory.create_standard_deck()
```

### 3. Prototype Pattern (DeckPrototype)

The Prototype pattern allows cloning objects without coupling to their specific classes.

```python
class DeckPrototype:
    def __init__(self, cards: List[Card]):
        self.cards = cards.copy()
        self.shuffle()
    
    def clone(self):
        return DeckPrototype(self.cards)
```

**Key Features:**
- Creates new objects by copying existing ones
- Avoids recreating objects from scratch when similar objects are needed
- Provides flexibility in runtime by creating objects dynamically

**In our game:** Allows us to create new shuffled decks efficiently from an existing deck prototype.

**Usage example:**
```python
deck_prototype = DeckPrototype(CardFactory.create_standard_deck())
game_deck = deck_prototype.clone()  # Create a new deck for this game
```

### 4. Builder Pattern (HandBuilder)

The Builder pattern separates the construction of a complex object from its representation.

```python
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
```

**Key Features:**
- Creates objects step-by-step
- Uses method chaining (fluent interface) for a clean API
- Separates construction from representation
- Reusable for creating different variations of objects

**In our game:** Used to build player and dealer hands incrementally.

**Usage example:**
```python
player_hand = HandBuilder().add_card(card1).add_card(card2).build()
```

## How These Patterns Work Together

1. **Game Initialization:**
   - The `BlackjackGame` class gets a singleton instance of `BalanceSingleton`
   - Uses `CardFactory` to create a deck of cards
   - Uses `DeckPrototype` to clone a shuffled deck for each game

2. **Game Round:**
   - Takes bet from player's balance (singleton)
   - Uses `HandBuilder` to create hands for player and dealer
   - Deals cards from the cloned deck
   - Handles game logic and updates balance based on results

## Code Walkthrough: Game Flow

1. **Starting the Game:**
```python
def main():
    game = BlackjackGame()  # Creates game with all required components
    
    while True:
        game.play_round()   # Play one round of blackjack
        # Check if player wants to continue...
```

2. **Playing a Round:**
```python
def play_round(self):
    # Get bet from player
    bet = int(input("Place your bet: $"))
    self.place_bet(bet)
    
    # Start new game with fresh hands
    self.start_new_game()
    
    # Player's turn (hit or stand)
    while player_choice == 'hit':
        self.player_hit()
    
    # Dealer's turn
    self.dealer_play()
    
    # Determine winner and update balance
    self.determine_winner()
```

## Common Questions

### How does the Singleton pattern ensure only one instance exists?
The private constructor raises an exception if called directly. All access must go through the `get_instance()` method, which creates the instance only if it doesn't already exist.

### Why use a Factory instead of direct construction?
The Factory centralizes the deck creation logic, making it easier to modify how cards are created without changing the code that uses them. It also hides the complexity of creating 52 different card objects.

### What's the benefit of the Prototype pattern here?
It allows us to create new decks quickly based on a template deck. This is more efficient than creating a new deck from scratch for each game.

### How does the Builder pattern improve hand creation?
It provides a clean, fluent interface for creating hands and keeps the construction logic separate from the `Hand` class itself. This makes the code more readable and maintainable.

## Exercises to Understand Better

1. **Modify the Singleton:** Add a method to reset the player's balance to a specific amount.

2. **Extend the Factory:** Add a method to create a special deck with multiple standard decks combined (like casinos often use).

3. **Enhance the Prototype:** Add a method to create a deck with certain cards removed.

4. **Improve the Builder:** Add validation to prevent adding more than 5 cards to a hand.

By understanding these patterns, you'll have powerful tools for structuring object-oriented code in a way that's flexible, maintainable, and reusable.