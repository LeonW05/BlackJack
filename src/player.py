class Player:
    def __init__(self):
        self.hand = []
        self.points = 0
        self.turn = True

    def add_card(self, card):
        self.hand.append(card)

    def reset_hand(self):
        self.hand.clear()
    
    def get_total(self):
        total = 0
        for card in self.hand:
            if card.rank == 'A':
                if total + 11 < 21:
                    total += 11
                else:
                    total += 1
            elif card.rank in ['J', 'Q', 'K']:
                total += 10
            else:
                total += card.rank
        
        return total
    
    def hit(self, deck):
        new_card = deck.deal_card()
        if new_card:
            self.hand.append(new_card)
        self.points = self.get_total()

    def draw_hand(self, screen, x, y):
        for i, card in enumerate(self.hand):
            card.face_up = True
            if x + i * 50 < 400:
                card.draw(screen, x + i * 65, y)