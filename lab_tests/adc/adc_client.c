#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h> # Librería utilizada para Ubuntu

int main() {
    int client_socket;
    struct sockaddr_in server_addr;
    char message[] = "f8000";

    client_socket = socket(AF_INET, SOCK_STREAM, 0);

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8000);
    server_addr.sin_addr.s_addr = inet_addr("169.254.81.30");

    if (connect(client_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("Error al conectar");
        exit(1);
    }

    send(client_socket, message, sizeof(message), 0);

    close(client_socket);

    return 0;
}
