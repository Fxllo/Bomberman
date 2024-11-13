from typing import Tuple, List, Optional
from abc import ABC, abstractmethod

# Definizione di un tipo Point per rappresentare le coordinate
Point = Tuple[int, int]

class Actor(ABC):
    """Classe base per tutti gli attori nel gioco."""

    @abstractmethod
    def move(self, arena: 'Arena'):
        """Aggiorna la posizione dell'attore (implementata nelle sottoclassi)."""
        pass

    @abstractmethod
    def pos(self) -> Point:
        """Restituisce la posizione attuale dell'attore."""
        pass

    @abstractmethod
    def size(self) -> Point:
        """Restituisce la dimensione dell'attore."""
        pass

    @abstractmethod
    def sprite(self) -> Point:
        """Restituisce la posizione del frammento di sprite da usare."""
        pass


class Arena:
    """Gestisce l'arena di gioco, gli attori, e le interazioni."""

    def __init__(self, size: Tuple[int, int]):
        self._width, self._height = size
        self._actors: List[Actor] = []
        self._keys: List[str] = []
        self._to_remove: List[Actor] = []
        self._exit_position = None# Attori da rimuovere

    def size(self) -> Point:
        """Restituisce la dimensione dell'arena."""
        return self._width, self._height

    def spawn(self, actor: Actor):
        """Aggiunge un attore all'arena."""
        self._actors.append(actor)

    def remove(self, actor: Actor):
        """Contrassegna un attore per la rimozione."""
        if actor in self._actors and actor not in self._to_remove:
            self._to_remove.append(actor)

    def actors(self) -> List[Actor]:
        """Restituisce una lista di tutti gli attori presenti nell'arena."""
        return [a for a in self._actors if a not in self._to_remove]

    def tick(self, keys: List[str]):
        """Aggiorna lo stato di ogni attore."""
        self._keys = keys
        for actor in self._actors:
            if actor not in self._to_remove:
                actor.move(self)
        # Rimuove gli attori contrassegnati per la rimozione
        for actor in self._to_remove:
            self._actors.remove(actor)
        self._to_remove.clear()

    def current_keys(self) -> List[str]:
        """Restituisce i tasti attivi correnti."""
        return self._keys

    def check_collision(self, actor: Actor, new_x: int, new_y: int) -> bool:
        from bomb import Bomb
        from entities import Bomberman, Ballom
        from wall import Wall
        for other_actor in self.actors():
            if actor != other_actor:
                # Ignora le bombe se sono attraversabili e l'attore è Bomberman o Ballom, la porta se è Bomberman
                if isinstance(other_actor, Bomb) and other_actor.is_passable() and isinstance(actor, (Bomberman, Ballom)):
                    continue  # Non considera questa bomba nella collisione
                if isinstance(other_actor, Ballom) and other_actor.is_passable() and isinstance(actor, Bomberman):
                    continue  # Non considera questa bomba nella collisione
                if isinstance(other_actor, Wall) and other_actor.is_door() and isinstance(actor, Bomberman):
                    continue # Non considera la porta nella collisione
                
                ox, oy = other_actor.pos()
                ow, oh = other_actor.size()
                if (new_x < ox + ow and new_x + actor.size()[0] > ox and
                    new_y < oy + oh and new_y + actor.size()[1] > oy):
                    return True
        return False
    
    def set_exit_position(self, position):
        self._exit_position = position

    def check_victory(self, bomberman):
        return bomberman.pos() == self._exit_position
    
    def get_bomberman(self):
        for actor in self.actors():
            from entities import Bomberman
            if isinstance(actor, Bomberman):
                return actor
        return None