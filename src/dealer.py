from player import Player

class Dealer(Player):
    def __init__(self):
        self.hand = []
        self.points = 0
        self.turn = False
    
    def draw_hand(self, screen, x, y):
        for i, card in enumerate(self.hand):
            if x + i * 50 < 200:
                card.draw(screen, x + i * 65, y)

    def hit(self, deck):
        if self.points < 17:
            new_card = deck.deal_card()
            if new_card:
                self.hand.append(new_card)
                self.hand[-1].face_up = True
                self.points = self.get_total()
    
    def get_first_card(self):
        if self.hand:
            if self.hand[0].rank == 'A' and self.points + 11 <= 21:
                return 11
            elif self.hand[0].rank == 'A' and self.points + 11 > 21:
                return 1
            elif self.hand[0].rank in ['J', 'Q', 'K']:
                return 10
            else:
                return int(self.hand[0].rank)