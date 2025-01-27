import time, os
from random import choices, randint
TILE, STEP = 16, 1
WIDTH, HEIGHT = 31, 25
ARENA_W, ARENA_H = TILE * WIDTH, TILE * HEIGHT
SPRITE = "https://fondinfo.github.io/sprites/bomberman.png"
NUM_BALLONS = 5
TOP_MARGIN = 60
TIMER_START = 200
time_remaining = TIMER_START
last_tick_time = None
intro_end_time = None
intro_audio_played = False
main_game_audio_played = False
numLives = 3
background = (189, 190, 189)
game_audio_path = os.path.join(os.path.dirname(__file__), "../audio/main.mp3")
death_wait_start = None

def tick():
    global bomberman, time_remaining, last_tick_time, intro_end_time, intro_audio_played, main_game_audio_played, numLives, background, game_audio_path, death_wait_start

    if intro_end_time is None:
        intro_end_time = time.time() + 3
    if time.time() < intro_end_time:
        if not intro_audio_played:
            intro_audio_path = os.path.join(os.path.dirname(__file__), "../audio/StageStart.mp3")
            g2d.play_audio(intro_audio_path, loop=False, volume=0.03)
            intro_audio_played = True

        g2d.clear_canvas_with_color((0, 0, 0))
        g2d.set_color((255, 255, 255))
        g2d.draw_text("STAGE 1", (ARENA_W // 2, (ARENA_H - 20 ) // 2), 40)
        return

    if not main_game_audio_played:
        g2d.play_audio(game_audio_path, loop=True, volume=0.3)
        main_game_audio_played = True

    if last_tick_time is None:
        last_tick_time = time.time()
    if time.time() - last_tick_time >= 1:
        time_remaining -= 1
        last_tick_time = time.time()
    if time_remaining <= 0:
        time_remaining = 0
        for actor in arena.actors():
            from entities import Ballom
            if isinstance(actor, Ballom):
                actor.setToSkull()
                
        if arena.check_victory(bomberman):
            g2d.alert("Hai vinto!")
            g2d.close_canvas()
   
    if bomberman.is_killed():
        g2d.pause_audio(game_audio_path)
        reset_game()
        return

    g2d.clear_canvas_with_color(background)

    g2d.set_color((0, 0, 0))
    g2d.draw_text(f"Time: {time_remaining} sec", (70, 20), 20)
    g2d.draw_text(f"{bomberman.score}", (arena.size()[0] // 2, 20), 20)
    g2d.draw_text(f"Left: {bomberman.count_lives() - 1}", (arena.size()[0] - 50, 20), 20)   

    g2d.set_color((0, 150, 0))
    g2d.draw_rect((0, TOP_MARGIN), arena.size())
    for a in arena.actors():
        pos_with_margin = (a.pos()[0], a.pos()[1] + TOP_MARGIN)
        g2d.draw_image(SPRITE, pos_with_margin, a.sprite(), a.size())

    arena.tick(g2d.current_keys())

def reset_game():
    global arena, bomberman, time_remaining, last_tick_time, intro_end_time, intro_audio_played, main_game_audio_played, numLives
    from entities import Bomberman

    time_remaining = TIMER_START
    last_tick_time = None
    intro_end_time = None
    intro_audio_played = False
    main_game_audio_played = False
    
    arena = worldGenerator()
    bomberman = Bomberman((ARENA_W / 2 - TILE / 2, ARENA_H / 2 - TILE / 2))
    numLives -= 1
    bomberman.set_lives(numLives)
    arena.spawn(bomberman)
    spawn_balloms(arena, NUM_BALLONS)
    return


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
    occupied_positions = {actor.pos() for actor in arena.actors()}
    spawned = 0
    
    while spawned < num_balloms:
        x = randint(1, (arena.size()[0] // TILE) - 2) * TILE
        y = randint(1, (arena.size()[1] // TILE) - 2) * TILE
        new_ballom_pos = (x, y)
        if new_ballom_pos not in occupied_positions:
            arena.spawn(Ballom(new_ballom_pos))
            occupied_positions.add(new_ballom_pos)
            spawned += 1

def worldGenerator():
    from actor import Arena
    from wall import Wall

    arena = Arena((ARENA_W, ARENA_H))

    for y in range(0, ARENA_H, TILE):
        for x in range(0, ARENA_W, TILE):
            if (x == 0 or y == 0 or x == ARENA_W - TILE or y == ARENA_H - TILE or x % 32 == 0 and y % 32 == 0):
                arena.spawn(Wall((x, y), destructible=False))
            elif ((x != ARENA_W / 2 - TILE / 2 - TILE or y != ARENA_H / 2 - TILE / 2) and
                  (x != ARENA_W / 2 - TILE / 2 + TILE or y != ARENA_H / 2 - TILE / 2) and
                  (x != ARENA_W / 2 - TILE / 2 or y != ARENA_H / 2 - TILE / 2 - TILE) and
                  (x != ARENA_W / 2 - TILE / 2 or y != ARENA_H / 2 - TILE / 2 + TILE) and
                  (x != ARENA_W / 2 - TILE / 2 or y != ARENA_H / 2 - TILE / 2) and
                  choices([True, False], [0.3, 0.7])[0]):
                if choices([True, False], [0.05, 0.95])[0]:
                    arena.spawn(Wall((x, y), plusBomb=True))
                arena.spawn(Wall((x, y), destructible=True))

    while True:
        doorX = randint(1, WIDTH - 2) * TILE
        doorY = randint(1, HEIGHT - 2) * TILE
        if doorX % 32 != 0 or doorY % 32 != 0:
            break
    arena.spawn(Wall((doorX, doorY), door=True))
    arena.set_exit_position((doorX, doorY))
    arena.spawn(Wall((doorX, doorY), destructible=True))
    return arena

def main():
    global g2d, arena, bomberman
    import g2d, os

    from entities import Bomberman

    arena = worldGenerator()
    bomberman = Bomberman((ARENA_W / 2 - TILE / 2, ARENA_H / 2 - TILE / 2))
    arena.spawn(bomberman)
    spawn_balloms(arena, NUM_BALLONS)

    g2d.init_canvas((arena.size()[0], arena.size()[1] + TOP_MARGIN))
    audio_path = os.path.join(os.path.dirname(__file__), "../audio/StageStart.mp3")
    g2d .play_audio(audio_path, loop=False, volume=0.01)
    
    g2d.main_loop(tick, 60)

if __name__ == "__main__":
    main()