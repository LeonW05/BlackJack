class Card:
    def __init__(self, suit, rank, front_image, back_image):
        self.suit = suit
        self.rank = rank
        self.front_image = front_image
        self.back_image = back_image
        self.face_up = True

    def draw(self, screen, x, y):
        if self.face_up is True:
            screen.blit(self.front_image, (x, y))
        else:
            screen.blit(self.back_image, (x, y))
    
    def flip(self):
        if self.face_up is True:
            self.face_up = False
        else:
            self.face_up = True
