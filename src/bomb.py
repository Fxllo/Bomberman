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
            arena.spawn(Explosion(self.pos(), arena.get_bomberman(), arena, "center"))
            # prendo l'attore nei blocchi adiacenti a x e y e controllo se è un muro
            # array delle posizioni degli attori
            positions = [actor.pos() for actor in arena.actors() if isinstance(actor, Wall) and not actor.is_destructible()]
            # controllo se sono presenti attori nelle posizioni adiacenti
            if (self._x + TILE, self._y) not in positions:
                arena.spawn(Explosion((self._x + TILE, self._y), arena.get_bomberman(), arena, "right"))
            if (self._x - TILE, self._y) not in positions:
                arena.spawn(Explosion((self._x - TILE, self._y), arena.get_bomberman(), arena, "left"))
            if (self._x, self._y + TILE) not in positions:
                arena.spawn(Explosion((self._x, self._y + TILE), arena.get_bomberman(), arena, "down"))
            if (self._x, self._y - TILE) not in positions:
                arena.spawn(Explosion((self._x, self._y - TILE), arena.get_bomberman(), arena, "up"))

            arena.remove(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._timer < 20:
            return 32, 48
        elif self._timer < 40:
            return 16, 48
        return 0, 48

    def is_passable(self) -> bool:
        return self._passable

    def make_impassable(self):
        self._passable = False

class Explosion(Actor):
    def __init__(self, pos, bomberman, arena, type):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 20
        self._bomberman = bomberman
        self._arena = arena
        self._type = type
        
    def move(self, arena: Arena):
        from entities import Ballom, Bomberman
        
        self._timer -= 1
        if self._timer <= 0:
            arena.remove(self)

            for actor in arena.actors():
                if isinstance(actor, Ballom) and self.check_collision(actor):
                    actor.kill()
                elif isinstance(actor, Wall) and actor.is_destructible() and self.check_collision(actor):
                    actor.kill()
                elif isinstance(actor, Bomberman) and self.check_collision(actor):
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
        if self._type == "center":
            if self._timer < 5:
                sprite_x, sprite_y = 112, 175
            elif self._timer < 10:
                sprite_x, sprite_y = 32, 176
            elif self._timer < 15:
                sprite_x, sprite_y = 113,96
            else:
                sprite_x, sprite_y = 34, 97  
        elif self._type == "up":
            if self._timer < 5:
                return 112, 160
            elif self._timer < 10:
                return 32, 160
            elif self._timer < 15:
                return 112, 80
            else:
                return 32, 80
        elif self._type == "down":
            sprite_x, sprite_y = 32, 112
        elif self._type == "left":
            sprite_x, sprite_y = 16, 96
        elif self._type == "right":
            sprite_x, sprite_y = 48, 96 
        return sprite_x, sprite_y
    
class FreeSprite(Actor):
    def __init__(self, pos, sprite_type):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 20
        self._sprite_type = sprite_type

    def move(self, arena: Arena):
        self._timer -= 1
        if self._timer <= 0:
            arena.remove(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._sprite_type == "up":
            if self._timer < 5:
                return 112, 160
            elif self._timer < 10:
                return 32, 160
            elif self._timer < 15:
                return 112, 80
            else:
                return 32, 80
        elif self._sprite_type == "down":
            return 32, 112
        elif self._sprite_type == "left":
            return 16, 96
        elif self._sprite_type == "right":
            return 48, 96