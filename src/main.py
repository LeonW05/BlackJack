import pygame
from game import BlackJack

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("BlackJack")
    clock = pygame.time.Clock()

    game = BlackJack(screen)

    running = True
    while running:
        running = game.handle_events()
        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()