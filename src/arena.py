Point = tuple[float, float]

class Actor:
    def move(self, arena: "Arena"):
        raise NotImplementedError("Abstract method")

    def pos(self) -> Point:
        raise NotImplementedError("Abstract method")

    def size(self) -> Point:
        raise NotImplementedError("Abstract method")

    def sprite(self) -> Point | None:
        raise NotImplementedError("Abstract method")


def check_collision(a1: Actor, a2: Actor) -> bool:
    x1, y1, w1, h1 = a1.pos() + a1.size()
    x2, y2, w2, h2 = a2.pos() + a2.size()
    return (y2 <= y1 + h1 and y1 <= y2 + h2 and
            x2 <= x1 + w1 and x1 <= x2 + w2)


class Arena():
    def __init__(self, size: Point):
        self._w, self._h = size
        self._count = 0
        self._turn = -1
        self._actors = []
        self._curr_keys = self._prev_keys = tuple()
        self._collisions = []

    def spawn(self, a: Actor):
        if a not in self._actors:
            self._actors.append(a)

    def kill(self, a: Actor):
        if a in self._actors:
            self._actors.remove(a)

    def tick(self, keys=[]):
        actors = list(reversed(self._actors))
        self._detect_collisions(actors)
        self._prev_keys = self._curr_keys
        self._curr_keys = keys
        for self._turn, a in enumerate(actors):
            a.move(self)
        self._count += 1

    def _naive_collisions(self, actors):
        self._collisions.clear()
        for a1 in actors:
            colls1 = []
            for a2 in actors:
                if a1 is not a2 and check_collision(a1, a2):
                    colls1.append(a2)
            self._collisions.append(colls1)

    def _detect_collisions(self, actors):
        self._collisions.clear()
        tile = 40
        nx, ny = -(-self._w // tile),  -(-self._h // tile)
        cells = [set() for _ in range(nx * ny)]
        for i, a in enumerate(actors):
            x, y, w, h = (round(v) for v in a.pos() + a.size())
            for tx in range((x - 1) // tile, 1 + (x + w + 1) // tile):
                for ty in range((y - 1) // tile, 1 + (y + h + 1) // tile):
                    if 0 <= tx < nx and 0 <= ty < ny:
                        cells[ty * nx + tx].add(i)
        for i, a in enumerate(actors):
            neighs = set()
            x, y, w, h = (round(v) for v in a.pos() + a.size())
            for tx in range((x - 1) // tile, 1 + (x + w + 1) // tile):
                for ty in range((y - 1) // tile, 1 + (y + h + 1) // tile):
                    if 0 <= tx < nx and 0 <= ty < ny:
                        neighs |= cells[ty * nx + tx]
            colls = [actors[j] for j in sorted(neighs, reverse=True)
                     if i != j and check_collision(a, actors[j])]
            self._collisions.append(colls)

    def collisions(self) -> list[Actor]:
        t, colls = self._turn, self._collisions
        return colls[t] if 0 <= t < len(colls) else []
        
    def actors(self) -> list:
        return list(self._actors)

    def size(self) -> Point:
        return (self._w, self._h)

    def count(self) -> int:
        return self._count

    def current_keys(self) -> list[str]:
        return self._curr_keys

    def previous_keys(self) -> list[str]:
        return self._prev_keys