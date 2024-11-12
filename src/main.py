from random import choice, randint
TILE, STEP = 16, 4 

def tick():
    global bomberman  # Per utilizzare bomberman definito nel main
    g2d.clear_canvas()
    img = "https://fondinfo.github.io/sprites/bomberman.png"
    for a in arena.actors():
        g2d.draw_image(img, a.pos(), a.sprite(), a.size())

    arena.tick(g2d.current_keys())

    # Controllo della vittoria
    if arena.check_victory(bomberman):
        g2d.alert("Hai vinto!")
        g2d.close_canvas()

def is_bomberman_trapped(bomberman, arena):
    from wall import Wall
    x, y = bomberman.pos()
    surrounding_positions = [(x + TILE, y), (x - TILE, y), (x, y + TILE), (x, y - TILE)]
    
    for pos in surrounding_positions:
        if not any(isinstance(actor, Wall) and actor.pos() == pos for actor in arena.actors()):
            return False
    return True

def spawn_balloms(arena, num_balloms=5):
    from entities import Ballom
    
    spawned = 0
    while spawned < num_balloms:
        x = randint(1, (arena.size()[0] // TILE) - 2) * TILE
        y = randint(1, (arena.size()[1] // TILE) - 2) * TILE
        new_ballom_pos = (x, y)
        
        if not any(actor.pos() == new_ballom_pos for actor in arena.actors()):
            arena.spawn(Ballom(new_ballom_pos))
            spawned += 1
        else:
            print("Errore: posizione occupata, riprova.")

def main():
    global g2d, arena, bomberman  # Dichiarazione globale di bomberman
    import g2d

    from actor import Arena
    from entities import Bomberman
    from wall import Wall
    
    while True:
        arena = Arena((480, 390))
        
        # Genera una posizione casuale per l'uscita sui bordi
        edge = choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            exit_position = (randint(1, (arena.size()[0] // TILE) - 2) * TILE, 0)
        elif edge == 'bottom':
            exit_position = (randint(1, (arena.size()[0] // TILE) - 2) * TILE, arena.size()[1] - TILE)
        elif edge == 'left':
            exit_position = (0, randint(1, (arena.size()[1] // TILE) - 2) * TILE)
        else:  # right
            exit_position = (arena.size()[0] - TILE, randint(1, (arena.size()[1] // TILE) - 2) * TILE)

        # Imposta la posizione dell'uscita nell'arena
        arena.set_exit_position(exit_position)

        # Crea muri lungo i bordi, tranne la posizione scelta per l'uscita
        for y in range(0, 390, TILE):
            for x in range(0, 480, TILE):
                if (x, y) == exit_position:
                    continue  # Lascia vuoto per l'uscita
                if (x == 0 or y == 0 or x == 480 - TILE or y == 390 or (x % 32 == 0 and y % 32 == 0)):
                    arena.spawn(Wall((x, y), destructible=False))
                elif (x % 32 != 0 and y % 32 != 0 and choice([True, False])):
                    arena.spawn(Wall((x, y), destructible=True))

        bomberman = Bomberman((240, 160))
        arena.spawn(bomberman)

        if is_bomberman_trapped(bomberman, arena):
            print("Bomberman è circondato da muri, riprova.")
        else:
            break

    spawn_balloms(arena, num_balloms=5)

    g2d.init_canvas(arena.size())
    g2d.main_loop(tick, 60)

if __name__ == "__main__":
    main()