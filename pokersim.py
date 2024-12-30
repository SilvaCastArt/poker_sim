import random


class Card:
    def __init__(self,suit,rank,points):
        self.suit= suit
        self.rank = rank
        self.points = points
    


class Deck:
    def __init__(self,suits,ranks,points_per_rank):

        self.suits= suits
        self.ranks=ranks
        self.ponts_per_rank = points_per_rank
  
        # Create a list of Card objects
        self.cards = [Card(suit, rank, points_per_rank[ranks[rank]]) for suit in suits for rank in ranks]
        # print(f"The Deck was created : \n {len(self.cards)} cards with {len(self.suits)} different suits \n and {len(self.ranks)} different ranks")

    def deck_info(self):
        print(f"The Deck has {len(self.cards)} cards")

    def show_deck(self):
        for card in self.cards:
            print(f"{self.ranks[card.rank]} of {self.suits[card.suit]}")
    
    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_cards(self,hand_size = 5,pop = True ): #should include number of players
        hand = []
        if len(self.cards)< hand_size :
            print("No more Cards ")
        else:
            # print(f"Drawing Cards...replacement {pop}")
            if pop == True :
                for i in range(0,hand_size):
                    card=self.cards.pop()
                    hand.append(card)
                    #print(f"You drawed {self.ranks[card.rank]} of {self.suits[card.suit]} ")
            else :
                hand  = random.sample(self.cards, hand_size)



        return hand
    

class Hand:
    def __init__(self):
        self.cards=[]
        self.min_length = 5
        self.max_length = 5
        self.diff_ranks = 0 # 0 means not evaluated
        self.hand_value = "NAN"
    
    def print_hand(self,deck):
        for i in range(0,self.max_length):
            print(f"You drawed {deck.ranks[self.cards[i].rank]} of {deck.suits[self.cards[i].suit]} ")
    
    def check_length (self) :
        if len(self.cards) < self.min_length :
            print("Not enough cards")
            return False
        elif len(self.cards) > self.max_length :
            print("Very long hand")
            return False
        else:
            return True
    
    def is_flush(self):
        suits = [card.suit for card in self.cards]
        return len(set(suits)) == 1
    
    def is_straight(self):
        
        straight = False

        ranks = sorted([rank for rank in self.diff_ranks ])
        if ranks == list(range(ranks[0], ranks[-1]+1)):
            straight = True
        elif ranks == [0,9,10,11,12] :
            straight = True


        return straight    

        

    def eval_hand (self):
        valid_hand = False
        valid_hand = self.check_length()
        if valid_hand == True :
            ranks = [card.rank for card in self.cards]
            self.diff_ranks = {rank: ranks.count(rank) for rank in ranks}
            # print(self.diff_ranks)
            count_ranks= len (self.diff_ranks)

            # print(f"{count_ranks} different ranks in hand" )
            # print (len(ranks))

            pairs = [card for card in self.diff_ranks if self.diff_ranks[card] == 2]
            t3ok  = [card for card in self.diff_ranks if self.diff_ranks[card] == 3]
            poker  = [card for card in self.diff_ranks if self.diff_ranks[card] == 4]
            f5ok =  [card for card in self.diff_ranks if self.diff_ranks[card] == 5]



            if count_ranks == self.max_length :
                flush = self.is_flush()
                straight = self.is_straight()
                if flush and straight:
                    # print(f"You have a straight flush")
                    self.hand_value = "SRFL"
                elif flush and not straight : 
                    # print(f"You have a flush")
                    self.hand_value = "FLUSH"
                elif straight and not flush : 
                    # print(f"You have a Straight")
                    self.hand_value = "STR8"
                else:
                    # print(f"You have a High Card")
                    self.hand_value = "HIGHCARD"

            else :
                pairs = [card for card in self.diff_ranks if self.diff_ranks[card] == 2]
                t3ok  = [card for card in self.diff_ranks if self.diff_ranks[card] == 3]
                poker  = [card for card in self.diff_ranks if self.diff_ranks[card] == 4]
                f5ok =  [card for card in self.diff_ranks if self.diff_ranks[card] == 5]

                if len(pairs) > 1 :
                    # print(f"You have two pairs")
                    self.hand_value = "T2PA"
                elif len(pairs) ==  1:
                    if len(t3ok)  == 1 :
                        # print(f"You have a Full house")
                        self.hand_value = "FUHO"
                    else : 
                        # print(f"You have a pair")
                        self.hand_value = "PAIR"
                elif len(pairs) ==  0:
                        if len(t3ok)  == 1 :
                            # print(f"You have Three of a Kind")
                            self.hand_value = "3TOK"
                        elif len(poker)  == 1 :
                            # print(f"You have Poker")
                            self.hand_value = "POKER"
                        elif len(f5ok)  == 1 :
                            # print(f"You have Five of a Kind")
                            self.hand_value = "5FOaK"
                        else :
                            # print("Not a possible hand ERROR: Kind_0001")
                            self.hand_value = "ERROR"
                
        else :
            # print("Could not evaluate hand, correct length ERROR: Length_0001")
            self.hand_value = "ERROR"
        
        return self.hand_value # should be one hot encoded
    

        

def main():

    suits= {0: "Spades", 1: "Hearts", 2: "Clubs", 3: "Diamonds"}
    ranks = {0: "Ace", 1: "2",  2: "3", 3: "4", 4: "5", 5:"6", 6: "7", 7: "8", 8: "9", 9:"10", 10: "Jack", 11: "Queen", 12: "King"}
    points_per_rank = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "Jack": 11, "Queen": 12, "King": 13, "Ace": 14}
    seed=13203
    #points_per_rank = {
    #        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    #        "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}
    
    deck = Deck(suits,ranks,points_per_rank)
    # deck.deck_info()
    #deck.show_deck()
    #random.seed(seed)
    deck.shuffle_deck()

    player1 = Hand()
    if len(deck.cards) >= 5 :
        player1.cards = deck.draw_cards(pop=False)
    # deck.deck_info()
    # player2 = Hand()
    # if len(deck.cards) >= 5 :
    #     player2.cards =  deck.draw_cards(pop=False)


    # deck.deck_info()

    # player1.eval_hand()

    count = 0 
    tries = 5000000
    for  i in range (0,tries):
        player1.cards = deck.draw_cards(pop=False)
        output = player1.eval_hand()
        if output == "3TOK":
            count= count + 1
        if i % 100000 == 1 :
             print(f"{count} of {i} perc: {count/i} ")       





if __name__ == "__main__":
    main()



      