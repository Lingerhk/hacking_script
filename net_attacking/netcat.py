# -*- coding:utf-8 -*-

# a simple util netcat tools.
# by s0nnet
#

import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_dest = ""
port = 0

def usage():
    print "Usage: ./mynetcat.py -t target -p port"
    print "-l --listen                -listen on [host]:[port] wair for incoming connections"
    print "-e --execute=file_to_run   -execute the given file upon receiving a connections"
    print "-c --command               -initialize a command shell"
    print "-u --upload=destination    -upon receiving connections upload a file and write to [destination]"
    
    print 
    print "Examples:"
    print "  ./netcat.py -t 10.0.0.2 -p 666 -l -c"
    print "  ./netcat.py -t 10.0.0.2 -p 666 -l -u a.txt"
    print "  ./netcat.py -t 10.0.0.2 -p 666 -l -e cat\\/etc/passwd"
    print "  echo 'heheda' | ./mynetcat.py -t 10.0.0.2 -p 666"
    sys.exit(0)

def run_command(command):
    command = command.rstrip()
    try:
        output  = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = "Failed to execute command.\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_dest):
        # read in all of the bytes and write to our destination
        file_buffer  = ""

        # keep reading data until none is available

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data

        # now we take these bytes and try to write them out
        try:
            file_desc = open(upload_dest,"wb")
            file_desc.write(file_buffer)
            file_desc.close()

            # acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s\r\n" % upload_dest)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_dest)

    # check for command execution
    if len(execute):
        # run the command
        output = run_command(execute)
        
        client_socket.send(output)

    # now we go into another loop if a command shell was requested
    if command:
        while True:
            # show a simple prompt
            client_socket.send("CMD:#> ")
            # now we receive until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # send back the command output
            response = run_command(cmd_buffer)

            # send back the response
            client_socket.send(response)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)
        
        while True:

            # now wait for data back
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response = data

                if recv_len < 4096:
                    break

            print response,

            # wait for more input
            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)

    except:
        print "[*] Exception! Exiting"
        client.close()

def server_loop():
    global target

    # listen all interfaces if no target is defined
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def main():
    global listen
    global port
    global execute
    global command
    global upload_dest
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for opt,arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-l", "--listen"):
            listen = True
        elif opt in ("-e", "--execute"):
            execute = arg
        elif opt in ("-c", "--command"):
            command = True
        elif opt in ("-u", "--upload"):
            upload_dest = arg
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        else:
            assert False, "unhandled Option"
    
    # connection remote server
    #if not listen and len(target)

    # read the buffer from the commandline
    if not listen and len(target) and port > 0:
        # send CTRL-D in order not be block
        buffer = sys.stdin.read()
        client_sender(buffer)

    # upload things, execute commands,and drop a shell back
    if listen:
        server_loop()

if __name__ == "__main__":
    main()
