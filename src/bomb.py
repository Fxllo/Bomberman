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
            arena.spawn(Explosion(self.pos(), arena.get_bomberman(), arena))  
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
    def __init__(self, pos, bomberman, arena):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 20
        self._bomberman = bomberman
        self._arena = arena

        self._explosion_blocks = [
            (self._x, self._y),               # Centro
            (self._x, self._y - TILE),        # Su
            (self._x, self._y + TILE),        # Giù
            (self._x - TILE, self._y),        # Sinistra
            (self._x + TILE, self._y)         # Destra
        ]
        
        self._valid_explosion_blocks = self._filter_valid_blocks(self._explosion_blocks)
        
    def _filter_valid_blocks(self, blocks) -> list:
        mask = [True, True, True, True, True]  # Mask per ciascun blocco (centrale, sopra, sotto, sinistra, destra)
        
        for i, (bx, by) in enumerate(blocks):
            if i == 0:  # Non controlliamo il centro
                continue
            for actor in self._arena.actors():
                if isinstance(actor, Wall):  # Controlla se è un muro
                    ax, ay = actor.pos()
                    aw, ah = actor.size()
                    if (bx < ax + aw and bx + self._w > ax and
                        by < ay + ah and by + self._h > ay):
                        mask[i] = False  # Se c'è una collisione con un muro, il blocco diventa non valido
                        break
        print(mask)
        return mask

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

        for bx, by in self._explosion_blocks:
            if (bx < ax + aw and bx + self._w > ax and
                by < ay + ah and by + self._h > ay):
                return True
        return False

    def pos(self) -> Point:
        return self._x - TILE, self._y - TILE

    def size(self) -> Point:
        return self._w * 3, self._h * 3
    
    def sprite(self) -> list:
        if self._timer < 5:
            sprite_x, sprite_y = 97, 160
        elif self._timer < 10:
            sprite_x, sprite_y = 16, 160
        elif self._timer < 15:
            sprite_x, sprite_y = 97, 80
        else:
            sprite_x, sprite_y = 16, 80

        x, y = self.pos()
        size_x, size_y = self.size()

        if not self._valid_explosion_blocks[1]:
            y += TILE
            if self._timer > 10:
                sprite_y = 97
            else:
                sprite_y = 176
        elif not self._valid_explosion_blocks[2]:
            size_y = 2 * TILE
            y -= TILE
            if self._timer > 10:
                sprite_y = 97
            else:
                sprite_y = 176
        elif not self._valid_explosion_blocks[3]:
            x += TILE
            if self._timer < 5:
                sprite_x = 110
            elif self._timer < 10:
                sprite_x = 31
            elif self._timer < 15:
                sprite_x = 112
            else:
                sprite_x = 34
        elif not self._valid_explosion_blocks[4]:
            size_x = 2 * TILE
            x -= TILE
            if self._timer < 5:
                sprite_x = 110
            elif self._timer < 10:
                sprite_x = 31
            elif self._timer < 15:
                sprite_x = 112
            else:
                sprite_x = 34
            
        return sprite_x, sprite_y, x, y, size_x, size_y