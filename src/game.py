import pygame
import os
from pathlib import Path
from deck import Deck
from player import Player
from dealer import Dealer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BlackJack:
    def __init__(self, screen):
        self.screen = screen
        path = os.path.join(BASE_DIR, "../media/light")
        self.assets_path = os.path.abspath(path)
        self.deck = Deck(self.assets_path)
        self.player = Player()
        self.dealer = Dealer()
        self.dealer_draw_time = 0
        self.button_hit = pygame.Rect(50, 720, 120, 50)
        self.button_stand = pygame.Rect(240, 720, 120, 50)
        self.button_restart = pygame.Rect(430, 720, 120, 50)
        self.end_game = False
        self.start_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.button_hit.collidepoint(mouse_pos) and not self.end_game:
                    self.player.hit(self.deck)
                elif self.button_stand.collidepoint(mouse_pos) and not self.end_game:
                    self.player.turn = False
                    self.dealer.turn = True
                    self.dealer_draw_time = pygame.time.get_ticks()
                elif self.button_restart.collidepoint(mouse_pos):
                    self.end_game = False
                    self.start_game()
        return True

    def start_game(self):
        self.deck = Deck(self.assets_path)
        self.player.reset_hand()
        self.dealer.reset_hand()

        for _ in range(2):
            self.player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())

        # Set all dealer cards face up, then set the first one face down
        for card in self.dealer.hand:
            card.face_up = True
        if self.dealer.hand:
            self.dealer.hand[1].face_up = False

        self.player.points = self.player.get_total()
        self.dealer.points = self.dealer.get_total()

    def update(self):
        if self.player.points > 21 or self.player.points == 21:
            self.end_game = True

        # Reveal dealer's cards if dealer's turn is over or game is over
        if self.dealer.turn:
            for card in self.dealer.hand:
                card.face_up = True

        # Dealer's turn logic with delay
        if self.dealer.turn and not self.end_game:
            now = pygame.time.get_ticks()
            if now - self.dealer_draw_time >= 500:
                if self.dealer.points < 17:
                    self.dealer.hit(self.deck)
                    self.dealer_draw_time = now
                else:
                    self.dealer.turn = False
                    self.end_game = True
        
        '''if self.end_game is True:
            self.check_winner()'''

    def draw_winner(self):
        message = ""
        if self.player.points == 21:
            message = "You Win!"
        elif self.player.points > 21:
            message = "You Lost!"
        elif self.dealer.points > 21:
            message = "You Win!"
        elif self.dealer.points == 21:
            message = "You Lost!"
        elif self.player.points > self.dealer.points:
            message = "You Win!"
        elif self.player.points == self.dealer.points:
            message = "It's a Draw!"
        else:
            message = "You Lost!"
        
        font = pygame.font.SysFont(None, 100)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, (self.screen.get_height() // 2) - 35))
        self.screen.blit(text, text_rect)

    def draw(self):
        self.screen.fill((0, 100, 0))

        self.player.draw_hand(self.screen, 30, 440)
        self.dealer.draw_hand(self.screen, 30, 100)

        
        font_points = pygame.font.SysFont(None, 60)
        player_points = f"Player Points: {self.player.get_total()}"
        player_points = font_points.render(player_points, True, (255, 255, 255))
        self.screen.blit(player_points, (30, 650))

        dealer_points = ""
        if self.dealer.turn is False and self.end_game is False:
            dealer_points = f"Dealer Points: {self.dealer.get_first_card()}"
        else:
            dealer_points = f"Dealer Points: {self.dealer.get_total()}"
        dealer_points = font_points.render(dealer_points, True, (255, 255, 255))
        self.screen.blit(dealer_points, (30, 35))

        font_btn = pygame.font.SysFont(None, 36)

        # Draw buttons
        pygame.draw.rect(self.screen, (50, 150, 50), self.button_hit)
        pygame.draw.rect(self.screen, (150, 150, 50), self.button_stand)
        pygame.draw.rect(self.screen, (150, 50, 50), self.button_restart)

        # Center text on each button
        hit_text = font_btn.render("Hit", True, (255,255,255))
        stand_text = font_btn.render("Stand", True, (255,255,255))
        restart_text = font_btn.render("Restart", True, (255,255,255))

        self.screen.blit(hit_text, hit_text.get_rect(center=self.button_hit.center))
        self.screen.blit(stand_text, stand_text.get_rect(center=self.button_stand.center))
        self.screen.blit(restart_text, restart_text.get_rect(center=self.button_restart.center))

        if self.end_game:
            self.draw_winner()