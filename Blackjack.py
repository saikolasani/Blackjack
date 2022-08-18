import random

#Creating the Deck
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#Creating Classes for the Game

#Card Class
class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

#Deck Class
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    
    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

#Hand Class
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
    def adjust_for_ace(self):
        
        # If total value > 21 and I still have an ace
        # change the value of an ace to 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

#Chips Class
class Chips:
    
    def __init__(self,total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total = self.total+self.bet
    
    def lose_bet(self):
        self.total = self.total-self.bet

#Functions needed to run the game

#Betting
def take_bet(chips):
    
     while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

#Hit Function
def hit(deck,hand):
    hand.add_card(deck.deal())

#Player chooses to hit or stand
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input('Hit or Stand? Enter h or s') # Hit or stand
        
        if x[0].lower() == 'h':
            hit(deck,hand)
        
        elif x[0].lower() == 's':
            print('Player Stands')
            playing = False
            
        else:
            print('Sorry, please try again')
        break

#Display the cards
def show_some(player,dealer):
    
    # Show only one of the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])
    # Show all of the player's hand/cards
    print("Player's Hand")
    for card in player.cards:
        print(card)
def show_all(player,dealer):
    # Show all of the dealer's cards
    print("\n Dealer's Hand: ")
    for card in dealer.cards:
        print(card)
    print("\n Dealer's hand: ",*dealer.cards,sep='\n')
    print(f"Value of Dealer's hand is: {dealer.value}")
    # Show all of the player's cards
    print("Player's Hand")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand is: {player.value}")

#End of the game situations
def player_busts(player,dealer,chips):
    print('BUST PLAYER!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('PLAYER WINS!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('PLAYER WINS! DEALER BUSTED')
    
def dealer_wins(player,dealer,chips):
    print('DEALER WINS!')
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! PUSH")

#Playing the Game
while True:
    # Print an opening statement

    print('Welcome to BlackJack')
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    # Inform Player of their chips total 
    print(f"\n Player total chips are at: {player_chips.total}")
    # Ask to play again
    new_game = input('Would you like to play again? y/n')
    if new_game[0].lower()=='y':
        playing = True
    else:
        print('Thank you for playing!')
        break
