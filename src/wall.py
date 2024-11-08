from main import TILE
from actor import Actor, Arena, Point

class Wall(Actor):
    def __init__(self, pos, destructible=False):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._destructible = destructible

    def move(self, arena: Arena):
        return

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return (80, 48) if not self._destructible else (96, 48)

    def is_destructible(self) -> bool:
        return self._destructible