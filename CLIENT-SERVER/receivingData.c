#include <stdio.h>
#include <string.h>
#include <sys/socket.h> //content host
#include <arpa/inet.h>

int main(int argc, char** argv){

    char *host_name = "www.google.com.br";
    char ip[100];

    struct hostent *machigne;
    struct in_addr **addr_list;

    int i; //loop
    /*to conect a remopte host is necessary has the ip address. The ghostbyname function is usually
    to this point. The get a domain name like a paramether and return the struct of hostent type.
    
    This struct have a ip information. The library is the netdb.h*/

    if(((machigne = ghostbyname(host_name)) == NULL)){

        //the gethost is failed.
        herror("ghostbyname");
        return 1;
    }

    /*now we give a h_addr_list cast to in_addr, one time whop h_addr_list have the ip address too, but only on long type*/

    addr_list = (struct in_addr **) machigne->h_addr_list;

    for(i = 0; addr_list[i] != NULL; i++){

        strcpy(ip, inet_ntoa(*addr_list[i]));
    }

    printf("have the ip address: %s\n", host_name, ip);
    return 0;
}