# coding=utf-8
# file with game logics
# Here will be Player, Game, Element classes

import random
import math


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

    def _digg(self, y, x):
        if not (0 <= x < GX and 0 <= y < GY):
            return
        if self.game.g[y][x] == Elem.dirt:
            self.game.g[y][x] = Elem.empty
        elif self.game.g[y][x] == Elem.evildirt:
            self.game.new_fire(y, x)
