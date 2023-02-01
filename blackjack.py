import random
from typing import Union

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
    """, choices = ['yes','no'], default = "yes")
    

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
    for card in random_draw:
        shuffled_deck.remove(card)
 
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
    dealers_hand.append(random_draw)
    for card in random_draw:
        shuffled_deck.remove(card)
    
    return dealers_hand[0], shuffled_deck

def get_card_value(card: str, over_ten: bool)-> int or tuple:
    """Finds the point value of a given card

    Args:
        card (str): any card

    Returns:
        over_ten (int): the point value of the card
    """
    value = card[:-1]
    if value.isnumeric():
        return int(value)
    if value == 'J' or value == 'Q' or value == 'K':
        return 10
    if value == 'A' and over_ten:
        return 1
    if value == 'A' and over_ten is False:
        return 11

def hand_value(hand: list)-> int:
    """calculate the point value of the hand

    Args:
        hand (list): cards in the hand

    Returns:
        int: point value of hand
    """
    point_value = 0
    for card in hand:
        over_ten = point_value > 10
        point_value += get_card_value(card,over_ten)
    return point_value

def check_for_blackjack(points: int) -> bool:
    """Check if score is 21

    Args:
        points (int): hand value

    Returns:
        bool: whether or not hand is 21
    """
    return points == 21

def draw_card(hand: list,deck: list,player:str) -> tuple:
    """Adds a random card to the hand and removes the card from the deck

    Args:
        hand (list): relevant player's hand
        deck (list): deck before new card is drawn
        player (str): player drawing the card (dealer/player)

    Returns:
        tuple: new hand and updated deck with 1 card removed
    """

    new_card = random.choices(deck)[0]
    hand.append(new_card)
    deck.remove(new_card)
    new_hand = hand
    console.print(f" {player} has drawn the {new_card} \n ----- {player} has {hand_value(new_hand)} -----", style = "#55d4ff")
    return new_hand, deck


def players_turn(players_hand: list, deck: list) -> Union[None, tuple]:
    """Asks the player for their decision

    Args:
        players_hand (list): player's hand
        deck (list): deck of cards as is

    Returns:
        Union[None, tuple]: either none to signal sticking or the updated hand and deck
    """
    hit_or_stick = prompt.ask("[#55d4ff] Would you like to HIT or STICK?[/#55d4ff]", choices = ["hit", "stick"])
    if hit_or_stick == "stick":
        console.print(f" {player_name} sticks on {hand_value(players_hand)}", style = "#55d4ff")
        return
    else:
        players_new_hand,deck = draw_card(players_hand,deck,player_name)
        return players_new_hand,deck
        


def check_new_hand(hand: list) -> int:
    """Checks whether the hand is blackjack, bust or below 21

    Args:
        hand (list): player's hand

    Returns:
        int: numbers to signal different outcomes
    """

    value_of_hand = hand_value(hand)
    if check_for_blackjack(value_of_hand):
        console.print(f" {player_name} has BlackJack! \n -- Dealer's Turn --")
        return 0
    elif value_of_hand > 21:
        return 1
    else:
        return 2

def check_winner(dealer_points:int,player_points:int) -> None:
    """Checks which player's hand was worth more

    Args:
        dealer_points (int): value of dealer's hand
        player_points (int): value of player's hand

    Returns:
        function: gets the relevant message to announce the result
    """
    if check_for_blackjack(dealer_points) and check_for_blackjack(player_points):
        console.print(f"{player_name} and Dealer have BlackJack!")
        return result_messages("no winner")
    elif player_points > dealer_points:
        return result_messages("player")
    elif dealer_points > player_points:
        return result_messages("dealer")
    else:
        return result_messages("no winner")


def dealers_turn(hand: list, deck: list) -> tuple:
    """Dealer's turn where they will keep hitting until bust or a hand
    value equal to or above 16

    Args:
        hand (list): dealer's hand
        deck (list): current deck

    Returns:
        tuple: dealer's new hand and deck with card removed
    """
    dealers_points = hand_value(hand)
    if dealers_points < 16:
        new_hand, deck = draw_card(hand,deck,"dealer")
        return dealers_turn(new_hand,deck)
    else:
        if dealers_points <= 21:
            console.print(f" Dealer sticks on {dealers_points}", style = "#55d4ff")
            console.print("------------------",style = "#55d4ff")
            return hand,deck
        else:
            return


def result_messages(winner: str) -> None:
    """Messages to tell the player the result of the game

    Args:
        winner (str): player name or dealer
    """
    if winner == "player":
        console.print(f" Congratulations! \n {player_name} has won the hand", style = "#55d4ff")
    elif winner == "dealer":
        console.print(f" Dealer has won the hand", style = "#55d4ff")
    else:
        console.print(f" The hand ends a tie", style = "#55d4ff")
    return 
     
def trigger_dealer_turn(hand:list,deck: list) -> None:
    """Performs the dealers turn and then checks the result
    of the game once their turn is over

    Args:
        hand (list): dealer's initial hand
        deck (list): current deck
    """
    dealers_new_hand_and_deck = dealers_turn(hand, deck)
    if dealers_new_hand_and_deck:
        dealers_new_hand,deck = dealers_new_hand_and_deck
        dealers_points = hand_value(dealers_new_hand)
        if dealers_points == 21:
            console.print(" BLACKJACK!", style = "#55d4ff")
        return check_winner(dealers_points,players_points)
    else:
        console.print(" Dealer has gone BUST!", style = "#55d4ff")
        return result_messages(player_name)
    


if __name__ == "__main__":
    deck = generate_deck()
    shuffled_deck = shuffle_deck(deck)
    ready_to_play = begin_game()
    game_status = True
    if ready_to_play == "no":
        console.print("    ----------------- Come again soon ----------------------", style = "magenta",justify = "center")
    else:
        player_name = prompt.ask("[magenta]    --------------- Enter your name to begin --------------[/magenta]")
        initial_player_hand, deck = players_initial_draw(shuffled_deck)
        initial_dealer_hand, deck = dealers_initial_draw(deck)
        players_points = hand_value(initial_player_hand)
        dealers_points = hand_value(initial_dealer_hand) 
        player_natural_blackjack_check = check_for_blackjack(players_points)
        dealer_natural_blackjack_check = check_for_blackjack(dealers_points)
        
        console.print(f" {player_name} has drawn the {initial_player_hand[0]} and the {initial_player_hand[1]}", style = "#55d4ff")
        console.print(f" ----- {player_name} has {players_points} ------", style ="#55d4ff")

        if player_natural_blackjack_check and dealer_natural_blackjack_check:
            console.print(f" BLACKJACK! \n ------ Dealer's turn ------\n The dealer has drawn the {initial_dealer_hand[0]} and the {initial_dealer_hand[1]} \n Dealer has {hand_value(initial_dealer_hand)}", style = "#55d4ff")
            console.print(f" BLACKJACK! \n Both players have Blackjack \n ---------------", style = "#55d4ff")
            result_messages("no winner")
             
        elif player_natural_blackjack_check and dealer_natural_blackjack_check is False:
            console.print(f" BLACKJACK! \n ------ Dealer's turn ----\n The dealer has drawn the {initial_dealer_hand[0]} and the {initial_dealer_hand[1]}",style = "#55d4ff")
            console.print(f"----- Dealer has {hand_value(initial_dealer_hand)} -----", style = "#55d4ff")
            console.print("------------------",style = "#55d4ff")
            result_messages("player")
        else: 
            console.print(f" The dealer has drawn the {initial_dealer_hand[0]} and the ???", style = "#55d4ff")
            players_new_hand_and_deck = players_turn(initial_player_hand, deck)
            is_players_turn = True
            while is_players_turn:
                if players_new_hand_and_deck is None:
                    console.print("------ Dealer's turn ------", style = "#55d4ff")
                    console.print(f" Dealer has the {initial_dealer_hand[0]} and the {initial_dealer_hand[1]}", style = "#55d4ff")
                    trigger_dealer_turn(initial_dealer_hand,deck)
                    is_players_turn = False
                elif check_new_hand(players_new_hand_and_deck[0]) == 0:
                    console.print("------ Dealer's turn ------", style = "#55d4ff")
                    console.print(f" Dealer has the {initial_dealer_hand[0]} and the {initial_dealer_hand[1]}", style = "#55d4ff")  
                    trigger_dealer_turn(initial_dealer_hand,deck)
                    is_players_turn = False
                elif check_new_hand(players_new_hand_and_deck[0]) == 1:
                    console.print(f" {player_name} has gone BUST!", style = "#55d4ff")
                    console.print("------------------",style = "#55d4ff")
                    result_messages("dealer")
                    is_players_turn = False
                else:
                    players_new_hand_and_deck = players_turn(initial_player_hand, deck)
                


