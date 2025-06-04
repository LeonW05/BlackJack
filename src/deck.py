import random
import os
from pathlib import Path
import pygame
from card import Card

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Deck:
    def __init__(self, path_media):
        self.cards = []
        self.card_images = {}
        self.load_images(path_media)
        self.create_deck()
        random.shuffle(self.cards)

    def load_images(self, path):
        temp = []
        for png in os.listdir(path):
            if png == "BACK.png" or png == "JOKER.png":
                continue
            new_png = png[:-4]
            temp.append(new_png)
            card = new_png.split('-')

            image = pygame.image.load(os.path.join(path, png))
            image = pygame.transform.scale(image, (140, 180))

            self.card_images[card[0] + card[1]] = image

    def create_deck(self):
        back_path = os.path.join(BASE_DIR, "../media/light/BACK.png")
        back_path = os.path.abspath(back_path)
        back_image = pygame.image.load(back_path)
        back_image = pygame.transform.scale(back_image, (140, 180))

        for key, front_image in self.card_images.items():
            suit = key[-1]
            rank = key[:-1]
            if rank not in ['A', 'J', 'Q', 'K']:
                rank = int(rank)

            self.cards.append(Card(suit, rank, front_image, back_image))
    
    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None
