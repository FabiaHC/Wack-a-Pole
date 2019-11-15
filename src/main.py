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

    def setInGameScene(self):
        x, y = self.__screen.get_size()
        self.__moleHoleImg = pygame.image.load("assets/ground_hole.png")
        self.__moleHoleImg = pygame.transform.scale(self.__moleHoleImg, (x // 3, y // 4))

        self.__moleHoles = []
        for i in range(9):
            self.__moleHoles.append( MoleHole( x, y, i ) )

    def setMenuScene(self):
        x, y = self.__screen.get_size()
        x //= 100 #One percent of pixels in the x axis
        y //= 100 #One percent of pixels in the y axis
        self.buttons = {}
        self.buttons["start"] = TextBox(20, [50, 15], "Start", (x, y))

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.__startButton.getRect().collidepoint(x, y):
                    self.setInGameScene()
                    self.setScene("inGame")

        self.__screen.fill((255, 255, 255))
        for button in self.buttons:
            self.buttons[button].blit(self.__screen)

        return done





class TextBox():
    def __init__(self, size, pos, text, screenPercentage):
        font = pygame.font.Font('assets/burnstown dam.ttf', size*screenPercentage[1])
        self.__textSurface = font.render(text, True, (0,0,0))
        self.__textRect = self.__textSurface.get_rect()
        rectSize = self.__textSurface.get_size()
        pos[0] = pos[0] * screenPercentage[0] - rectSize[0] // 2
        pos[1] = pos[1] * screenPercentage[1] - rectSize[1] // 2
        self.__textRect.move_ip(pos[0], pos[1])
        self.__pos = pos

    def blit(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.__textRect, 3)
        screen.blit(self.__textSurface, self.__pos)

    def getRect(self):
        return self.__textRect




def main():
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    x, y = screen.get_size()
    done = False
    pygame.display.set_caption('Wack a Pole!')
    clock = pygame.time.Clock()

    scene = Scene(screen)
    scene.setInGameScene()
    scene.setMenuScene()
    scene.setScene("menu")

    while not done:
        events = pygame.event.get()
        done = scene.loop(events)
        pygame.display.update()
        clock.tick(60)

    print("END")





if __name__ == "__main__":
    main()
