/*
    Simple example.
    Create client on C sockets
*/

#include <stdio.h>  
#include <stdlib.h>
#include <string.h>     
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <signal.h>

#define PORT 5000
#define BUFFER_SIZE 1024
#define MESSAGE "HELLO FROM C CLIENT"
#define SERVER_IP "127.0.0.1"

int my_socket;

//handler for CTRL+C
void sigint_handler(int signal) {
    close(my_socket);
    exit(0); 
}

int main(){

    signal(SIGINT, sigint_handler);
    
    int size_byte;

    struct sockaddr_in serv_addr;

    char buffer[BUFFER_SIZE] = {0};

    //create socket
    if ((my_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\nERROR IN SOCKET CREATE\n");
        return -1;
    }

    serv_addr.sin_family = AF_INET; // define type of IP (v4 or v6)
    serv_addr.sin_port = htons(PORT); // define server port

    //translate const char* to IP format
    if (inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    //connect to server
    if (connect(my_socket, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }

    printf("CONNECT TO SERVER [PORT, IP] %s:%d\n", SERVER_IP, PORT);

    //start data transmission
    while (1){
        size_byte = send(my_socket, MESSAGE, strlen(MESSAGE), 0);
        printf("CLIENT SEND TO SERVER %d BYTE\n", size_byte);
        sleep(2);
    }

}