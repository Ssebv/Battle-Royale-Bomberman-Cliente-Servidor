// ? Se compila con: gcc -pthread -o servidor server.c
// ? Se ejecuta con: ./servidor [puerto]

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <dispatch/dispatch.h>

#define MAX_CLIENTS 4 
#define BUFFER_SIZE 256

dispatch_semaphore_t semaphore; 

// * Estructura para almacenar la información de un cliente
typedef struct {
    int id;
    int sock;
    int connected; 
} client_t;

client_t clients[MAX_CLIENTS]; 
int client_count = 0;

void error(const char *msg) {
    perror(msg);
    exit(1);
}

void *handle_client(void *arg) { 
    client_t client = *(client_t *) arg;
    char buffer[BUFFER_SIZE];
    int n;

    // * Recibir y enviar datos al cliente
    while (1) {
        bzero(buffer, BUFFER_SIZE);
        n = read(client.sock, buffer, sizeof(buffer)); // ? Recibir mensaje del cliente
        if (n < 0) {
            error("ERROR reading from socket");
        } else if (n == 0) { 
            printf("Client %d disconnected\n", client.id);
            dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER); 
            clients[client.id].connected = 0; 
            dispatch_semaphore_signal(semaphore); 
            break;
        }

        // ? Imprimir el mensaje recibido
        printf("Read Client %d: %s\n", client.id, buffer);

        // ! Se envia la data como un objeto JSON válido.
        // ! Por ejemplo, puedes formatear el string como: {"id": 1, "message": {"player_position": [60, 60]}}
        char message[BUFFER_SIZE]; // * Mensaje a enviar
        sprintf(message, "{\"id\": %d, \"message\": %s}", client.id, buffer); 

        dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);

        for (int i = 0; i < client_count; i++) { // ! Enviar el mensaje a todos los clientes conectados
            if (clients[i].id != client.id && clients[i].connected) {  
                n = write(clients[i].sock, message, strlen(message));  
                printf("Write Client %d: %s\n", clients[i].id, message); 
                if (n < 0) error("ERROR writing to socket");
            }
        }
        dispatch_semaphore_signal(semaphore);
    }
    close(client.sock);
    return 0;
}

int main(int argc, char *argv[]) {
    int sockfd, portno; 
    struct sockaddr_in serv_addr; 

    semaphore = dispatch_semaphore_create(1);

    if (argc < 2) { 
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket"); 

    bzero((char *) &serv_addr, sizeof(serv_addr)); 
    portno = atoi(argv[1]); 

    serv_addr.sin_family = AF_INET; 
    serv_addr.sin_addr.s_addr = INADDR_ANY; 
    serv_addr.sin_port = htons(portno); 

    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) error("ERROR on binding"); 

    listen(sockfd, MAX_CLIENTS); 
    printf("Server listening on port %d\n", portno); 

    while (1) { 
        struct sockaddr_in cli_addr; 
        socklen_t clilen = sizeof(cli_addr); 
        int newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen); 

        if (newsockfd < 0) error("ERROR on accept"); 
        else printf("Accepted new client\n"); 
        dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER); 
        if (client_count >= MAX_CLIENTS) { 
            printf("Too many clients. Disconnecting new client...\n");
            close(newsockfd); // * Cerrar el socket del cliente
        } else {
            clients[client_count].id = client_count;
            clients[client_count].sock = newsockfd;
            clients[client_count].connected = 1;  
            pthread_t client_thread; 
            pthread_create(&client_thread, NULL, handle_client, (void *) &clients[client_count]); 
            client_count++; 
        }
        dispatch_semaphore_signal(semaphore); 
    }
    close(sockfd);
    return 0; 
}