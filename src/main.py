import sys
import pygame
import copy
import random
import math
import threading
import time
pygame.init()


# VARIABLE INIT

size = width, height = 480, 480
screen = pygame.display.set_mode(size)
score = 0


# CLASSES

class Snake:
    def __init__(self):
        self.segments = [Segment(width/2, height/2)]
        self.x_direction = 0
        self.y_direction = 0
        self.color = (255, 255, 255)

    def add_segment(self):
        head = copy.deepcopy(self.segments[len(self.segments) - 1])
        self.segments.append(head)
        global score
        score += 10

    def draw(self):
        for segment in self.segments:
            color = self.color
            if segment == self.segments[len(self.segments)-1]:
                color = (122, 244, 40)
            pygame.draw.rect(screen, color, pygame.Rect(
                segment.x, segment.y, segment.width, segment.height))

    def move(self):
        head = copy.deepcopy(self.segments[len(self.segments)-1])
        self.segments.pop(0)
        head.x += self.x_direction * 10
        head.y += self.y_direction * 10
        if head.x <= 0:
            head.x += 480
        if head.y <= 0:
            head.y += 480
        if head.x >= width:
            head.x = 0
        if head.y >= height:
            head.y = 0
        self.segments.append(head)

    def set_direction(self, x, y):
        self.x_direction = x
        self.y_direction = y

    def death(self):
        head = self.segments[len(self.segments)-1]
        for i in range(len(self.segments)-2):
            if head.x == self.segments[i].x and head.y == self.segments[i].y:
                global score
                score = 0
                return True
        return False

    def eats(self, apple):
        snakeHead = self.segments[len(self.segments)-1]
        if math.dist((apple.x, apple.y), (snakeHead.x, snakeHead.y)) < 10:
            self.add_segment()
            return True

    def __str__(self):
        return f"Snake's length: {len(self.segments)}"


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10

    def __str__(self):
        return f"Segment position: x = {self.x}, y = {self.y}"


class Apple:
    def __init__(self):
        self.x = random.randrange(10, width-20, 10)
        self.y = random.randrange(10, height-20, 10)
        self.width = 10
        self.height = 10
        self.color = (234, 32, 16)
        self.decayed = False
        threading.Thread(target=self.decay).start()

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(
            self.x, self.y, self.width, self.height))

    def decay(self):
        time.sleep(4)
        self.decayed = True

    def __str__(self):
        return f"Apple at position: x = {self.x}, y = {self.y}"


# MAIN FUNCTION

def main():
    clock = pygame.time.Clock()
    color = 76, 76, 90
    snake = Snake()
    apples = [Apple()]
    font = pygame.font.Font(pygame.font.match_font('consolas'), 24)
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_w] and snake.y_direction != 1:
                    snake.set_direction(0, -1)
                    break
                if pygame.key.get_pressed()[pygame.K_a] and snake.x_direction != 1:
                    snake.set_direction(-1, 0)
                    break
                if pygame.key.get_pressed()[pygame.K_s] and snake.y_direction != -1:
                    snake.set_direction(0, 1)
                    break
                if pygame.key.get_pressed()[pygame.K_d] and snake.x_direction != -1:
                    snake.set_direction(1, 0)
                    break
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    snake.add_segment()
                    break
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    running = False
                    pygame.quit()
                    exit()

        if random.randint(0, 100) == 1:
            apples.append(Apple())
        screen.fill(color)
        for apple in apples:
            apple.draw()
            if snake.eats(apple) or apple.decayed == True:
                apples.remove(apple)

        if snake.death():
            snake = Snake()
        screen.blit(font.render(
            f"Score: {score}", True, (255, 255, 255)), (16, height-32))
        snake.draw()
        snake.move()
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
