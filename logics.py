# coding=utf-8
# file with game logics
# Here will be Player, Game, Element classes

import random
import math


ELEM_PROB = 0.1
EVIL_PROB = 0.1
RESTORE_TIME = 12
GX = 23
GY = 35
HEART_LIFE = 25
BURN_LIFE = 20
GOAL_OF_LEVEL = lambda level:300 + level*100

class GameOver(Exception):
    def __str__(self):  return 'Game Over'


class YouWin(Exception):
    def __str__(self): return 'You Win'


class _FireStopped(Exception):
    pass   # nothing


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
    def __init__(self, game, y, x, name, total_score):

        self.name = name
        self.password = ''
        self.life = 100
        self.life_restore = 0
        self.life_waiting = False
        self.left = False
        self.command = ''
        self.game = game
        self.y = y
        self.x = x
        self.total_score = total_score

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
                self._digg(self.y + 1, self.x + (-1 if self.left else 1))
            self.command = ''

    def go(self, x, y):
        self.game.g[self.y][self.x] = Elem.empty
        self.game.g[y][x] = Elem.player
        self.y = y
        self.x = x

    def _move(self, y, x):
        if not (0 <= x < GX and 0 <= y < GY):
            return False
        g_yx = self.game.g[y][x]
        if g_yx == Elem.empty:
            self.go(x, y)
            return True
        elif g_yx == Elem.heart:
            self.life = min(self.life + HEART_LIFE, 100)
            self.go(x, y)
            return  True
        elif g_yx in Elem.chunk:
            ind = self.game.g[y][x]
            self.game.cur += SALARY[ind]
            if self.game.cur >= self.game.goal:
                raise YouWin()
            self.go(x, y)
            return True
        elif g_yx == Elem.fire:
            for fire in self.game.fires:
                if fire.x == x and fire.y == y:
                    if self.hurt(BURN_LIFE):
                        self.game.g[y][x] = Elem.empty
                        self.game.fires.remove(fire)
                        return self._move(y, x)
                    else:
                        return False
            else:
                raise RuntimeError('cant find right fire')

    def set_name(self, name):
        self.name = name
        return self

    def add_total_score(self,score):
        self.total_score += score


class Fire:
    def __init__(self, game, y, x):
        self.left = False
        self.y = y
        self.x = x
        self.game = game

    def tick(self):
        _t = (Elem.dirt, Elem.evildirt, Elem.fire)
        if self.y < GY - 1 and self.game.g[self.y + 1][self.x] == Elem.empty: # go down
            self.game.g[self.y + 1][self.x] = Elem.fire
            self.game.g[self.y][self.x] = Elem.empty
            self.y += 1
        elif self.y < GY - 1 and self.game.g[self.y + 1][self.x] in Elem.chunk + [Elem.heart]: # burn down
            self.game.new_fire(self.y + 1,self.x)
        elif self.y < GY - 1 and self.game.g[self.y + 1][self.x] == Elem.player: # beat down
            if self.game.player.hurt(BURN_LIFE):
                 raise _FireStopped()
        elif 0 < self.x < GX - 1 and self.game.g[self.y][self.x + 1] in _t and self.game.g[self.y][self.x - 1] in _t: # nothing
            return
        elif (self.x == 0 and self.game.g[self.y][1] in _t) or (self.x == GX - 1 and self.game.g[self.y][GX - 2] in _t): # nothing
            return
        else:
            if self.x == 0:
                self.left = False
            if self.x == GX - 1:
                self.left = True
            next_x = self.x - 1 if self.left else self.x + 1
            if self.game.g[self.y][next_x] in _t:
                self.left=not self.left
                next_x=self.x - 1 if self.left else self.x + 1

            if self.game.g[self.y][next_x] == Elem.empty: # go next
                self.game.g[self.y][next_x] = Elem.fire
                self.game.g[self.y][self.x] = Elem.empty
                self.x=next_x
            elif self.game.g[self.y][next_x] in Elem.chunk+[Elem.heart]: # burn next
                self.game.new_fire(self.y, next_x)
            elif self.game.g[self.y][next_x] == Elem.fire: # ourselves
                pass
            elif self.game.g[self.y][next_x] == Elem.player: # beat next
                if self.game.player.hurt(BURN_LIFE):
                    raise _FireStopped()
            else:
                raise RuntimeError('bad next elem: %s'%self.game.g[self.y][next_x])


class Game:
    """Tests for hurting, ending level and changing player name
    >>> #Test for no hurting
    >>> Game().player.hurt(0)
    True
    >>> #Test for killing player
    >>> Game().player.hurt(100)
    Traceback (most recent call last):
    GameOver: Game Over
    >>> #Test for changing name
    >>> Game().player.set_name('Player').name
    'Player'
    >>> # Test for ending level
    >>> game = Game()
    >>> game.cur = 500
    >>> game.g[1][1] = 'Chunk1'
    >>> game.player._move(1,1)
    Traceback (most recent call last):
    YouWin: You Win
    """
    def __init__(self):
        self.g=None
        self.level=-1
        self.cur=0
        self.goal=0
        self.fires=set()
        self.player=Player(self,0,0,'noname',0)
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
        self.player=Player(self,0,math.floor(GX/2), self.player.name, self.player.total_score)

    def tick_fire(self):
        for fire in sorted(self.fires, key=lambda this:this.y*GX+this.x):
            try:
                fire.tick()
            except _FireStopped:
                self.g[fire.y][fire.x] = Elem.empty
                self.fires.remove(fire)

    def tick_item(self):
        for y in range(GY - 2, -1, -1):
            for x in range(GX):
                if self.g[y][x] in Elem.chunk + [Elem.heart]:
                    if self.g[y + 1][x] == Elem.empty:
                        self.g[y + 1][x] = self.g[y][x]
                        self.g[y][x] = Elem.empty
                    elif self.g[y + 1][x] == Elem.player:
                        if self.g[y][x] == Elem.heart:
                            self.player.life = min(self.player.life + HEART_LIFE, 100)
                        else:
                            self.cur += SALARY[self.g[y][x]]
                            if self.cur >= self.goal:
                                raise YouWin()
                        self.g[y][x] = Elem.empty
                    elif self.g[y + 1][x] == Elem.fire:
                        self.new_fire(y, x)

    def new_fire(self, y, x):
        self.g[y][x] = Elem.fire
        self.fires.add(Fire(self, y, x))

    def tick(self):
        self.tick_item()
        if self.fire_ticked:
            self.tick_fire()
        self.fire_ticked = not self.fire_ticked
        self.player.tick()

if __name__ == "__main__":
    import doctest
    doctest.testmod()