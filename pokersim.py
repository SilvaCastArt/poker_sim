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
        print(f"The Deck was created : \n {len(self.cards)} cards with {len(self.suits)} different suits \n and {len(self.ranks)} different ranks")

    def deck_info(self):
        print(f"The Deck has {len(self.cards)} cards")

    def show_deck(self):
        for card in self.cards:
            print(f"{self.ranks[card.rank]} of {self.suits[card.suit]}")
    
    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_cards(self,hand_size = 5):
        hand = []
        if len(self.cards)< 1 :
            print("No more Cards ")
        else:
            print("Drawing Cards...")
            for i in range(0,hand_size):
                card=self.cards.pop()
                hand.append(card)
                print(f"You drawed {self.ranks[card.rank]} of {self.suits[card.suit]} ")
        return hand

class Hand:
    def __init__(self):
        self.cards=[]
        self.min_length = 5
        self.max_length = 5
        self.diff_ranks = 0 # 0 means not evaluated
    
    def check_length (self) :
        if len(self.cards) < self.min_length :
            print("Not enough cards")
            return False
        elif len(self.cards) > self.max_length :
            print("Very long hand")
            return False
        else:
            return True

    def eval_hand (self):
        valid_hand = False
        valid_hand = self.check_length()
        if valid_hand == True :
            ranks = [card.rank for card in self.cards]
            self.diff_ranks = {rank: ranks.count(rank) for rank in ranks}
            self.diff_ranks = len (self.diff_ranks)

            print(f"{self.diff_ranks} different ranks in hand" )
            print (len(ranks))
        else :
            print("Could not evaluate hand, correct length")
    
    def check_exact_pair(self):
        pass


        

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
    deck.deck_info()
    #deck.show_deck()
    random.seed(seed)
    deck.shuffle_deck()

    player1 = Hand()
    if len(deck.cards) >= 5 :
        player1.cards = deck.draw_cards()
    deck.deck_info()
    player2 = Hand()
    if len(deck.cards) >= 5 :
        player2.cards = deck.draw_cards()


    deck.deck_info()

    player1.eval_hand()

    




if __name__ == "__main__":
    main()



      