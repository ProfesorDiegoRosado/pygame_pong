import pygame as pg
from enum import Enum
import random
import pygame.freetype  # Import the freetype module.

# Speed player's bars move around
PLAYER_MOVE = 10


def sign(n):
    if n < 0:
        return -1
    else:
        return 1


class Direction(Enum):
    UP = 0
    DOWN = 1


class Side(Enum):
    LEFT = 0
    RIGHT = 1


class Score:
    """ store scores """
    def __init__(self, player_1_score: int, player_2_score: int, pos_xy):
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        self.pos_xy: (int,int) = pos_xy

    def update_player_1(self, increment):
        self.player_1_score += increment

    def update_player_2(self, increment):
        self.player_2_score += increment

    def draw(self, surface):
        text_font = pg.font.Font('resources/fonts/SuperLegendBoy.ttf', 20)
        text = str(self.player_1_score) + "   " + str(self.player_2_score)
        text_surface = text_font.render(text, False, (255,255,255))
        surface.blit(text_surface, self.pos_xy)


class Sound:
    """ Manage sounds """
    @classmethod
    def beep(cls):
        beep_sound = pg.mixer.Sound('resources/sounds/beep.ogg')
        beep_sound.set_volume(0.5)
        beep_sound.play()

    @classmethod
    def baby_laugh(cls):
        laugh_sound = pg.mixer.Sound('resources/sounds/baby_laugh.ogg')
        laugh_sound.set_volume(1.0)
        laugh_sound.play()


class Player:
    """ Pong player """
    RECT_WIDTH = 20
    RECT_HEIGHT = 80

    def __init__(self, dimensions: (int, int), name: str, side: Side, pos: (int, int), color=(255, 255, 255)):
        self.dimensions = dimensions
        self.name = name
        self.side: Side = side
        self.pos_x: int = pos[0]
        self.pos_y: int = pos[1]
        self.color = color

    def is_left_player(self):
        return self.side == Side.LEFT

    def is_right_player(self):
        return not self.is_left_player()

    def update_position(self, dir: Direction):
        if dir == Direction.DOWN:
            if self.pos_y < self.dimensions[1]:  # check DOWN boundary
                self.pos_y = self.pos_y + PLAYER_MOVE
        else:  # Direcction.UP
            if self.pos_y > 0:
                self.pos_y = self.pos_y - PLAYER_MOVE

    def draw(self, surface):
        # pygame.draw.rect(surface, color, pygame.Rect(left, top, width, height))
        left = self.pos_x - (Player.RECT_WIDTH / 2)
        top = self.pos_y - (Player.RECT_HEIGHT / 2)
        pg.draw.rect(surface, self.color, pg.Rect(left, top, Player.RECT_WIDTH, Player.RECT_HEIGHT))


class Velocity:
    def __init__(self, x, y, speed):
        self.x: int = x
        self.y: int = y
        self.speed: int = speed

    @classmethod
    def random(cls, speed = None):
        VELOCITY_X = 4
        velocity_x = random.choice([-VELOCITY_X, VELOCITY_X])
        velocity_y = random.choice([-3,-2,-1,1,2,3])
        velocity_speed = 1 if speed is None else random.randint(1,3)
        return Velocity(velocity_x, velocity_y, velocity_speed)


class Ball:
    def __init__(self, pos_x, pos_y, radius, velocity: Velocity, color=(255, 255, 255)):
        self.initial_pos_x = pos_x
        self.initial_pos_y = pos_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.velocity = Velocity(-5, 3, 1)
        self.color = color

    def update(self):
        self.pos_x = self.pos_x + (self.velocity.x * self.velocity.speed)
        self.pos_y = self.pos_y + (self.velocity.y * self.velocity.speed)

    def draw(self, surface):
        # pygame.draw.circle(surface, color, center, radius)
        pg.draw.circle(surface, self.color, (self.pos_x, self.pos_y), self.radius)

    def restart(self):
        self.pos_x = self.initial_pos_x
        self.pos_y = self.initial_pos_y
        self.velocity = Velocity.random(1)


class Board:
    BLACK = (0, 0, 0)  # class constant
    WHITE = (255, 255, 255)
    BALL_RADIUS = 6
    BALL_COLOR = WHITE
    PLAYER_SIDE_OFFSET = 20

    def __init__(self, dimensions: (int, int)):
        self.dimensions: (int, int) = dimensions
        player1_pos: (int, int) = (Board.PLAYER_SIDE_OFFSET, dimensions[1] / 2)
        player2_pos: (int, int) = (dimensions[0] - Board.PLAYER_SIDE_OFFSET, dimensions[1] / 2)
        self.player1: Player = Player(self.dimensions, "Player 1", Side.LEFT, player1_pos)
        self.player2: Player = Player(self.dimensions, "Player 2", Side.RIGHT, player2_pos)
        self.score = Score(0,0, ((dimensions[0] / 2)-32, 20))
        self.ball = Ball(dimensions[0] / 2, dimensions[1] / 2, Board.BALL_RADIUS, Velocity(-5, 3, 1), Board.BALL_COLOR)
        self.display = pg.display.set_mode(dimensions)
        self.display.fill(Board.BLACK)

    def update_elements(self):
        if self.ball.pos_y - self.ball.radius <= 0:  # check collision ball up wall
            # change sign velocity y
            self.ball.velocity.y = - self.ball.velocity.y
            Sound.beep()
        elif self.ball.pos_y + self.ball.radius >= self.dimensions[1]:  # check collision ball down wall
            # change sign velocity y
            self.ball.velocity.y = - self.ball.velocity.y
            Sound.beep()
        elif self.ball.pos_x - self.ball.radius <= 0:  # check player 1 goal
            # reset ball position
            self.ball.restart()
            # Play goal sound
            Sound.baby_laugh()
            # update score player 1
            self.score.update_player_1(1)
            #self.score.draw(self.display)
        elif self.ball.pos_x + self.ball.radius >= self.dimensions[0]:  # check player 2 goal
            # reset ball position
            self.ball.restart()
            # Play goal sound
            Sound.baby_laugh()
            # update score player 2
            self.score.update_player_2(1)
            #self.score.draw(self.display)
        elif (self.ball.pos_x - self.ball.radius <= self.player1.pos_x + (self.player1.RECT_WIDTH / 2)) and \
                (self.ball.pos_x - self.ball.radius > self.player1.pos_x + (self.player1.RECT_WIDTH / 2) - PLAYER_MOVE) and \
                (self.ball.pos_y <= self.player1.pos_y + int(self.player1.RECT_HEIGHT / 2)) and \
                (self.ball.pos_y >= self.player1.pos_y - int(self.player1.RECT_HEIGHT / 2)):  # collision with player 2 bar
            self.ball.velocity.x = -self.ball.velocity.x
            Sound.beep()
            # change velocity y depending on bar place of impact
            """
            CHANGE_VELOCITY_SEGMENTS = 4
            vel_y_proportion: float = self.ball.velocity.y / CHANGE_VELOCITY_SEGMENTS
            bars_segment = int((self.player1.RECT_HEIGHT/2) / CHANGE_VELOCITY_SEGMENTS)
            deviation = int(self.ball.pos_y - self.player1.pos_y)

            impact_segment = int(deviation / CHANGE_VELOCITY_SEGMENTS)
            self.ball.velocity.y = self.ball.velocity.y + int(sign(deviation) * impact_segment * vel_y_proportion)
            """

        elif (self.ball.pos_x + self.ball.radius >= self.player2.pos_x - (self.player2.RECT_WIDTH / 2)) and \
                (self.ball.pos_x + self.ball.radius < self.player2.pos_x - (self.player2.RECT_WIDTH / 2) + PLAYER_MOVE) and \
                (self.ball.pos_y <= self.player2.pos_y + int(self.player2.RECT_HEIGHT / 2)) and \
                (self.ball.pos_y >= self.player2.pos_y - int(self.player2.RECT_HEIGHT / 2)):  # collision with player 2 bar
            self.ball.velocity.x = -self.ball.velocity.x
            Sound.beep()
            """
            # change velocity y depending on bar place of impact
            CHANGE_VELOCITY_SEGMENTS = 4
            vel_y_portion = int(self.ball.velocity.y / CHANGE_VELOCITY_SEGMENTS)
            bars_segment = int((self.player2.RECT_HEIGHT/2) / CHANGE_VELOCITY_SEGMENTS)
            deviation = int(self.ball.pos_y - self.player2.pos_y)

            impact_segment = int(abs(deviation) / CHANGE_VELOCITY_SEGMENTS)
            self.ball.velocity.y = self.ball.velocity.y + int(sign(deviation) * impact_segment * vel_y_portion)
            beep_sound = pg.mixer.Sound('resources/sounds/beep.ogg')
            beep_sound.play()
            """
        self.ball.update()

    def update(self):
        # update everything black
        self.display.fill(Board.BLACK)
        # update positions and check collisions
        self.update_elements()
        # self.player1.update_position()  # Done when key strokes
        # self.player2.update_position()
        self.ball.draw(self.display)
        self.score.draw(self.display)
        self.player1.draw(self.display)
        self.player2.draw(self.display)
        # update
        pg.display.update()
