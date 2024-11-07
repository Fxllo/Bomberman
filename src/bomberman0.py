from arena import Actor, Arena, Point, check_collision

TILE, STEP = 40, 4
COLOR_BACKGROUND = (200, 200, 200)
COLOR_PLAYER = (0, 128, 255)
COLOR_WALL = (128, 128, 128)

# Classe Wall per i muri
class Wall(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE

    def move(self, arena: Arena):
        return

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return None  # Nessun sprite specifico per il muro

# Classe Bomberman
class Bomberman(Actor):
    def __init__(self):
        self._x, self._y = 200, 200
        self._dx, self._dy = 0, 0
        self._w, self._h = TILE/1.05, TILE/1.05
        self._speed = STEP

    def move(self, arena):
        self._dx = 0
        self._dy = 0
        
        # Basic Movement
        if "D" in arena.current_keys():
             self._dx = self._speed
        elif "A" in arena.current_keys():
             self._dx = -self._speed
        elif "W" in arena.current_keys():
            self._dy = -self._speed
        elif "S" in arena.current_keys():
            self._dy = self._speed
            
        for other in arena.collisions():
            wall_x, wall_y = other.pos()
            wall_w, wall_h = other.size()
            
            if self._y < wall_y and self._dy >= 0:
                self._y = wall_y - self._h
                self._dy = 0
            elif self._y + self._h > wall_y + wall_h and self._dy <= 0:
                self._y = wall_y + wall_h + 1
                self._dy = 0
            elif self._x < wall_x and self._dx >= 0:
                self._x = wall_x - self._w
                self._dx = 0
            elif self._x + self._w > wall_x + wall_w and self._dx <= 0:
                self._x = wall_x + wall_w
                self._dx = 0

        arena_width, arena_height = arena.size()
        if self._x + self._dx < 0:
            self._x = 0
        elif self._x + self._w + self._dx > arena_width:
            self._x = arena_width - self._w
        if self._y + self._dy < 0:
            self._y = 0
        elif self._y + self._h + self._dy > arena_height:
            self._y = arena_height - self._h - self._speed

        self._x = (self._x + self._dx)
        self._y = (self._y + self._dy)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return None


# Funzioni di rendering e aggiornamento
def draw_grid():
    """Disegna la griglia con sfondo, muri e giocatore."""
    g2d.clear_canvas()
    
    # Disegna i muri
    g2d.set_color(COLOR_WALL)
    for actor in arena.actors():
        if isinstance(actor, Wall):
            g2d.draw_rect(actor.pos(), actor.size())
            
    # Disegna il giocatore
    g2d.set_color(COLOR_PLAYER)
    for actor in arena.actors():
        if isinstance(actor, Bomberman):
            g2d.draw_rect(actor.pos(), actor.size())

def tick():
    g2d.clear_canvas()
    draw_grid()
    arena.tick(g2d.current_keys())

def main():
    global arena, g2d
    import g2d
    arena = Arena((520, 400))  

    g2d.init_canvas(arena.size())
    
    for x in range(0, 520, TILE):
        arena.spawn(Wall((x, 0)))
        arena.spawn(Wall((x, 400 - TILE)))
    for y in range(0, 400, TILE):
        arena.spawn(Wall((0, y)))
        arena.spawn(Wall((520 - TILE, y)))

    # Muri interni a scacchiera
    for x in range(TILE * 2, 520 - TILE * 2, TILE * 2):
        for y in range(TILE * 2, 400 - TILE * 2, TILE * 2):
            arena.spawn(Wall((x, y)))
            
    arena.spawn(Bomberman())
    
    g2d.main_loop(tick, 120)

if __name__ == "__main__":
    main()