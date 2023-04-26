#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h> //strlen
#include <unistd.h> //write function


int main(int argc, char** argv){

    int my_socket, new_socket, c;
    struct sockaddr_in, servidor, cliente;

    //create a socket
    my_socket = socket(AF_INET, SOCK_STREAM, 0);

    if(my_socket == -1){
        printf("Socket is failed.");
    }

    //preparing the SOCKADDR_IN STRUCT
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(8888);

    //bind - turning on the socket conection to a door
    if(bind(my_socket,(struct sockaddr *)&server, sizeof(server)) < 0){
        puts("bind error");

    }else{

        puts("bind on");
    }

    //Listen - listen the conections
    listen(my_socket, 3);

    //accept the conections
    puts("Waiting the conections arrive...");

    c = sizeof(struct sockaddr_in);
    my_socket = accept(my_socket, (struct sockaddr *)&cliente, (socklen_t*)&c);

    if(my_socket < 0){
        perror("Error to accepted the conection");
    }else{
        puts("accepted concection");
        return 0;
    }

    message = "message received";
    write(new_socket, message, strlen(message));
    return 0;
       
}