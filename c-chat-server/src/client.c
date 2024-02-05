#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <poll.h>
#include <unistd.h>


int main(int argc, char* argv[]) {
    
    // Create the socket:
    int socketFileDescriptor = socket(
        AF_INET,  // using the IPv4 address family
        SOCK_STREAM,  //  Sequenced, reliable, connection-based byte streams - from socket_type.h
        0  // use default protocol
    );

    // Create a struct to describe the IPv4 socket address:
    struct sockaddr_in addr = {
        AF_INET,
        htons(9999),  // htons converts between host and network byte order (i.e., converts little endian to big endian)
                      // 9999 is arbitrary unused port, must be same as server
        0
    };

    connect(
        socketFileDescriptor, 
        (const struct sockaddr *)&addr, 
        sizeof(addr)
    );


    struct pollfd pollFileDescriptorArray[2] =  {
        {
            0,  // listen on stdin, so the client can send to server
            POLLIN,  // event where there is data to read
            0
        },
        {
            socketFileDescriptor,  // listen from the server
            POLLIN,  // event where there is data to read
            0
        }
    };
    
    // char buffer[256] = {'\0'};
    char *buffer = calloc(256, sizeof(char));
    while (1) {
        poll(
            pollFileDescriptorArray,
            2,
            10000 // wait 10,000 milliseconds to time out
        );
        if (pollFileDescriptorArray[0].revents & POLLIN) {  // for the server to send to the client
            // if the first file descriptor (stdin) is ready, read from stdin:
            read(0, buffer, 255);
            // send to client:
            send(socketFileDescriptor, buffer, 255, 0);

            free(buffer);
            buffer = calloc(256, sizeof(char));
        } else if (pollFileDescriptorArray[1].revents & POLLIN) {  // client has sent something to the server

            if (recv(socketFileDescriptor, buffer, 255, 0) == 0) {  // if nothing is recieved (i.e., if the server is terminated), end program
                return 0;
            }
            printf("Server: %s", buffer);
            fflush(stdout);
            // for (int i = 0; i < 256; i++) buffer[i] = (char)0;

            free(buffer);
            buffer = calloc(256, sizeof(char));
        }
        
        
    }

    return 0;
}