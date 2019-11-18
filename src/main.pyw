import pygame
import random

class MoleHole():
    def __init__(self, screenX, screenY, number):
        self.__width = screenX // 3 #Take up 1/3 of x width
        self.__height = screenY // 4 #Take up 1/4 of y width
        self.__x = ( (number)  % 3 ) * self.__width #x Blit Position
        self.__y = ( (number) // 3 ) * self.__height + self.__height #y Blit Position
        self.__rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
        self.__number = number

    def getBlitPos(self):
        return (self.__x, self.__y)

    def getRect(self):
        return self.__rect

    def getNumber(self):
        return self.__number





class Scene():
    def __init__(self, screen):
        self.__screen = screen
        self.__maxTime = 10
        self.__musicPlaying = True

    def loop(self, events):
        self.__events = events
        if self.__scene == "inGame":
            return self.__inGame()
        elif self.__scene == "menu":
            return self.__menu()
        elif self.__scene == "score":
            return self.__scoreDisplay()

    def setInGameScene(self):
        self.__scene = "inGame"
        x, y = self.__screen.get_size()
        self.__moleHoleImg = pygame.image.load("assets/ground_hole.png")
        self.__moleHoleImg = pygame.transform.scale(self.__moleHoleImg, (x // 3, y // 4))
        self.__score = 0
        self.__moleImg = pygame.image.load("assets/pope.png")
        self.__moleImg = pygame.transform.scale(self.__moleImg, (x // 6, y // 8))
        self.__moleNumber = random.randint(0, 8)
        self.__molePosOffset = (x//12, y//80)

        self.__moleHoles = []
        for i in range(9):
            self.__moleHoles.append( MoleHole( x, y, i ) )

        self.__initialTicks = pygame.time.get_ticks()

    def setMenuScene(self):
        self.__scene = "menu"
        x, y = self.__screen.get_size()
        x //= 100 #One percent of pixels in the x axis
        y //= 100 #One percent of pixels in the y axis
        self.buttons = {}
        self.buttons["start"] = TextBox(20, [50, 15], "Start", (x, y))
        self.buttons["quit"] = TextBox(20, [50, 40], "Quit", (x, y))
        self.buttons["10"] = TextBox(10, [40, 70], "10s", (x, y))
        self.buttons["30"] = TextBox(10, [50, 70], "30s", (x, y))
        self.buttons["60"] = TextBox(10, [60, 70], "60s", (x, y))
        self.buttons["toggleMusic"] = TextBox(15, [50, 90], "Toggle Music", (x, y))

    def setScoreScene(self):
        self.__scene = "score"
        x, y = self.__screen.get_size()
        x //= 100 #One percent of pixels in the x axis
        y //= 100 #One percent of pixels in the y axis
        self.__finalScoreText = TextBox(35, [50, 20], "Score: " + str(self.__score), (x, y))
        self.__continueText = TextBox(10, [50, 65], "Press enter to continue", (x, y))

    def __inGame(self):
        done = False

        if ((pygame.time.get_ticks() - self.__initialTicks) / 1000) > self.__maxTime:
            self.setScoreScene()

        x, y = self.__screen.get_size()
        x //= 100 #One percent of pixels in the x axis
        y //= 100 #One percent of pixels in the y axis
        self.__currentScoreText = TextBox(20, [50, 10], "Score: " + str(self.__score), (x, y))

        for event in self.__events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key >= 257 and event.key <= 265:
                    if [263, 264, 265, 260, 261, 262, 257, 258, 259].index(event.key) == self.__moleNumber:
                        self.__score += 1
                        self.__moleNumber = random.randint(0, 8)
                    else:
                        if self.__score > 0:
                            self.__score -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for moleHole in self.__moleHoles:
                    if moleHole.getRect().collidepoint(x, y):
                        if moleHole.getNumber() == self.__moleNumber:
                            self.__score += 1
                            self.__moleNumber = random.randint(0, 8)
                        else:
                            if self.__score > 0:
                                self.__score -= 1

        self.__screen.fill((255, 255, 255))
        for hole in self.__moleHoles:
            self.__screen.blit(self.__moleHoleImg, hole.getBlitPos())
        molePosition = self.__moleHoles[self.__moleNumber].getBlitPos()
        molePosition = list(molePosition)
        molePosition[0] += self.__molePosOffset[0]
        molePosition[1] += self.__molePosOffset[1]
        self.__screen.blit(self.__moleImg, molePosition)
        self.__currentScoreText.blit(self.__screen)

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
                if self.buttons["start"].getRect().collidepoint(x, y):
                    self.setInGameScene()
                if self.buttons["quit"].getRect().collidepoint(x, y):
                    done = True
                if self.buttons["10"].getRect().collidepoint(x, y):
                    self.__maxTime = 10
                if self.buttons["30"].getRect().collidepoint(x, y):
                    self.__maxTime = 30
                if self.buttons["60"].getRect().collidepoint(x, y):
                    self.__maxTime = 60
                if self.buttons["toggleMusic"].getRect().collidepoint(x, y):
                    if self.__musicPlaying:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    self.__musicPlaying = not self.__musicPlaying

        self.__screen.fill((255, 255, 255))
        for button in self.buttons:
            self.buttons[button].blit(self.__screen)

        return done

    def __scoreDisplay(self):
        done = False

        for event in self.__events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_RETURN:
                    self.setMenuScene()

        self.__screen.fill((255, 255, 255))
        self.__finalScoreText.blit(self.__screen)
        self.__continueText.blit(self.__screen)

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
    pygame.mixer.init()
    pygame.mixer.music.load("assets/bensound-jazzyfrenchy.mp3")
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    done = False
    pygame.display.set_caption('Wack a Pole!')
    clock = pygame.time.Clock()

    scene = Scene(screen)
    scene.setInGameScene()
    scene.setMenuScene()

    pygame.mixer.music.play(-1,0.0)
    while not done:
        events = pygame.event.get()
        done = scene.loop(events)
        pygame.display.update()
        clock.tick(60)

    print("END")





if __name__ == "__main__":
    main()
