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
            
            blocks_explosion = [
                (self._x, self._y),
                (self._x + TILE, self._y),
                (self._x - TILE, self._y),
                (self._x, self._y + TILE),
                (self._x, self._y - TILE)
            ]
            
            arena.spawn(Explosion(self.pos(), arena.get_bomberman(), arena, "center"))
            # positions = [actor.pos() for actor in arena.actors() if isinstance(actor, Wall) and not actor.is_destructible()]
            # if (self._x + TILE, self._y) not in positions:
            #     arena.spawn(Explosion((self._x + TILE, self._y), arena.get_bomberman(), arena, "right"))
            # if (self._x - TILE, self._y) not in positions:
            #     arena.spawn(Explosion((self._x - TILE, self._y), arena.get_bomberman(), arena, "left"))
            # if (self._x, self._y + TILE) not in positions:
            #     arena.spawn(Explosion((self._x, self._y + TILE), arena.get_bomberman(), arena, "down"))
            # if (self._x, self._y - TILE) not in positions:
            #     arena.spawn(Explosion((self._x, self._y - TILE), arena.get_bomberman(), arena, "up"))
            
            #controlla se in una delle posizioni c'è un muro
            positions = [actor.pos() for actor in arena.actors() if isinstance(actor, Wall)]
            if (self._x + TILE, self._y) not in positions:
                arena.spawn(Explosion((self._x + TILE, self._y), arena.get_bomberman(), arena, "right"))
            if (self._x - TILE, self._y) not in positions:
                arena.spawn(Explosion((self._x - TILE, self._y), arena.get_bomberman(), arena, "left"))
            if (self._x, self._y + TILE) not in positions:
                arena.spawn(Explosion((self._x, self._y + TILE), arena.get_bomberman(), arena, "down"))
            if (self._x, self._y - TILE) not in positions:
                arena.spawn(Explosion((self._x, self._y - TILE), arena.get_bomberman(), arena, "up"))

            for pos in blocks_explosion:
                for actor in arena.actors():
                    if isinstance(actor, Wall) and actor.pos() == pos:
                        if actor.is_destructible():
                            actor.kill()
                        break
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
                return 112, 176
            elif self._timer < 10:
                return 32, 176
            elif self._timer < 15:
                return 112, 96
            else:
                return 32, 96  
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
            if self._timer < 5:
                return 112, 192
            elif self._timer < 10:
                return 32, 192
            elif self._timer < 15:
                return 112, 112
            else:
                return 32, 112
        elif self._type == "left":
            if self._timer < 5:
                return 96, 176
            elif self._timer < 10:
                return 16, 176
            elif self._timer < 15:
                return 96, 96
            else:
                return 16, 96
        elif self._type == "right":
            if self._timer < 5:
                return 128, 176
            elif self._timer < 10:
                return 64, 176
            elif self._timer < 15:
                return 128, 96
            else:
                return 64, 96
    
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