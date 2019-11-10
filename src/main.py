import pygame
import random

class MoleHole():
    def __init__(self, screenX, screenY, number):
        self.__width = screenX // 3 #Take up 1/3 of x width
        self.__height = screenY // 3 #Take up 1/3 of y width
        self.__x = ( (number)  % 3 ) * self.__width #x Blit Position
        self.__y = ( (number) // 3 ) * self.__height #y Blit Position

def main():
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    x, y = screen.get_size()
    done = False
    pygame.display.set_caption('Wack a Pole!')
    clock = pygame.time.Clock()

    moleHoles = []
    for i in range(9):
        moleHoles.append( MoleHole( x, y, i ) )

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
