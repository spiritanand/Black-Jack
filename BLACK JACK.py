import random

# Creating global variables that are useful throughout the code
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
# This the type of cards that we encounter in player cards.
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
# This is the number of the card encountered.
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
          'Seven': 7, 'Eight': 8,'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}
# This dictionary is used to find the value of the card using it's rank.
balance = 100
playing = True
# Assigning a boolean that can control the loop that allows the player to
# continue playing or stop the game.


class Card:
    """
    This class initializes the card and displays what card it is.
    """

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    """
    This class makes the 52 playing cards (card objects) using PnC the cards class.
                         (except the Joker XD)
    """

    def __init__(self):
        self.deck = []  # store the deck in this list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_contains = ''  # start with an empty string
        for card in self.deck:
            deck_contains += '\n ' + card.__str__()  
            # Contains the string representation of all the card object.
        return 'The deck contains :-' + deck_contains

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        chosen_card = self.deck.pop()
        # Here a random card is chosen and thrown out of the deck list
        # The card is random because the deck is shuffled.
        return chosen_card


class Hand:
    """
    This class to hold the cards that are in hand of the
    player or the dealer
    """

    def __init__(self):
        self.cards = []
        # start with an empty list to store the cards in hand.
        self.value = 0
        self.aces = 0  # to keep count of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def ace_up_my_sleeve(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    """
    This class is used to initialize the number of chips and
    to adjust the number of chips according to result of the round.
    """

    def __init__(self):
        global balance
        self.balance = balance
        self.bet = 0

    def win_bet(self):
        self.balance += self.bet

    def lose_bet(self):
        self.balance -= self.bet


def take_bet(chips):
    """
    
    :param chips: This is the amount of chips the player bets from his balance.
    This function takes in the number of chips by the user as bet.
    """
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, your bet must be an integer!')
        else:
            if chips.bet > chips.balance:
                print("Sorry, your bet can't exceed "
                      "{}".format(chips.balance))
            else:
                break


def hit(deck, hand):
    """

    :param deck: Deck is all the remaining cards of the 52  cards
    :param hand: This includes all the cards in the hand of the player/dealer.
    This function adds a random card in the players existing hand.
    """
    hand.add_card(deck.deal())
    hand.ace_up_my_sleeve()


def hit_or_stand(deck, hand):
    """

    :param deck: Deck is all the remaining cards of the 52  cards
    :param hand: This includes all the cards in the hand of the player/dealer.
    This function checks whether the player wants to hit or stand.
    """
    global playing  # Referring to the global variable 'playing'

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck, hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


def show_some(player, dealer):
    """
    
    :param player: This is the players hand
    :param dealer: This is the dealers hand
    :return:This function prints all the cards of the player and
    one of the cards of the dealer.
    """
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    """

        :param player: This is the players hand
        :param dealer: This is the dealers hand
        :return:This function prints all the cards of the player and the dealer.
    """
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    '''
    The value of the player's hand goes over 21 and the player goes bust and
    loses the bet.
    '''
    print("Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    '''
    The value of the player's hand is more than the dealer and player wins the bet.
    '''
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    '''
    The value of the dealer's hand goes over 21 and the dealer goes bust and
    loses the bet.Player wins the bet in this case.
    '''
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    '''
    The value of the dealer's hand is more than the player and dealer wins the bet.
    '''
    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    """

    In this case the hand of both the player and the dealer are equal and
    it results in a push.
    """
    print("Dealer and Player tie! It's a push.")

# CODE OF THE GAME

print('\t\t\t\t\t~Welcome to BlackJack~'
          '\n\t\tGet as close to 21 as you can without going over!\n'
          '\n\t\t\t\t\tAces count as 1 or 11.')

# Set up the Player's chips
player_chips = Chips()  # The default value is set to 100

while True:

    # Create & shuffle the deck
    deck = Deck()
    deck.shuffle()

    # Deals two cards to each player and the dealer
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Prompt the Player for their bet:
    take_bet(player_chips)

    # Show the cards:
    show_some(player_hand, dealer_hand)

    while playing:  # This boolean is again used to control the while loop.

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand        
    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        # Test different scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    # Inform Player of their chips balance    
    print("\nPlayer's balance stand at", player_chips.balance)

    # Ask to play again
    if player_chips.balance == 0:
        print("Thanks for playing! You ran out of chips")
        break
    else:
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print("Thanks for playing!")
            break
