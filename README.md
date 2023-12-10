<p align="center">
    <a>
        <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4862cebc-a29e-43c8-a9df-5b0889d30ed4/df6ii6o-859bcbab-fdf0-41c3-ab39-87ee634545fa.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzQ4NjJjZWJjLWEyOWUtNDNjOC1hOWRmLTViMDg4OWQzMGVkNFwvZGY2aWk2by04NTliY2JhYi1mZGYwLTQxYzMtYWIzOS04N2VlNjM0NTQ1ZmEucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Zc7hONno1P9pdPckPPhppidyW1wu0s9T9wKjlRdwIo8"     width="600" alt="Torneo de Cell" />
    </a>
</p>   


#### JUEGO “BATTLE ROYALE DE BOMBERMAN”
##### Battle Royale de Bomberman 


Juego en python y servidor en C. Que permite jugar hasta 4 jugadores en una misma partida. Donde el objetivo es ser el último jugador en pie.

Es un juego de acción, donde los jugadores se mueven en un laberinto y deben colocar bombas para destruir obstáculos y eliminar a los otros jugadores.

![Juego en ejecucion](./src/assets/img/game_v0.5.png)


###### Instalaciones necesarias para ejecutar el juego

###### Manual del Juego

w,s,a,d: Movimiento del jugador
space: Colocar bomba

###### Reglas del Juego

Tres vidas por jugador.
El jugador que quede vivo gana.

###### Arquitectura General 
 
Desde el punto de Sistemas Operativos, el juego tiene una arquitectura cliente servidor, donde el servidor es un software multiproceso y multihebra con una gestión de recursos que le permita asegurar su coordinación y consistencia (procesos, hebras, memoria y archivos). Por el lado del cliente, este es un software gráfico donde se despliega el contenido del juego y permite capturar la interacción del usuario. 
 - A continuación, un esquema: 

![Arquitectura](./src/assets/img/arquitectura_juego.png)
 
##### Ejemplo de ejecución del juego: 

###### Servidor

En la carpeta server se encuentra el código del servidor.

Se compila con: gcc -pthread -o servidor server.c
Se ejecuta con: ./servidor [puerto]

###### Cliente

En la carpeta client se encuentra el código del cliente. Donde se pueden ejecutar hasta 4 instancias del cliente.

Se ejecuta con: python -m client.main

```bash

Read Client 1: {"player_position": [80, 79], "player_bombs_throwed": [], "player_direction": "down"}
Write Client 0: {"id": 1, "message": {"player_position": [80, 79], "player_bombs_throwed": [], "player_direction": "down"}}
Read Client 0: {"player_position": [48, 51], "player_bombs_throwed": [], "player_direction": "down"}
Write Client 1: {"id": 0, "message": {"player_position": [48, 51], "player_bombs_throwed": [], "player_direction": "down"}}
Read Client 1: {"player_position": [80, 79], "player_bombs_throwed": [], "player_direction": "down"}
Write Client 0: {"id": 1, "message": {"player_position": [80, 79], "player_bombs_throwed": [], "player_direction": "down"}}
Read Client 0: {"player_position": [48, 51], "player_bombs_throwed": [], "player_direction": "down"}
Write Client 1: {"id": 0, "message": {"player_position": [48, 51], "player_bombs_throwed": [], "player_direction": "down"}}
Read Client 1: {"player_position": [80, 79], "player_bombs_throwed": [], "player_direction": "down"}

```