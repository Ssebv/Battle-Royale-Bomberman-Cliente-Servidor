# Se ejecuta con: python -m client.main

from .game.map import *
from .game.player import *
from .game.inventory import *
from .game.bomb import *
from .game.constants import *
import sys
import time
import socket
import json
import threading

lock = threading.Lock() 
stop_signal = threading.Event()  

players = [] 
bombs = [] 
other_players = {}  

player_positions = [(60,60), (60,540), (540,60), (540,540)]

# * Configuración del servidor a conectarse
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_HOST = "localhost"
SERVER_PORT = 65000

def start_client(player):
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
        
        threading.Thread(target=handle_server_data, args=(stop_signal,)).start()
        threading.Thread(target=send_game_data, args=(player, stop_signal)).start()

    except Exception as e:
        print(f"No se pudo conectar a {SERVER_HOST}:{SERVER_PORT}: {e}")
        sys.exit(1)

    print("Cliente iniciado")
    
def send_game_data(player, stop_signal):
    while not stop_signal.is_set():
        time.sleep(0.00001)
        with lock:
            for bomb in player.bombs_thrown:
                game_state = {
                    "player_position": (player.rect.x, player.rect.y),
                    "player_bombs_throwed": [bomb.position],
                    "player_direction": player.direction, 
                }
                game_state_str = json.dumps(game_state)
                if client_socket.fileno() != -1:
                    client_socket.send(game_state_str.encode())
                else:
                    print("Socket desconectado, gracias por jugar")
                
            player.bombs_thrown = []

def handle_server_data(stop_signal):
    while not stop_signal.is_set():
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Disconnected from server")
                sys.exit(0)

            received_data = json.loads(data.decode())
            client_id = received_data['id']
            player_position = received_data['message']['player_position']
            bombs_positions = received_data['message']['player_bombs_throwed']
            player_direction = received_data['message']['player_direction']

            print(f"Received data from client {client_id}: {received_data}")
            
            if len(bombs_positions) > 0:
                print(f"bombs_positions: {bombs_positions}")
            
                other_players[client_id].inventory.add_bomb(Bomb())
                bomb = other_players[client_id].throw_bomb(bombs_positions[0])  
                bombs.append(bomb)
                
            if client_id not in other_players:
                other_players[client_id] = Player(*player_positions[client_id]) 


            other_players[client_id].rect.x, other_players[client_id].rect.y = player_position
            other_players[client_id].direction = player_direction
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)

        except Exception as e:
            print(f"Error receiving data from server: {e}")
            sys.exit(1)

def find_nearest_square(position, tile_size):
    x, y = position
    grid_x = round(x / tile_size) * tile_size
    grid_y = round(y / tile_size) * tile_size
    return (grid_x, grid_y)

def main(winstyle=0):
    pg.init()  
 
    
    clock = pg.time.Clock()
    game_time = 0
    previus_time = time.time()
    font = pg.font.Font(None, 24)
    bomb_cooldown = 0
    height = SCREENRECT.height

    pg.display.set_caption("BOMBERMAN")
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    tiles_images = load_tile_images()
    player_images = load_player_images()
    bomb_images = load_bomb_images()
    game_map = Map(MAP) 

    players.append(Player(60,60))
    player = players[0]
    
    start_client(player) 
    
    while True:
        clock.tick(45)
        game_time += clock.get_time() / 600

        keys_pressed = pg.key.get_pressed()

        current_time = time.time()
        dt = current_time - previus_time

        game_map.draw_map(screen, tiles_images)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                with lock:
                    client_socket.shutdown(socket.SHUT_RDWR) 
                    client_socket.close() 
                stop_signal.set() 
                pg.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: 
                    with lock:
                        client_socket.shutdown(socket.SHUT_RDWR)
                        client_socket.close()
                    stop_signal.set()
                    pg.quit()
                    sys.exit()

                if event.key == pg.K_SPACE:
                    print("Espacio presionado")
                    
                    if player.inventory.has_bomb(): 
                        print("El jugador tiene una bomba")
                        
                        nearest_square = find_nearest_square(player.rect.topleft, TILE_SIZE)
                        bomb = player.throw_bomb(nearest_square)
                        bomb.in_inventory = False   
                        bombs.append(bomb)

                        bomb_cooldown = BOMB_COOLDOWN                                                         
        
                    else:
                        print("El jugador no tiene bombas")
        
        for bomb in bombs:
            bomb.update(dt)
            bomb.draw(screen)

            if bomb.is_exploded and bomb.current_frame > 2:
                if not bomb.hit_player and player.rect.colliderect(bomb.rect):
                    print("¡El jugador ha sido golpeado por la explosión!")
                    player.life -= 1
                    bomb.hit_player = True
                    if player.life == 0:
                        print("El jugador ha perdido todas sus vidas")
                        print("El jugador ha muerto")
                        player.is_alive = False   

            if bomb.current_frame == 6:
                bombs.remove(bomb)

        for player_id, other_player in other_players.items():
            other_player.draw(screen)  
            other_player.render(screen) 

        for player in players:
            if player.is_alive:
                player.update(keys_pressed, game_map)
                player.draw(screen)
                
                game_state_str = f"Jugador : {player.rect.x}, {player.rect.y}"
                print(game_state_str)
                
                game_state = {
                    "player_position": (player.rect.x, player.rect.y),
                    "player_bombs_throwed": [bomb.position for bomb in player.bombs_thrown if not bomb.in_inventory],
                    "player_direction": player.direction,
                }
            
                game_state_str = json.dumps(game_state)
                
                if client_socket.fileno() != -1:
                    client_socket.send(game_state_str.encode())
                else:
                    print("El socket no está conectado")          
    
        if bomb_cooldown > 0:
            bomb_cooldown -= dt

        elif bomb_cooldown <= 0 and not player.inventory.has_bomb():
            print("Enfriamiento de la bomba completado")
            print("Añadiendo bomba al inventario del jugador")
            player.inventory.add_bomb(Bomb())
        
        # nearest_square = find_nearest_square(player.rect.topleft, TILE_SIZE) 

        # ! Dibujar el cuadrado más cercano
        # pg.draw.rect(screen, (255, 0, 0), pg.Rect(nearest_square[0], nearest_square[1], TILE_SIZE, TILE_SIZE), 2)
        # pg.draw.rect(screen, (255, 0, 0), player.rect, 2) 

        ## *  Dibujar el panel
        time_text = font.render(f'{int(game_time)}´', True, (215, 215, 215))
        screen.blit(font.render("JUGADOR ", True, (215, 215, 215)), (20, height / 2 - 388))
        screen.blit(player_images[0], (20 + 90, height / 2 - 388))
        screen.blit(font.render(f" x {players[0].kills}", True, (215, 215, 215)), (20 + 90 + 20, height / 2 - 388))
        screen.blit(time_text, (SCREENRECT.width - time_text.get_width() - 20, PANEL_LIBE / 2 - time_text.get_height() / 1 + 1))
        screen.blit(font.render("VIDAS ", True, (215, 215, 215)), (20, PANEL_LIBE / 2 - 15))
        inventory_rect1 = pg.Rect(360, PANEL_LIBE / 2 - 27, 40, 40)
        inventory_rect2 = pg.Rect(400, PANEL_LIBE / 2 - 27, 40, 40)
        inventory_rect3 = pg.Rect(440, PANEL_LIBE / 2 - 27, 40, 40)
        pg.draw.rect(screen, (69, 50, 46), inventory_rect1, 4)
        pg.draw.rect(screen, (69, 50, 46), inventory_rect2, 4)
        pg.draw.rect(screen, (69, 50, 46), inventory_rect3, 4)
        screen.blit(font.render("INVENTARIO ", True, (215, 215, 215)), (245, PANEL_LIBE / 2 - 15))
        
        if bomb_cooldown > 0:
            screen.blit(font.render(f"{bomb_cooldown:.1f}´", True, (215, 215, 215)), (366, PANEL_LIBE / 2 - 15))    
        else:
            bomb_image = pg.transform.scale(bomb_images[0], (30, 30))
            screen.blit(bomb_image, (363, PANEL_LIBE / 2 - 23))

        for i in range(players[0].life):
            screen.blit(player_images[0], (88 + i * 30, PANEL_LIBE / 2 - 14.5))
        ## * Dibujar el panel

        pg.display.flip()
        previus_time = current_time
        clock.tick(45)
    
if __name__ == "__main__":
    main()
    pg.quit()