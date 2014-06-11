#-*- coding:utf-8 -*-

import socket

def telnet_core(host,port,timeout):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host,int(port)))
        return True
    except:
        return False
    finally:
        sock.close()

def telnet(host,port,timeout,times):
    for x in range(0,times):
        result=telnet_core(host,port,timeout)
        if result==True:
            return True
    return False    

def main():
    global services
    for service in services:
        host,port,serviceName=service.split(':')
        if telnet(host,port,1000,2):
            print service+' is up'
        else:
            print service+' is down'






services=['192.168.1.204:8003:uServer']

if __name__=='__main__':
    main()