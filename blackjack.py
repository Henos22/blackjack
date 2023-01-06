import random

from rich.prompt import Prompt
from rich.style import Style

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

def begin_game():
    prompt.ask("[magenta]Hello, welcome to the BlackJack table! \n Are you ready to play?[/magenta]", choices = ['yes','no'])
    return


if __name__ == "__main__":
    deck = generate_deck()
    shuffled_deck = shuffle_deck(deck)
    begin_game()