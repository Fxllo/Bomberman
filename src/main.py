import sys; sys.path.append("../")
import g2d
from arena import Actor, Arena
from wall import Wall, WallWin

class Bomberman(Actor):
    def __init__(self):
        self._x, self._y = 30, 30
        self._w, self._h = 35, 35
        self._dx, self._dy = 0, 0
        self._speed = 2
        self._color = (0, 0, 255)

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
            
        # Diagonal Movement
        if "D" in arena.current_keys() and "W" in arena.current_keys():
            self._dx = self._speed
            self._dy = -self._speed
        elif "D" in arena.current_keys() and "S" in arena.current_keys():
            self._dx = self._speed
            self._dy = self._speed
        elif "A" in arena.current_keys() and "W" in arena.current_keys():
            self._dx = -self._speed
            self._dy = -self._speed
        elif "A" in arena.current_keys() and "S" in arena.current_keys():
            self._dx = -self._speed
            self._dy = self._speed
            
        # Stop Movement
        if "D" in arena.current_keys() and "A" in arena.current_keys():
            self._dx = 0
        elif "W" in arena.current_keys() and "S" in arena.current_keys():
            self._dy = 0
            
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

        # Chjeck if Bomberman wins
        for other in arena.collisions():
            if isinstance(other, WallWin):
                print("Bomberman wins!")

        arena_w, arena_h = arena.size()
        self._x = (self._x + self._dx)
        self._y = (self._y + self._dy)

    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def color(self):
        return self._color

    def sprite(self):
        return None

def tick():
    g2d.clear_canvas()
    for a in arena.actors():
        g2d.draw_text(str(a.pos()), (int(a.pos()[0]), int(a.pos()[1] - 10)), 20)
        g2d.draw_rect_with_color(a.pos(), a.size(), a.color())

    arena.tick(g2d.current_keys())

def spawnAll():
    arena.spawn(Wall((0, 0), (1200, 20)))
    arena.spawn(Wall((0, 0), (20, 800)))
    arena.spawn(Wall((0, 780), (1200, 20)))
    arena.spawn(Wall((1180, 0), (20, 700)))
    arena.spawn(WallWin((1180, 700), (20, 80)))
    arena.spawn(Bomberman())


arena = Arena((1200, 800))
def main():
    g2d.init_canvas(arena.size())
    spawnAll()
    g2d.main_loop(tick, 120)


if __name__ == "__main__":
    main()