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
        self._to_remove: List[Actor] = []  # Attori da rimuovere

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
        self._keys = keys  # memorizza i tasti attivi
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
        """Controlla se l'attore collide con un altro attore o con i bordi."""
        ax, ay = actor.pos()
        aw, ah = actor.size()
        for other in self._actors:
            if other is not actor:
                ox, oy = other.pos()
                ow, oh = other.size()
                # Controllo delle collisioni rettangolari
                if (new_x < ox + ow and new_x + aw > ox and
                    new_y < oy + oh and new_y + ah > oy):
                    return True
        # Controllo collisione con i bordi dell'arena
        if not (0 <= new_x <= self._width - aw and 0 <= new_y <= self._height - ah):
            return True
        return False
