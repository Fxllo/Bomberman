from random import choices, randint
TILE, STEP = 16, 1
WIDTH, HEIGHT = 31, 25
ARENA_W, ARENA_H = TILE*WIDTH, TILE*HEIGHT
SPRITE = "https://fondinfo.github.io/sprites/bomberman.png"
NUM_BALLONS = 5

def tick():
    global bomberman  # Per utilizzare bomberman definito nel main
    g2d.clear_canvas()
    g2d.set_color((0, 150, 0)) # Grass
    g2d.draw_rect((0, 0), arena.size())
    
    for a in arena.actors():
        g2d.draw_image(SPRITE, a.pos(), a.sprite(), a.size())

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

def worldGenerator():
    from actor import Arena
    from wall import Wall
    
    arena = Arena((ARENA_W, ARENA_H))

    # Genera i muri perimetrali e interni
    for y in range(0, ARENA_H, TILE):
        for x in range(0, ARENA_W, TILE):
            if (x == 0 or y == 0 or x == ARENA_W - TILE or y == ARENA_H-TILE or x % 32 == 0 and y % 32 == 0):
                arena.spawn(Wall((x, y), destructible=False))
            elif ((x != ARENA_W/2-TILE/2-TILE or y != ARENA_H/2-TILE/2) and
                (x != ARENA_W/2-TILE/2+TILE or y != ARENA_H/2-TILE/2) and
                (x != ARENA_W/2-TILE/2 or y != ARENA_H/2-TILE/2-TILE) and
                (x != ARENA_W/2-TILE/2 or y != ARENA_H/2-TILE/2+TILE) and
                (x != ARENA_W/2-TILE/2 or y != ARENA_H/2-TILE/2) and
                choices([True, False], [0.3, 0.7])[0]):
                arena.spawn(Wall((x, y), destructible=True))
    
    # Genera una posizione casuale per la porta
    while True:
        doorX = randint(1, WIDTH-2)*TILE
        doorY = randint(1, HEIGHT-2)*TILE
        if doorX % 32 != 0 or doorY % 32 != 0:
            break
    arena.spawn(Wall((doorX, doorY), door=True))
    arena.set_exit_position((doorX, doorY))
    arena.spawn(Wall((doorX, doorY), destructible=True))
    print("Porta creata in posizione", (doorX, doorY))
    return arena
        

def main():
    global g2d, arena, bomberman  # Dichiarazione globale di bomberman
    import g2d

    from actor import Arena
    from entities import Bomberman
    from wall import Wall
    
    arena = worldGenerator()
    bomberman = Bomberman((ARENA_W/2-TILE/2, ARENA_H/2-TILE/2))
    arena.spawn(bomberman)

    spawn_balloms(arena, NUM_BALLONS)

    g2d.init_canvas(arena.size())
    g2d.main_loop(tick, 60)

if __name__ == "__main__":
    main()