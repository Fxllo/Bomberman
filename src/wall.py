from main import TILE
from actor import Actor, Arena, Point

class Wall(Actor):
    def __init__(self, pos, destructible=False, **kwargs):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._destructible = destructible
        self._door = kwargs.get('door', False)
        self._plusBomb = kwargs.get('plusBomb', False)
        self._timeDead = 0

    def move(self, arena: Arena):
        if self._timeDead >= 1:
            self._timeDead += 1
            arena.remove(self) if self._timeDead == 60 or self.is_plusBomb() else None
        return

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._door:
            return 176, 48
        elif self._plusBomb:
            return 0, 224
        elif not self._destructible:
            return 48, 48
        elif self._timeDead == 0:
            return 64, 48
        elif self._timeDead < 10:
            return 80, 48
        elif self._timeDead < 20:
            return 96, 48
        elif self._timeDead < 30:
            return 112, 48
        elif self._timeDead < 40:
            return 128, 48
        elif self._timeDead < 50:
            return 144, 48
        return 160, 48
    

    def is_destructible(self) -> bool:
        return self._destructible
    
    def is_door(self) -> bool:
        return self._door
    
    def is_plusBomb(self) -> bool:
        return self._plusBomb
    
    def hasHitbox(self) -> bool:
        if self._door:
            return False
        elif self._plusBomb:
            return False
        return True

    def kill(self):
        self._timeDead = 1