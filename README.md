<p align="center">
    <a>
        <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4862cebc-a29e-43c8-a9df-5b0889d30ed4/df6ii6o-859bcbab-fdf0-41c3-ab39-87ee634545fa.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzQ4NjJjZWJjLWEyOWUtNDNjOC1hOWRmLTViMDg4OWQzMGVkNFwvZGY2aWk2by04NTliY2JhYi1mZGYwLTQxYzMtYWIzOS04N2VlNjM0NTQ1ZmEucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Zc7hONno1P9pdPckPPhppidyW1wu0s9T9wKjlRdwIo8"     width="600" alt="Torneo de Cell" />
    </a>
</p>   

# Proyecto Sistema Operativo
+ **Fecha de entrega:** 27 de junio, 2023 (Incluye Presentacion)

#### PROYECTO JUEGO “EL TORNEO DE CELL”
##### Battle Royale de Bomberman 

El juego “Torneo de Cell” es un juego multijugador tipo Battle Royale. Varios jugadores se enfrentan dentro de un laberinto donde pueden atacarse mutuamente con bombas que explotan con un patrón de impacto definido. En este juego, gana el jugador que sobrevive. Después de cierto tiempo, donde se permite a los jugadores recolectar bombas y otros ítems, el escenario se va haciendo cada vez más pequeño hasta un punto donde, si no lo han hecho, se les obliga a enfrentarse. Para una idea similar del juego pueden ver la siguiente versión en YouTube 

* [Boomberman - YouTube](https://www.youtube.com/watch?v=6wJDIoAWmNcArquitectura)

###### Instalaciones necesarias para ejecutar el juego

...

###### Manual del Juego
...

###### Reglas

...
###### Arquitectura General 
 
Desde el punto de Sistemas Operativos, el juego tiene una arquitectura cliente servidor, donde el servidor es un software multiproceso y multihebra con una gestión de recursos que le permita asegurar su coordinación y consistencia (procesos, hebras, memoria y archivos). Por el lado del cliente, este es un software gráfico donde se despliega el contenido del juego y permite capturar la interacción del usuario. 
 - A continuación, un esquema: 
 
 <p align="center">
    <a>
        <img src="./src/img/arquitectura_juego.png"    width="600" alt="Arquitectura Juego" />
    </a>
</p>  
 
 
###### Servidor: 
Un software en Linux que recibe las acciones de los jugadores (movimientos) y ejecuta la lógica del juego, tomando en consideración todas las acciones de todos los jugadores, para luego, enviar a todos los jugadores el resultado de dichas acciones. El servidor es similar a cualquier servidor de videojuegos, pues centraliza el procesamiento del juego, permite crear partidas y controla la conexión y desconexión de los jugadores.
 
 Algunas consideraciones para tener en cuenta: 
 
 - El servidor puede crear más de una partida al mismo tiempo: Mediante un mecanismo multiproceso, el servidor dedica un proceso para cada partida. Esto permite que, si una partida tiene problemas o el proceso falla, otras partidas sigan ejecutándose sin problemas.
 - El servidor puede atender, dentro de una partida, a más de un jugador al mismo tiempo (mismo proceso): mediante un mecanismo de concurrencia multi-hebra, el servidor debe recibir en todo momento las acciones en tiempo real del jugador (tecla que presionó, botón, etc.). Luego, mediante memoria compartida y la atención concurrente de todos los jugadores, sin dejar de lado mecanismos de sincronización y exclusión mutua sobre los recursos compartidos, debe simular internamente las acciones de los jugadores y comunicar a los clientes el resultado de estas.
 - El cliente jugador puede ser mono-hebra o multi-hebra, por lo que se deja a decisión del grupo la forma de implementarlo
 - El cliente jugador debe ser gráfico y presentar una interfaz típica de juego.
 - El servidor debe ejecutarse en S.O. Linux y los clientes en S.O. Windows o MacOS. 
 - Se debe utilizar C para el servidor y Python para el cliente.
 - Se debe demostrar el funcionamiento online en varios computadores al mismo tiempo (ojo, no es necesario varios computadores para desarrollar)Servidor (Linux) Jugador n (Windows) Jugador 1 (Windows) 

###### Reglas del Juego: 
- Al inicio, cada cliente se conecta indicando la dirección IP del servidor y puerto. 
- Luego, el cliente tiene dos opciones:  
    - 1) Iniciar una partida indicando la cantidad máxima de jugadores permitidos: aquí, se genera una pantalla, donde se espera a que se unan la cantidad de jugadores indicados. El jugador da un nombre a la partida. 
    - 2) Unirse a una partida creada que aparece en una lista: aquí, el jugador selecciona de una lista una de las partidas que están en espera seleccionando por el nombre de la partida. 

- Las reglas del juego pueden ser flexibles, siempre y cuando cumplan con que es un Battle Royale, multijugador al estilo de Bomberman indicado en el video expuesto anteriormente. No es necesario que el juego tenga toda la complejidad del original, pero debe ser “jugable, online y multijugador”. 

###### Prohibiciones:

- Se prohíbe el uso de soluciones existentes, se verificará código.  
- La interfaz de los jugadores debe ser gráfica. 

###### Recursos Disponibles: 

- Instalar módulo pygame para Python https://www.pygame.org/
- Pueden obtener sonidos gratis para este tipo de juegos en https://freesound.org/
- Utilizar ejemplos de códigos disponibles en clases y/o laboratorios. 
###### Restricciones: 

Las restricciones lista aquellas condiciones que deben cumplirse para poder acceder a la revisión del proyecto. No se revisarán programas que no cumplan las restricciones.
- Se prohíbe el uso de soluciones existentes, se verificará código.  
- La interfaz de los jugadores debe ser gráfica. 
- Debe comentar el código para la entrega. 
- Al momento de presentar no puede usar código con comentarios (solo al presentar). 
- Programas que no puedan ejecutarse (cualquier motivo) no serán revisados y se considerará como no entrega 
- Debe incluir las instrucciones para utilizar el servidor y clientes. Debe incluir un manual del juego y sus reglas

###### Criterios de Evaluación

- Utilizar multiprocesos de forma correcta **(10)**
- Utiliza multi-hebra de forma correcta  **(10)**
- El servidor está implementado para Linux y Lenguaje C en forma correcta **(20)**
- El cliente está implementado para Windows en Lenguaje Python en forma correcta **(20)** 
Se utilizan mecanismos de sincronización y exclusión mutua de forma correcta  **(15)** 
- Originalidad del juego, jugabilidad, estética **(10)**
- Presentación **(15)** 
- Incumple con las restricciones algorítmicas o generales, entrega atrasada **(-30)**
- El juego o el código es copia de otro juego o contiene porciones considerables de copia de otro compañero o soluciones de internet **(-30)**