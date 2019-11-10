import pygame
import random

def main():
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    x, y = screen.get_size()
    done = False
    pygame.display.set_caption('Wack a Pole!')
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        pygame.display.update()
        clock.tick(60)

    print("END")

if __name__ == "__main__":
    main()
