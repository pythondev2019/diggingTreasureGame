# coding=utf-8
# file with game logics
# Here will be Player, Game, Element classes

import random
import math


RESTORE_TIME = 12
GX = 23
GY = 35


class GameOver(Exception):
    def __str__(self):  return 'Game Over'


class YouWin(Exception):
    def __str__(self): return 'You Win'


class Elem:
    dirt = 'Dirt'
    evildirt = 'Evil Dirt'
    empty = 'Empty'
    fire = 'Fire'
    heart = 'Heart'
    chunk = ['Chunk1', 'Chunk2', 'Chunk3']
    player = 'player'


SALARY = {Elem.chunk[0]: 100, Elem.chunk[1]: 200, Elem.chunk[2]: 300}


class Command:
    left = 'Move Left'
    right = 'Move Right'
    next = 'Digg Next'
    down = 'Digg Down'


class Player:
    def __init__(self, game, y, x):
        self.name = "noname"
        self.life = 100
        self.life_restore = 0
        self.life_waiting = False
        self.left = False
        self.command = ''
        self.game = game
        self.y = y
        self.x = x

    def hurt(self, value):
        if self.life_restore:
            return False
        else:
            self.life -= value
            self.life_restore = RESTORE_TIME
            if self.life <= 0:
                raise GameOver()
            return True

    def _digg(self, y, x):
        if not (0 <= x < GX and 0 <= y < GY):
            return
        if self.game.g[y][x] == Elem.dirt:
            self.game.g[y][x] = Elem.empty
        elif self.game.g[y][x] == Elem.evildirt:
            self.game.new_fire(y, x)

    def tick(self):
        if self.life_restore:
            self.life_restore -= 1
        if not self.life_waiting:
            self.life -= 1
        self.life_waiting = not self.life_waiting
        if self.life <= 0:
            raise GameOver()
        if not self._move(self.y + 1, self.x):
            if self.command == Command.left:
                if self.left:
                    self._move(self.y, self.x - 1)
                self.left = True
            elif self.command == Command.right:
                if not self.left:
                    self._move(self.y, self.x + 1)
                self.left = False
            elif self.command == Command.next:
                self._digg(self.y, self.x + (-1 if self.left else 1))
            elif self.command == Command.down:
                self._digg(self.y, self.x + (-1 if self.left else 1))
                self._digg(self.y+1, self.x + (-1 if self.left else 1))
            self.command = ''

    def go(self, x, y):
        self.game.g[self.y][self.x] = Elem.empty
        self.game.g[y][x] = Elem.player
        self.y = y
        self.x = x

    #def _move(self, y, x):


class Game:
    def __init__(self):
        self.g=None
        self.level=-1
        self.cur=0
        self.goal=0
        self.fires=set()
        self.player=Player(self,0,0)
        self.fire_ticked=False
        self.init_level(1)
    
    def init_level(self,level):
        #init grid
        self.g=[[Elem.dirt if random.random()>EVIL_PROB else Elem.evildirt for y in range(GX)] for x in range(GY)]
        self.g[0][math.floor(GX/2)]=Elem.player
        self.g[0][math.floor(GX/2)-1]=Elem.empty
        self.g[0][math.floor(GX/2)+1]=Elem.empty
        #put goods
        available=[(y,x) for y in range(GY) for x in range(GX) if self.g[y][x]==Elem.dirt]
        for y,x in random.sample(available,math.ceil(GX*GY*ELEM_PROB)):
            self.g[y][x]=random.choice(Elem.chunk+[Elem.heart])
        #init data
        self.level=level
        self.cur=0
        self.goal=GOAL_OF_LEVEL(level)
        self.fires=set()
        self.player=Player(self,0,math.floor(GX/2))
