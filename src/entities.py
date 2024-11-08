from main import TILE, STEP
from random import choice
from actor import Actor, Arena, Point
from bomb import Bomb

class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._dx, self._dy = choice([(0, -self._speed), (self._speed, 0), (0, self._speed), (-self._speed, 0)])
        self._tick_count = 0

    def move(self, arena: Arena):
        # import g2d
        
        self._tick_count += 1
        if self._tick_count % 3 != 0:
            return

        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = choice([(0, -self._speed), (self._speed, 0), (0, self._speed), (-self._speed, 0)])

        new_x, new_y = self._x + self._dx, self._y + self._dy
        if not arena.check_collision(self, new_x, new_y):
            self._x, self._y = new_x, new_y
        
        #TODO implementare collisione con Bomberman (non worka)
        # Controllo collisione con bomberman
        # for actor in arena.actors():
        #     if isinstance(actor, Bomberman) and self.check_collision(actor):
        #         actor.kill()
        #         arena.remove(actor)
        #         g2d.alert("Bomberman è stato ucciso da Ballom! GAME OVER!")
        #         g2d.close_canvas()
        #         return
            
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
        return 0, 240
    
class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._alive = True
        self._bomb_planted = False

    def move(self, arena: Arena):
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
        return 64, 0

    def kill(self):
        self._alive = False

    def is_alive(self) -> bool:
        return self._alive