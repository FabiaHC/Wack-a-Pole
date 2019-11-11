import pygame
import random

class MoleHole():
    def __init__(self, screenX, screenY, number):
        self.__width = screenX // 3 #Take up 1/3 of x width
        self.__height = screenY // 4 #Take up 1/4 of y width
        self.__x = ( (number)  % 3 ) * self.__width #x Blit Position
        self.__y = ( (number) // 3 ) * self.__height + self.__height #y Blit Position
        self.rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)

    def getBlitPos(self):
        return (self.__x, self.__y)





class Scene():
    def __init__(self, screen):
        self.__screen = screen

    def setScene(self, sceneName):
        self.__scene = sceneName

    def loop(self, events):
        self.__events = events
        if self.__scene == "inGame":
            return self.__inGame()
        elif self.__scene == "menu":
            return self.__menu()

    def setInGameScene(self, moleHoles, moleHoleImg):
        self.__moleHoles = moleHoles
        self.__moleHoleImg = moleHoleImg

    def __inGame(self):
        done = False

        for event in self.__events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        self.__screen.fill((255, 255, 255))
        for hole in self.__moleHoles:
            self.__screen.blit(self.__moleHoleImg, hole.getBlitPos())

        return done

    def __menu(self):
        done = False

        for event in self.__events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        self.__screen.fill((255, 255, 255))

        return done





class TextBox():
    def __init__(self, size, pos, text):
        font = pygame.font.Font('Comic Sans MS', size)
        self.__textSurface = font.render(text, True, (0,0,0))
        self.__textRect = self.__textSurface.get_rect()
        self.__pos = pos

    def getPos(self):
        return self.__pos





def main():
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    x, y = screen.get_size()
    done = False
    pygame.display.set_caption('Wack a Pole!')
    clock = pygame.time.Clock()

    #Assets
    moleHoleImg = pygame.image.load("assets/ground_hole.png")
    moleHoleImg = pygame.transform.scale(moleHoleImg, (x // 3, y // 4))

    moleHoles = []
    for i in range(9):
        moleHoles.append( MoleHole( x, y, i ) )
    scene = Scene(screen)
    scene.setInGameScene(moleHoles, moleHoleImg)
    scene.setScene("menu")

    while not done:
        events = pygame.event.get()
        done = scene.loop(events)
        pygame.display.update()
        clock.tick(60)

    print("END")





if __name__ == "__main__":
    main()
