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
                      // 9999 is arbitrary unused port
        0
    };

    // bind the socket to an address to listen on:
    bind(
        socketFileDescriptor,
        (const struct sockaddr *)&addr,
        sizeof(addr)
    );

    // prepare the socket for listening:
    listen(
        socketFileDescriptor,
        10  // maximum length that the queue of pending connections can grow to
    );

    // accept connections from the client:
    int clientFileDescriptor = accept(
        socketFileDescriptor,
        NULL,  // no need to restrict 
        NULL
    );

    // setup server to wait on events from file streams:
    struct pollfd pollFileDescriptorArray[2] =  {
        {
            0,  // listen on stdin, so the server can send to clients
            POLLIN,  // event where there is data to read
            0
        },
        {
            clientFileDescriptor,  // listen from the client
            POLLIN,  // event where there is data to read
            0
        }
    };
    
    // char buffer[256];  // not freeing and re-allocating the buffer occasionally causes buffer not to be cleared properly and parts of previously sent messages to be printed again
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
            send(clientFileDescriptor, buffer, 255, 0);

            free(buffer);
            buffer = calloc(256, sizeof(char));
            
        } else if (pollFileDescriptorArray[1].revents & POLLIN) {  // client has sent something to the server

            if (recv(clientFileDescriptor, buffer, 255, 0) == 0) {  // if nothing is recieved (i.e., if the client is terminated), end program
                return 0;
            }
            printf("Client: %s", buffer);
            fflush(stdout);

            free(buffer);
            buffer = calloc(256, sizeof(char));
        }
    }

    return 0;
}