#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from random import choice
from actor import Actor, Arena, Point

TILE, STEP = 16, 4  # Dimensione della cella e passo di movimento

class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])

    def move(self, arena: Arena):
        # Cambia direzione casualmente se raggiunge un incrocio
        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])

        # Prova a muoversi nella direzione scelta
        new_x, new_y = self._x + self._dx, self._y + self._dy
        if not arena.check_collision(self, new_x, new_y):
            self._x, self._y = new_x, new_y  # Muove solo se non collide

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 240


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


class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._alive = True

    def move(self, arena: Arena):
        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = 0, 0
            keys = arena.current_keys()
            if "ArrowUp" in keys:
                self._dy = -self._speed
            elif "ArrowDown" in keys:
                self._dy = self._speed
            elif "ArrowLeft" in keys:
                self._dx = -self._speed
            elif "ArrowRight" in keys:
                self._dx = self._speed
            elif "Space" in keys:
                arena.spawn(Bomb(self.pos()))  # Piazza una bomba

        # Muove solo se non collide
        new_x, new_y = self._x + self._dx, self._y + self._dy
        if not arena.check_collision(self, new_x, new_y):
            self._x, self._y = new_x, new_y

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


class Bomb(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 100  # Countdown per esplodere

    def move(self, arena: Arena):
        self._timer -= 1
        if self._timer <= 0:
            arena.spawn(Explosion(self.pos()))  # Genera esplosione
            arena.remove(self)  # Rimuove la bomba

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 32, 16


class Explosion(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 20  # Tempo dell'esplosione

    def move(self, arena: Arena):
        self._timer -= 1
        if self._timer <= 0:
            arena.remove(self)

        # Colpisce muri e nemici
        for actor in arena.actors():
            if isinstance(actor, (Ballom, Bomberman)) and self.check_collision(actor):
                actor.kill()
            elif isinstance(actor, Wall) and actor.is_destructible() and self.check_collision(actor):
                arena.remove(actor)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 48, 16

    def check_collision(self, actor: Actor) -> bool:
        ax, ay = actor.pos()
        aw, ah = actor.size()
        return (self._x < ax + aw and self._x + self._w > ax and
                self._y < ay + ah and self._y + self._h > ay)


def tick():
    g2d.clear_canvas()
    img = "https://fondinfo.github.io/sprites/bomberman.png"
    for a in arena.actors():
        g2d.draw_image(img, a.pos(), a.sprite(), a.size())

    arena.tick(g2d.current_keys())  # Game logic


def main():
    global g2d, arena
    import g2d  # Libreria grafica

    arena = Arena((480, 360))
    # Crea la griglia completa
    for y in range(0, 360, TILE):
        for x in range(0, 480, TILE):
            if (x == 0 or y == 0 or x == 480 - TILE or y == 360 - TILE or (x % 32 == 0 and y % 32 == 0)):
                arena.spawn(Wall((x, y), destructible=False))  # Muro indistruttibile
            elif (x % 32 != 0 and y % 32 != 0 and choice([True, False])):
                arena.spawn(Wall((x, y), destructible=True))  # Muro distruttibile

    # Spawna personaggi
    arena.spawn(Ballom((48, 80)))
    arena.spawn(Ballom((80, 48)))
    arena.spawn(Bomberman((240, 160)))

    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()
