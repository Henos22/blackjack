import random

from rich.console import Console
from rich.prompt import Prompt

console = Console()
prompt = Prompt()

def generate_deck()-> list:
    """ Generates a deck a 52 cards

    Returns:
        list: Cards
    """
    values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    suits = ['H','D','C','S']
    deck = [value+suit for suit in suits for value in values ]
    return deck


def shuffle_deck(deck: list)-> list:
    """Shuffles the deck

    Args:
        deck (list): Original, sequential deck

    Returns:
        list: Shuffled deck
    """
    random.shuffle(deck)
    return deck


def begin_game() -> str:
    """ Asks the player if they would like to start the game
    Returns:
        string: Player's response
    """
    return prompt.ask("""
    [magenta]------------ Welcome to the Python Casino ------------ 
    \n    ------------- High Stakes Blackjack Table ------------- 
    \n    ---------------- Are you ready to play? ---------------[/magenta]
    """, choices = ['yes','no'])
    

def players_initial_draw(shuffled_deck: list) -> tuple:
    """Draw 2 cards for the player and remove these cards from the deck

    Args:
        shuffled_deck (list): initial shuffled deck

    Returns:
        tuple: the player's hand and the rest of the deck
    """
    players_hand = []
    random_draw = random.choices(shuffled_deck,k = 2)
    players_hand.append(random_draw)
    shuffled_deck.remove(random_draw)
    return players_hand[0], shuffled_deck


def dealers_initial_draw(shuffled_deck: list) -> tuple:
    """Draw 2 cards for the dealer and remove these cards from the deck

    Args:
        shuffled_deck (list): 50 card deck

    Returns:
        tuple: dealer's hand and 48 card deck
    """

    dealers_hand = []
    random_draw = random.choices(shuffled_deck,k = 2)
    print(random_draw)
    print(shuffled_deck)
    dealers_hand.append(random_draw)
    shuffled_deck.remove(random_draw)
    return dealers_hand[0], shuffled_deck


if __name__ == "__main__":
    deck = generate_deck()
    shuffled_deck = shuffle_deck(deck)
    ready_to_play = begin_game()
    if ready_to_play == "no":
        console.print("    ----------------- Come again soon ----------------------", style = "magenta")
    else:
        initial_player_hand, deck = players_initial_draw(shuffled_deck)
        initial_dealer_hand, deck = dealers_initial_draw(deck)
        console.print(f" You have drawn the {initial_player_hand[0]} and the {initial_player_hand[1]}", style = "magenta")
        console.print(f" The dealer has drawn the {initial_dealer_hand[0]} and the ???")

