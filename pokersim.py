import random
import numpy as np


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
        self.hand_value = np.zeros(12, dtype=int) # HotEncoded[HIGHCARD_0,PAIR_1,T2PA_2,3TOAK_3,STR8_4,FLUSH_5,FUHAUS_6,POKER_7,STFL_8,ROFL_9,5FOAK_10,ERROR_11]
    
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
        royal = False

        ranks = sorted([rank for rank in self.diff_ranks ])
        if ranks == list(range(ranks[0], ranks[-1]+1)):
            straight = True
        elif ranks == [0,9,10,11,12] :
            straight = True
            royal    = True



        return straight, royal   

        

    def eval_hand (self):
        valid_hand = False
        valid_hand = self.check_length()
        self.hand_value = np.zeros(12, dtype=int)
        
        if valid_hand == True :
            ranks = [card.rank for card in self.cards]
            self.diff_ranks = {rank: ranks.count(rank) for rank in ranks}
            # print(self.diff_ranks)
            count_ranks= len (self.diff_ranks)

            # print(f"{count_ranks} different ranks in hand" )
            # print (len(ranks))

            # HotEncoded[HIGHCARD_0,PAIR_1,T2PA_2,3TOAK_3,STR8_4,FLUSH_5,FUHAUS_6,POKER_7,STFL_8,ROFL_9,5FOAK_10,ERROR_11

            if count_ranks == self.max_length :
                flush = self.is_flush()
                straight,royal = self.is_straight()
                if flush and straight and royal:
                    # print(f"You have a straight flush")
                    self.hand_value[9] = 1
                elif flush and straight and not royal :
                    # print(f"You have a straight flush")
                    self.hand_value[8] = 1

                elif flush and not straight : 
                    # print(f"You have a flush")
                    self.hand_value[5] = 1 
                elif straight and not flush : 
                    # print(f"You have a Straight")
                    self.hand_value[4] = 1
                else:
                    # print(f"You have a High Card")
                    self.hand_value[0] = 1

            else :

                # HotEncoded[HIGHCARD_0,PAIR_1,T2PA_2,3TOAK_3,STR8_4,FLUSH_5,FUHAUS_6,POKER_7,STFL_8,ROFL_9,5FOAK_,ERROR_12

                #check for pairs,
                pairs = [card for card in self.diff_ranks if self.diff_ranks[card] == 2]
                t3ok  = [card for card in self.diff_ranks if self.diff_ranks[card] == 3]
                poker  = [card for card in self.diff_ranks if self.diff_ranks[card] == 4]
                f5ok =  [card for card in self.diff_ranks if self.diff_ranks[card] == 5]

                if len(pairs) > 1 :
                    # print(f"You have two pairs")
                    self.hand_value[2] = 1
                elif len(pairs) ==  1:
                    if len(t3ok)  == 1 :
                        # print(f"You have a Full house")
                        self.hand_value[6] = 1
                    else : 
                        # print(f"You have a pair")
                        self.hand_value[1] = 1
                elif len(pairs) ==  0:
                        if len(t3ok)  == 1 :
                            # print(f"You have Three of a Kind")
                            self.hand_value[3] = 1
                        elif len(poker)  == 1 :
                            # print(f"You have Poker")
                            self.hand_value[7] = 1
                        elif len(f5ok)  == 1 :
                            # print(f"You have Five of a Kind")
                            self.hand_value [10] = 1
                        else :
                            # print("Not a possible hand ERROR: Kind_0001")
                            self.hand_value [11] = 1
                
        else :
            # print("Could not evaluate hand, correct length ERROR: Length_0001")
            self.hand_value[11] = 1
        
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
    
    # deck.shuffle_deck()

    player1 = Hand()
    if len(deck.cards) >= 5 :
        player1.cards = deck.draw_cards(pop=False)
    # deck.deck_info()
    # player2 = Hand()
    # if len(deck.cards) >= 5 :
    #     player2.cards =  deck.draw_cards(pop=False)

    theoretical_probs = {
    "Royal Flush": 0.00000154,
    "Straight Flush": 0.0000139,
    "Four of a Kind": 0.00024,
    "Full House": 0.001441,
    "Flush": 0.00197,
    "Straight": 0.003925,
    "Three of a Kind": 0.021128,
    "Two Pair": 0.047539,
    "One Pair": 0.422569,
    "High Card": 0.501177,
}


    # deck.deck_info()

    # player1.eval_hand()
    np.set_printoptions(precision=5, floatmode='unique')

    count = np.zeros(12, dtype=int)
    tries = 10000000
    for  i in range (1,tries+1):
        player1.cards = deck.draw_cards(pop=False)
        output = player1.eval_hand()
        count += output
        if i % 1000000 == 0 :
            #print(count/i)
            print(f"progress : {i/tries:.0%}")
    print("done")

    estimated_probs_val=count/tries

    estimated_probs = {
    "Royal Flush": estimated_probs_val[9],
    "Straight Flush": estimated_probs_val[8],
    "Four of a Kind": estimated_probs_val[7],
    "Full House": estimated_probs_val[6],
    "Flush": estimated_probs_val[5],
    "Straight": estimated_probs_val[4],
    "Three of a Kind": estimated_probs_val[3],
    "Two Pair":estimated_probs_val[2],
    "One Pair": estimated_probs_val[1],
    "High Card": estimated_probs_val[0],
}




if __name__ == "__main__":
    main()



      