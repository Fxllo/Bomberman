from main import TILE
from actor import Actor, Arena, Point

class Wall(Actor):
    def __init__(self, pos, destructible=False, **kwargs):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._destructible = destructible
        self._door = kwargs.get('door', False)

    def move(self, arena: Arena):
        return

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._door:
            return 176, 48
        elif self._destructible:
            return 64, 48
        return 48, 48

    def is_destructible(self) -> bool:
        return self._destructible
    
    def is_door(self) -> bool:
        return self._door