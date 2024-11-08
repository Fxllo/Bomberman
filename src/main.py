from random import choice, randint
TILE, STEP = 16, 4 

def tick():
    g2d.clear_canvas()
    img = "https://fondinfo.github.io/sprites/bomberman.png"
    for a in arena.actors():
        g2d.draw_image(img, a.pos(), a.sprite(), a.size())

    arena.tick(g2d.current_keys())

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
            print("Erorre: posizione occupata, riprova.")
            
def main():
    global g2d, arena
    import g2d

    from actor import Arena
    from entities import Bomberman
    from wall import Wall
    
    while True:
        arena = Arena((480, 360))
        for y in range(0, 360, TILE):
            for x in range(0, 480, TILE):
                if (x == 0 or y == 0 or x == 480 - TILE or y == 360 - TILE or (x % 32 == 0 and y % 32 == 0)):
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