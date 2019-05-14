# coding=utf-8
# file with game logics
# Here will be Player, Game, Element classes

import random
import math

class GameOver(Exception):
    def __str__(self):  return 'Game Over'

class YouWin(Exception):
    def __str__(self): return 'You Win'

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
