from main import TILE
from actor import Actor, Arena, Point
from wall import Wall

class Bomb(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 60
        self._passable = True

    def move(self, arena: Arena):
        self._timer -= 1
        if self._timer <= 0:
            from bomb import Explosion
            arena.spawn(Explosion(self.pos()))
            arena.remove(self) 

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 48

    def is_passable(self) -> bool:
        return self._passable

    def make_impassable(self):
        self._passable = False

class Explosion(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 10

        self._explosion_blocks = [
            (self._x, self._y),
            (self._x, self._y - TILE),
            (self._x, self._y + TILE),
            (self._x - TILE, self._y),
            (self._x + TILE, self._y)
        ]

    def move(self, arena: Arena):
        from entities import Ballom, Bomberman
        import g2d
        
        self._timer -= 1
        if self._timer <= 0:
            arena.remove(self)

        for actor in arena.actors():
            if isinstance(actor, Ballom) and self.check_collision(actor):
                arena.remove(actor)
            elif isinstance(actor, Wall) and actor.is_destructible() and self.check_collision(actor):
                arena.remove(actor)
            elif isinstance(actor, Bomberman) and self.check_collision(actor):
                actor.kill()
                arena.remove(actor)
                g2d.alert("Bomberman è stato ucciso da una bomba! GAME OVER!")
                g2d.close_canvas()

    def check_collision(self, actor: Actor) -> bool:
        ax, ay = actor.pos()
        aw, ah = actor.size()

        for bx, by in self._explosion_blocks:
            if (bx < ax + aw and bx + self._w > ax and
                by < ay + ah and by + self._h > ay):
                return True
        return False

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 34, 48