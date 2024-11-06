from arena import Actor

class Wall(Actor):
    def __init__(self, pos, size, color=(0, 0, 0)):
        self._pos = pos
        self._size = size
        self._color = color

    def move(self, arena):
        return

    def pos(self):
        return self._pos

    def size(self):
        return self._size
    
    def color(self):
        return self._color

    def sprite(self):
        return None

class WallWin(Wall):
    def __init__(self, pos, size, color=(255, 0, 0)):
        self._pos = pos
        self._size = size
        self._color = color
        
    def move(self, arena):
        return

    def pos(self):
        return self._pos

    def size(self):
        return self._size
    
    def color(self):
        return self._color

    def sprite(self):
        return None