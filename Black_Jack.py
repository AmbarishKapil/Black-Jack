import math
import random
from colorama import init, Fore, Style
init()


# Global Variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True
number_of_players = None

color = []
color.append(Fore.MAGENTA)
color.append(Fore.CYAN)
color.append(Fore.BLUE)
color.append(Fore.GREEN)
color.append(Style.DIM + Fore.YELLOW)
color.append(Fore.RED)
color.append(Style.BRIGHT+Fore.YELLOW)

while True:
    try:
        print(color[6] + "The table has provision for 1-5 players and a dealer, how many players are joining? :", end=" ")
        number_of_players = int(
            input())
    except ValueError:
        print("Invalid Input, please try again.")
        continue

    if number_of_players > 5 or number_of_players < 1:
        print("A maximum of 5 and a minimum of 1 player can play on this table.")
    else:
        print("")
        print("Ladies and Gentleman, Welcome to Black Jack!")
        break

number_of_decks = number_of_players


# Classes(attribute and methods)
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.card_rank()]

        if card.rank == 'Ace':
            self.aces += 1

    def remove_card(self):
        c = self.cards.pop()
        self.value -= values[c.card_rank()]

        if c.card_rank() == 'Ace':
            self.aces -= 1

        return c

    def can_split(self):
        if self.cards[0].card_rank() == self.cards[1].card_rank():
            return True

        return False

    def card_splits(self, chip, deck):
        if chip.bet > chip.total:
            chip.bet += chip.total
            chip.total = 0
        else:
            chip.total -= chip.bet

        split_hand_list = []
        first_split_hand = Hand()
        second_split_hand = Hand()

        first_split_hand.add_card(self.remove_card())
        first_split_hand.add_card(deck.deal())

        if first_split_hand.bust():  # this is a corner case if both initial cards were Aces and the last drawn card was also a Ace
            first_split_hand.adjust_for_ace()

        for card in first_split_hand.cards:
            print(card)

        split_hand_list.append(first_split_hand)

        second_split_hand.add_card(self.remove_card())
        second_split_hand.add_card(deck.deal())

        if second_split_hand.bust():  # this is a corner case if both initial cards were Aces and the last drawn card was also a Ace
            second_split_hand.adjust_for_ace()

        print("")
        for card in second_split_hand.cards:
            print(card)

        split_hand_list.append(second_split_hand)

        return split_hand_list

    def can_double_down(self):
        if self.value >= 9 and self.value <= 11:
            return True

        return False

    def double_down(self, chip, deck):
        if chip.bet > chip.total:
            ret_chip = chip.total
            chip.bet += chip.total
            chip.total = 0
        else:
            ret_chip = chip.bet
            chip.total -= chip.bet

        self.add_card(deck.deal())

        print(f"added {self.cards[len(self.cards)-1]}")

        if self.bust():
            self.adjust_for_ace()

        return ret_chip

    def hit_or_stand(self, deck):
        while True:
            if self.value == 21:
                print("Black Jack!!!")
                break

            h_or_s = input("press h to hit and s to stand:")

            if h_or_s.lower() == 'h':
                print('The player has chosen to hit...')
                self.add_card(deck.deal())
                print(f"added {self.cards[len(self.cards)-1]}")
                if self.bust():
                    self.adjust_for_ace()
                    if self.bust():
                        print("Player Busted")
                        break
            elif h_or_s.lower() == 's':
                print('The player has chosen to stand...')
                break
            else:
                print('Invalid Response, Try again.')

            print(f"The value of the is : {self.value}")

        # complete the action here in this func itself by passing the currrent hand object

    def adjust_for_ace(self):
        if self.aces != 0:
            if self.value > 21:
                self.value -= 10
                self.aces -= 1

    def bust(self):
        if self.value > 21:
            return True
        return False


class Deck:
    def __init__(self):
        self.deck = []

        for i in range(0, number_of_decks, 1):
            for suit in suits:
                for rank in ranks:
                    c = Card(suit, rank)
                    self.deck.append(c)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def card_rank(self):
        return self.rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Chips:
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def take_bet(self):
        while True:
            try:
                total_bet = int(input())
            except ValueError:
                print("Invalid Input, please try again.")
                continue

            if total_bet > self.total:
                print("Not enough chips!")
            else:
                self.bet = total_bet
                break

        self.total -= self.bet
        return self.bet

    def add_chips(self, sum):
        self.total += sum


class Game:

    def show_some(self, hands):
        print(color[0] + "Dealer's cards")
        print(color[0] + "xxx HIDDEN CARD xxx")
        print(hands[0].cards[1])
        print("")

        for i in range(1, number_of_players+1):
            print(color[i] + f"Player{i}'s cards")
            for card in hands[i].cards:
                print(card)
            print("")

    def show_all(self, hands):
        hand_index = 0
        for hand in hands:
            if isinstance(hand, list):
                for h in hand:
                    print(color[hand_index] + f"Player{hand_index}'s cards:")

                    for card in h.cards:
                        print(card)
                    print("")
                hand_index += 1
                continue

            if hand_index == 0:
                print(color[hand_index] + "Dealer's cards")
            else:
                print(color[hand_index] + f"Player{hand_index}'s cards'")

            for card in hand.cards:
                print(card)
            print("")
            hand_index += 1

    def show_player_cards(self, hand):
        for card in hand.cards:
            print(card)


# main equivalent code
# total_chips_on_the_bet
chip_list = []  # keeps track of chips of the players

# Initialising chip_list
for _ in range(number_of_players):
    chip = Chips()
    chip_list.append(chip)

while playing:
    total_chips_on_the_bet = 0
    # Players waging bets
    pl_index = 1
    for chip in chip_list:
        print(color[pl_index])
        print(f"How many chips do Player{pl_index} want to bet? :", end=" ")
        bet = chip.take_bet()
        total_chips_on_the_bet += bet
        pl_index += 1

    # the dealer will add the mean of total Chips
    total_chips_on_the_bet += math.ceil(total_chips_on_the_bet/number_of_players)

    # The dealer shuffles and deales the cards
    print("")
    print(color[6] + "The Dealer is shuffling the cards...")
    deck = Deck()
    deck.shuffle()

    print(color[6] + "The Dealer is dealing the cards...")
    print("")
    hand_list = []  # there are number_of_players + 1 hands and as convension let the first hand be the dealer's hand
    for _ in range(number_of_players+1):
        hand = Hand()
        hand_list.append(hand)

    for hands in hand_list:
        for _ in range(2):
            hands.add_card(deck.deal())

    # showing the dealed cards
    game = Game()
    game.show_some(hand_list)

    for player in range(1, number_of_players+1):
        print(color[player] + f"player{player}'s turn----------------------------------------")
        print(f"player{player}'s cards:")
        game.show_player_cards(hand_list[player])
        if hand_list[player].can_split():
            while True:
                will_split = input("Will the player like to split? 'y' for yes and 'n' for no:")

                if will_split.lower() == 'y':
                    split_hand_list = hand_list[player].card_splits(chip_list[player-1], deck)
                    hand_list.pop(player)
                    hand_list.insert(player, split_hand_list)
                    break
                elif will_split.lower() == 'n':
                    hand_list[player].hit_or_stand(deck)
                    break
                else:
                    print("Invalid input, please try again.")
        elif hand_list[player].can_double_down():
            while True:
                will_double_down = input(
                    "Will the player like to double_down? 'y' for yes and 'n' for no:")

                if will_double_down.lower() == 'y':
                    total_chips_on_the_bet += hand_list[player].double_down(
                        chip_list[player-1], deck)
                    break
                elif will_double_down.lower() == 'n':
                    hand_list[player].hit_or_stand(deck)
                    break
                else:
                    print("Invalid Input, please try again.")
        else:
            hand_list[player].hit_or_stand(deck)

    # dealer's play
    if hand_list[0].value < 17:
        hand_list[0].add_card(deck.deal())
        if hand_list[0].value > 21:
            hand_list[0].adjust_for_ace()

    game.show_all(hand_list)

    # Who won?
    winning_value = 0
    winner_index_list = []

    for player in range(0, number_of_players+1):
        if isinstance(hand_list[player], list):
            for lr in range(2):  # lr here means left and right hand
                if hand_list[player][lr].value > 21:
                    continue

                if hand_list[player][lr].value == winning_value:
                    winner_index_list.append(player)
                elif hand_list[player][lr].value > winning_value:
                    winning_value = hand_list[player][lr].value
                    winner_index_list.clear()
                    winner_index_list.append(player)
        else:
            if hand_list[player].value > 21:
                continue

            if hand_list[player].value == winning_value:
                winner_index_list.append(player)
            elif hand_list[player].value > winning_value:
                winning_value = hand_list[player].value
                winner_index_list.clear()
                winner_index_list.append(player)

    # Chips exchange
    try:
        total_won = math.floor(total_chips_on_the_bet/len(winner_index_list))
    except ZeroDivisionError:
        total_won = 0

    for player in winner_index_list:
        if player == 0:
            continue
        else:
            chip_list[player-1].add_chips(total_won)

    print(color[6] + "Chips for each player...If atleast one player is out of chips the game ends.")
    for player in range(number_of_players):
        print(color[player] + f"player {player+1} total chips stand at {chip_list[player].total}")
        if chip_list[player].total <= 0:
            playing = False

    if not playing:
        break

    # Willplayagain
    while True:
        print(color[6] + "Type y to continue play, n to stop :", end=" ")
        y_or_n = input()

        if y_or_n.lower() == 'n':
            playing = False
            break
        elif y_or_n.lower() == 'y':
            break
        else:
            print("Invalid Input, please try again.")

    print(Style.RESET_ALL)

    if not playing:
        break
