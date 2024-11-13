from main import TILE, STEP, ARENA_W, ARENA_H
from random import choice
from actor import Actor, Arena, Point
from bomb import Bomb

class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        self._speed = STEP * 2
        self._dx, self._dy = choice([(0, -self._speed), (self._speed, 0), (0, self._speed), (-self._speed, 0)])
        self._tick_count = 0
        self._passable = True

    def move(self, arena: Arena):       
        self._tick_count += 1
        if self._tick_count % 3 != 0:
            return

        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = choice([(0, -self._speed), (self._speed, 0), (0, self._speed), (-self._speed, 0)])

        new_x, new_y = self._x + self._dx, self._y + self._dy
        if not arena.check_collision(self, new_x, new_y):
            self._x, self._y = new_x, new_y
        
        for actor in arena.actors():
            if isinstance(actor, Bomberman) and self.check_collision(actor):
                actor.kill()
            
    def check_collision(self, actor: Actor) -> bool:
        ax, ay = actor.pos()
        aw, ah = actor.size()
        return (self._x < ax + aw and self._x + self._w > ax and
                self._y < ay + ah and self._y + self._h > ay)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._tick_count % 100 < 10:
            return 48, 240
        elif self._tick_count % 100 < 20:
            return 64, 240
        elif self._tick_count % 100 < 30:
            return 80, 240
        elif self._tick_count % 100 < 40:
            return 64, 240
        elif self._tick_count % 100 < 50 :
            return 48, 240
        elif self._tick_count % 100 < 60:
            return 0, 240
        elif self._tick_count % 100 < 70:
            return 16, 240
        elif self._tick_count % 100 < 80:
            return 32, 240
        elif self._tick_count % 100 < 90:
            return 16, 240
        return 0, 240
    
    def is_passable(self) -> bool:
        return self._passable
    
class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._alive = True
        self._bomb_planted = False
        self._lives = 3
        self._sprite = 48, 16
        self._invincible = False
        self._timeLived = 0
        self._score = 0

    def move(self, arena: Arena):
        self._timeLived += 1
        if self._invincible and self._timeLived > 60:
            self._invincible = False
        keys = arena.current_keys()

        if "Spacebar" in keys and not self._bomb_planted:
            arena.spawn(Bomb(self.pos()))
            self._bomb_planted = True
            
        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = 0, 0
            if "W" in keys:
                self._dy = -self._speed
            elif "S" in keys:
                self._dy = self._speed
            elif "A" in keys:
                self._dx = -self._speed
            elif "D" in keys:
                self._dx = self._speed
        new_x, new_y = self._x + self._dx, self._y + self._dy

        if not arena.check_collision(self, new_x, new_y):
            self._x, self._y = new_x, new_y

        if "Spacebar" not in keys:
            self._bomb_planted = False

    def check_collision(self, actor: Actor) -> bool:
        ax, ay = actor.pos()
        aw, ah = actor.size()
        return (self._x < ax + aw and self._x + self._w > ax and
                self._y < ay + ah and self._y + self._h > ay)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._dx < 0:
            if self._timeLived % 60 < 20:
                self._sprite = 0, 0
            elif self._timeLived % 60 < 40:
                self._sprite = 16, 0
            else:
                self._sprite = 32, 0
        elif self._dx > 0:
            if self._timeLived % 60 < 20:
                self._sprite = 0, 16
            elif self._timeLived % 60 < 40:
                self._sprite = 16, 16
            else:
                self._sprite = 32, 16
        elif self._dy < 0:
            if self._timeLived % 60 < 20:
                self._sprite = 48, 16
            elif self._timeLived % 60 < 40:
                self._sprite = 64, 16
            else:
                self._sprite = 80, 16
        elif self._dy > 0:
            if self._timeLived % 60 < 20:
                self._sprite = 48, 0
            elif self._timeLived % 60 < 40:
                self._sprite = 64, 0
            else:
                self._sprite = 80, 0
        return self._sprite

    def kill(self):
        if self._invincible:
            return
        
        self._lives -= 1
        self._invincible = True
        self._alive = False
        self._timeLived = 0
        
        self._x, self._y = ARENA_W/2-TILE/2, ARENA_H/2-TILE/2

        if self._lives == 0:
            import g2d
            self._alive = False
            g2d.alert("Bomberman è stato ucciso da un nemico! GAME OVER!")
            g2d.close_canvas()        

    def is_alive(self) -> bool:
        return self._alive
    
    def count_lives(self) -> int:
        return self._lives
    
    def score(self) -> int:
        return self._score
    
    def add_score(self, score):
        self._score += score
        return self._score