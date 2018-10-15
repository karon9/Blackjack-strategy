import tkinter
import random
import pandas as pd
import numpy as np
#6デック
#double,surrenderはsplit後はできない


class Player(object):
    # this creates a player object. Suitable for player & dealer.
    def __init__(self, cash=0, name='', hand=[], bet=0, blackjack=False):
        self.cash = 0
        self.name = ''
        self.originalname = ''
        self.hand = []
        self.isasplit = False
        self.bet = 0
        self.blackjack = False


class Card(object):
    def __init__(self):
        self.suit = ''
        self.rank = ''
        self.value_hard = 0
        self.value_soft = 0

    def getCard(self):
        return self.rank + " of " + self.suit

class Deck(object):
    def __init__(self):
        self.stack = []
        self.created_size = 0
        self.standard_size = 52

    def size(self):
        return len(self.stack)


class Table(object):
    def __init__(self):
        self.players = []
        self.deck = 0
        self.std_deck_size = 0
        self.dealprogression = 0



def setup():
    global table
    table = Table()
    # sets up the game. Player name, deck number, and starting funds are specified here
    print("Welcome to Python Blackjack.")
    # set up dealer
    dealer = Player()
    dealer.name = 'Dealer'
    table.players.append(dealer)

    #Playername
    newPlayer = Player()
    newPlayer.name = 'Charon'
    table.players.append(newPlayer)

    # decks
    print("Thanks")
    print("Please indicate the number of decks you would like to use in play.")
    deck_num = 1
    table.std_deck_size = deck_num
    table.deck = newdeck(deck_num)

    # starting funds
    print("Please indicate the level of starting funds you would like players to have.")
    startcash = 10000
    print("You will have $", startcash, "to begin. Good luck!")
    i = 0
    for player in table.players:
        if player.name != 'Dealer':
            player.cash = startcash

    table.counting = -2


def newdeck(n=1):
    suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
    ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    hard_values = [11, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soft_values = [1, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    std_deck = Deck()
    finaldeck = Deck()

    card_data = list(zip(ranks, hard_values, soft_values))
    #ジェネレーターの仕組み、zipをlistに変えたよ！！

    for i in suits:
        for j in card_data:
            newCard = Card()
            newCard.suit = i
            newCard.rank = j[0]
            newCard.value_hard = j[1]
            newCard.value_soft = j[2]
            std_deck.stack.append(newCard)

    std_deck.size = len(std_deck.stack)
    #deckの数もここからも増やせるよ！！
    finaldeck.stack = std_deck.stack * n
    finaldeck.created_size = len(finaldeck.stack)
    random.shuffle(finaldeck.stack)
    #print (finaldeck.size(), finaldeck.created_size, finaldeck.standard_size,std_deck.size )    #a little debugging
    return finaldeck


def deal():
    global table

    # first: Check if there are enough cards to go around
    print(table.deck.size(),table.dealprogression)

    if  table.deck.size() < 26:  # not happy about this arbitrary integer.
        print("Deck needs to be reshuffled")
        table.deck = newdeck(table.std_deck_size)

    playerCount = 2
    #二人で固定
    i = 0
    for player in table.players:
        player.hand.append(table.deck.stack.pop(i))
        table.dealprogression += 1
        #最初に0を引くのでまた0スタート
        player.hand.append(table.deck.stack.pop(i + playerCount - table.dealprogression))
        if value(player.hand) == 21:
            player.blackjack = True


def hit(cards):
    global table
    cards.append(table.deck.stack.pop(0))
    print("Hit results in  ", cards[-1].getCard())


def doubledown(player):
    player.cash = player.cash - player.bet
    player.bet = player.bet * 2
    print("You have chosen to double down. Your bet is now $", player.bet)
    hit(player.hand)
    print("Your cards are:")
    for item in player.hand:
        print(item.getCard())
    print("The value is now", value(player.hand))
    if value(player.hand) > 21:
        print("You busted! You lose.")


def surrender(player):
    print("You have surrendered.")
    player.cash += player.bet / 2
    print("You sacrificed $", player.bet / 2, "to withdraw.")


def resolve():
    global table

    def win(player, con=''):
        if con == 'bust':
            print("Dealer busts! You win!!!")
            print("You win $", str(player.bet))
            player.cash += 2 * player.bet
        elif con == 'BJ':
            print("You won with a blackjack! Blackjack pays 3:2")
            print("You win $", str((3. / 2) * player.bet))
            player.cash += (5. / 2) * player.bet
        else:
            print("You won!")
            print("You win $", str(player.bet))
            player.cash += 2 * player.bet

    def lose(player):
        print("You lost! You forfeit your bet of $", str(player.bet))

    def push(player):
        print("Push! You recoup your bet of $", str(player.bet))
        player.cash += player.bet

    # set up some special player objects to make life easier
    dealer = table.players[0]
    player_list = []
    for player in table.players:
        if player.name != 'Dealer':
            player_list.append(player)

    # keep a wall of text from happnin
    print("To continue, type 'ok'")
    check = ''
    while check != 'ok':
        check = 'ok'
        if check != 'ok':
            print("you MUST type in 'ok' to continue")

    print('-------------------------------------------------------------------------------------')

    # if all players busted, there is no reason to continue
    allbust = True
    for player in player_list:
        if value(player.hand) <= 21:
            allbust = False
    if allbust == True:
        print("All players busted! Dealer wins.")

    else:
        ################
        print("The dealer reveals his other card:")
        print(dealer.hand[0].getCard(), "\n")
        print("The value of his hand is", value(dealer.hand), "\n")
        if dealer.blackjack == True:
            print("Dealer has Blackjack! Uh-oh...")

        while value(dealer.hand) < 17:
            print("The dealer hits until he is at or equal to 17.")
            hit(dealer.hand)
            print("Dealer is now at", value(dealer.hand))
        ################

        # cases
        for player in player_list:
            print("\nResults for " + player.name)
            # player busting == instalose, regardless of dealer situation
            if value(player.hand) > 21:
                print(player.name + " busted.")
                lose(player)
            # dealer busts
            elif value(dealer.hand) > 21:
                win(player, 'bust')

            # the rest of the cases
            elif dealer.blackjack:
                if player.blackjack:
                    push(player)
                else:
                    lose(player)  # dealer BJ trumps anything but BJ
            else:
                if player.blackjack:  # check trump condition
                    win(player, 'BJ')  # special win condition, 3:2 for BJ
                elif value(player.hand) > value(dealer.hand):  # player has higher val
                    win(player)
                elif value(player.hand) < value(dealer.hand):  # player has lower val
                    lose(player)
                else:
                    push(player)  # true tie

    # gotta get rid of any splits & clean up bets
    done_list = []
    for player in player_list:
        if player.isasplit:
            done_list.append(player)
            # if a win, find original hand & give split's bet to it
            if player.name != 'Charon':
                if player.originalname == 'Charon':
                    table.players[1].cash += player.cash
        elif player.originalname:
            player.name = player.originalname
    for item in done_list:
        table.players.remove(item)


def split(player):
    global table
    if player.hand[0].rank == 'Ace' and player.hand[1].rank == 'Ace':
        print("\n\n\nSplit: you now play as if you had two hands, and your bet doubles.")
        player.cash -= player.bet

        # creates the split player, a 'ghost' player item
        split_ghost = Player()
        split_ghost.name = player.name + """'s 2nd split hand"""
        split_ghost.originalname = 'Charon'
        split_ghost.isasplit = True
        split_ghost.bet = player.bet
        split_ghost.hand.append(player.hand.pop(1))

        # insert the split player into the table, so resolution can take place right.
        table.players.append(split_ghost)
        player.originalname = 'Charon'
        player.name = player.name + """'s 1st split hand"""

        print("You will now play your first 'hand'.")
        hit(player.hand)


        print("You will now play your second 'hand'.")
        hit(split_ghost.hand)

    else:
        print("\n\n\nSplit: you now play as if you had two hands, and your bet doubles.")
        player.cash -= player.bet

        # creates the split player, a 'ghost' player item
        split_ghost = Player()
        split_ghost.name = player.name + """'s 2nd split hand"""
        split_ghost.originalname = 'Charon'
        split_ghost.isasplit = True
        split_ghost.bet = player.bet
        split_ghost.hand.append(player.hand.pop(1))

        # insert the split player into the table, so resolution can take place right.
        table.players.append(split_ghost)
        player.originalname = 'Charon'
        player.name = player.name + """'s 1st split hand"""

        print("You will now play your first 'hand'.")
        hit(player.hand)
        player_action(player)

        print("You will now play your second 'hand'.")
        hit(split_ghost.hand)
        player_action(split_ghost)


def main():
    global table
    setup()
    xyzzy = 0
    count = 0
    while xyzzy == 0:
        count += 1

        print("You must bet before the deal.\n")
        for player in table.players:
            if player.name == 'Dealer':
                continue
            print(player.name, ": You must bet. What is your bet?")
            while player.bet == 0.:
                player.bet = 100
                if player.bet > player.cash:
                    print("You bet too much, can't bet more than you have.")
                    player.bet = 0
            player.cash -= player.bet

        deal()

        print("\nThe Dealer shows", table.players[0].hand[1].getCard(), "\n")

        # begin the action
        for player in table.players:
            # weed out the 2 cases we don't want any actions
            if player.name == 'Dealer':
                continue
            if player.isasplit == True:  # split actions all happen in subfunctions
                continue
            print("Action is to player", player.name)
            print("Player must check in by typing 'ok'")
            check = ''
            while check != 'ok':
                check = 'ok'
                if check != 'ok':
                    print("you MUST type in 'ok' to continue")
            player_action(player)
        resolve()
        xyzzy = playagain()

    print("Thank you for playing Python Blackjack. See you next time!")
    return 0


def playagain():
    global table
    done_list = []
    for i in range(1, len(table.players)):
        yn = ''
        while yn == '':
            player = table.players[i]
            print(player.name + ": You have $", player.cash, "available to bet with.")
            print("Would you like to play again? (y/n)")
            yn = 'y'
            if yn == 'y':
                # reset everything
                player.bet = 0
                player.hand = []
                player.blackjack = False
                player.splitbet = 0
                player.splithand = []
            elif yn == 'n':
                print("Thank you for playing, " + player.name)
                done_list.append(table.players[i])
            else:
                print("Please input y or n only.")
                yn = ''

    # reset everything for another go
    # reset the dealer
    table.players[0].hand = []
    table.players[0].blackjack = False
    # reset the deal progression
    table.dealprogression = 0
    # get rid of unwanted players
    for item in done_list:
        table.players.remove(item)
    # check to see if there are any players left
    if len(table.players) == 1 or table.players[1].cash < 100:
        return 1
    else:
        return 0


def value(cards):
    # total is a list of every possible sum
    # at the end total will have 2**a sums, where a is the number of aces in the hand
    total = [0]
    for card in cards:
        if card.value_hard == card.value_soft:  # not an ace
            # add the hard value to each possible sum
            total = [i + card.value_hard for i in total]
        else:  # the card is an ace, which doubles the list length
            soft_totals = [i + card.value_soft for i in total]
            hard_totals = [i + card.value_hard for i in total]
            total = soft_totals + hard_totals
    # total now has every possible sum
    if min(total) > 21:
        # every sum is greater than 21; insta-bust
        return min(total)
    else:
        # only keep values less than or equal to 21 using an anonymous function
        total = filter(lambda x: x <= 21, total)
        return max(total)


def player_action(player):
    global table
    cardslist = ''
    for item in player.hand:
        while len(cardslist) != 0:
            cardslist += ', '
            break
        cardslist += item.getCard()

    print("\nYour cards are:", cardslist)
    print("Your hand value is", value(player.hand))

    # check for a split
    if player.hand[0].rank == player.hand[1]:
            splitCheck = True
    else:
        splitCheck = False

    # begin decisionmaking tree
    decision = 0
    while decision == 0:
        decision = decisiontree(player, split=splitCheck)
        if decision == 1:
            hit(player.hand)
            cardslist = ''
            for item in player.hand:
                while len(cardslist) != 0:
                    cardslist += ', '
                    break
                cardslist += item.getCard()
            print("Your cards are now:", cardslist)
            print("Your hand value is", value(player.hand))
            if value(player.hand) == 21:
                print("You should stand.")
                decision = 0
            elif value(player.hand) > 21:
                print("You busted! You lose.")
                break
            else:
                decision = 0

        elif decision == 2:
            print(player.name + " has elected to stand.")
            if player != table.players[-1]:
                print("Play now passes to the next player.")
            break
        elif decision == 3:
            if player.bet > table.players[1].cash - player.bet:
                print("You can't double down, you don't have enough money.")
                hit(player.hand)
                cardslist = ''
                for item in player.hand:
                    while len(cardslist) != 0:
                        cardslist += ', '
                        break
                    cardslist += item.getCard()
                print("Your cards are now:", cardslist)
                print("Your hand value is", value(player.hand))
                if value(player.hand) == 21:
                    print("You should stand.")
                    decision = 0
                elif value(player.hand) > 21:
                    print("You busted! You lose.")
                    break
                else:
                    decision = 0
            else:
                doubledown(player)
                break
        elif decision == 4:
            yn = ''
            while yn == '':
                print("""Surrender: Gives up a half bet & retires ("folds")""")
                print("Are you sure?")
                yn = 'y'
                if yn == 'y':
                    surrender(player)
                    break
        elif decision == 5 and splitCheck == True:
            split(player)
        else:
            decision = 1


def decisiontree(player, split=False):
    def option_text(n=2):
        # Largest possible tree "Press 1 to hit, 2 to stand, 3 to double down, 4 to surrender, 5 to split."
        option_list = ['1 to hit', ', 2 to stand', ', 3 to double down', ', 4 to surrender', ', 5 to split']
        str = ''
        for i in range(len(option_list)):
            while i < n:
                str = str + option_list[i]
                break
        print("Press " + str + ".")

    ## check for 1st time in this function
    firstpass = False
    if len(player.hand) == 2 and len(table.players) == 2:
        firstpass = True

    # Largest possible tree "Press 1 to hit, 2 to stand, 3 to double down, 4 to surrender, 5 to split."
    decision = strategy(player)
    while decision == 0:
        if split == True:
            option_text(n=5)
            if decision > 5:
                print("1 thru 5 only.")
        elif firstpass == True:
            option_text(n=4)
            if decision > 4:
                print("1 thru 4 only.")
        else:
            option_text(n=2)
            if decision  == 3:
                print("hitにしとくね")
                decision = 1
            if decision == 4:
                print("standにしとくね")
                decision = 2

    return decision

def strategy(player):
    global table

    def value_soft(cards):
        #Aceを1と置いた時のvalue
        total = [0]
        for card in cards:
            if card.value_hard == card.value_soft:  # not an ace
                # add the hard value to each possible sum
                total = [i + card.value_hard for i in total]
            else:  # the card is an ace, which doubles the list length
                soft_totals = [i + card.value_soft for i in total]
                total = soft_totals
        # total now has every possible sum
        if min(total) > 21:
            # every sum is greater than 21; insta-bust
            return min(total)
        else:
            # only keep values less than or equal to 21 using an anonymous function
            total = filter(lambda x: x <= 21, total)
            return max(total)

    data = pd.read_csv("blackjack.csv",index_col=0 ,encoding="SHIFT-JIS")
    dealerhand = str(table.players[0].hand[1].value_hard)
    if(dealerhand == '1' or dealerhand == '11'):
        dealerhand = 'A'
    if player.blackjack != True:
        if player.hand[0].rank == 'Ace' and player.hand[1].rank == 'Ace':
            myhand = 'A,A'
        elif 'Ace' in player.hand  and (value_soft(player.hand) - 1) != 10:
            myhand = 'A,' + str(value_soft(player.hand) - 1)
        elif player.hand[0].rank == player.hand[1].rank:
            myhand = str(player.hand[0].value_soft)+ ',' + str(player.hand[1].value_soft)
        elif value(player.hand) <= 8:
            myhand = '~8'
        elif value(player.hand) >= 17:
            myhand = '17~21'
        else:
            myhand = str(value(player.hand))
    else:
        myhand = '17~21'

    play = data.ix[myhand,dealerhand]
    if play == 'H':
        return 1
    if play == 'ST':
        return 2
    if play == 'D':
        return 3
    if play == 'SR':
        return 4
    if play == 'SP':
        return 5


def glaf():
    global table
    root = tkinter.Tk()
    root.title("Blackjack")
    x = 1400
    y = 700
    C = tkinter.Canvas(root,bg="black",height = y,width = x)

    C.create_line(50,50,50,y -50,fill = "white")
    C.create_line(50,y - 50,x-50,y-50,fill="white")

    for i in range(11):
        C.create_text(25,y - 50 - i * 60,fill = "white" , font = "Helvetica 10",text = str(i * 2500))

    for i in range(14):
        C.create_text(50 + i * 100,y - 25 , fill = "white",font = "Helvetica 10",text = str(i * 1000))

    color = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']

    def legend():
        global table
        setup()
        xyzzy = 0
        count = 0
        money = 0
        while xyzzy == 0 and count < 13000 and money <= 25000:
            money = table.players[1].cash
            print("You must bet before the deal.\n")
            for player in table.players:
                if player.name == 'Dealer':
                    continue
                print(player.name, ": You must bet. What is your bet?")
                while player.bet == 0.:
                    player.bet = 100
                    if player.bet > player.cash:
                        print("You bet too much, can't bet more than you have.")
                        player.bet = 0
                player.cash -= player.bet

            deal()

            print("\nThe Dealer shows", table.players[0].hand[1].getCard(), "\n")

            # begin the action
            for player in table.players:
                # weed out the 2 cases we don't want any actions
                if player.name == 'Dealer':
                    continue
                if player.isasplit == True:  # split actions all happen in subfunctions
                    continue
                print("Action is to player", player.name)
                print("Player must check in by typing 'ok'")
                check = ''
                while check != 'ok':
                    check = 'ok'
                    if check != 'ok':
                        print("you MUST type in 'ok' to continue")
                player_action(player)
            resolve()
            ######################################
            money_1 = table.players[1].cash
            if money_1 > 0:
                C.create_line(50 + count / 10,y - 50 - money/2500 * 60,50 + (count + 1) / 10 ,y - 50 - money_1/2500 * 60, fill = color[i])

            C.pack()
            count = count + 1
            money = money_1

            root.update()
            ###########################################
            xyzzy = playagain()
        if money == 0:
            C.create_text(50 + count / 10, y - 40, fill="white", font="Helvetica 10", text="$0" + " count:" + str(count))
        else:
            C.create_text(50 + count / 10, y - 50 - money / 2500 * 60, fill="white", font="Helvetica 10",
                          text="$" + str(money) + " count:" + str(count))

        print("Thank you for playing Python Blackjack. See you next time!")

    for i in range(10):
            legend()

    return root.mainloop()
glaf()


