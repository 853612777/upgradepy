#-*- coding:utf-8 -*-

import socket
import os
import sys

def getAppPath():
    path=sys.path[0]
    if os.path.isfile(path):
        path,name=os.path.split(path)
    return path
    

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

def getServices():
    path=os.path.join(getAppPath(),'Services.ini')
    fp=None
    result=[]
    try:
        fp=open(path,'r')
        lines=fp.readlines()
        for line in lines:
            result.append(line.strip())
        return result
    except:
        return []
    finally:
        if fp:
            fp.close()

def main():
    services=getServices()
    for service in services:
        host,port,serviceName=service.split(':')
        if telnet(host,port,1000,2):
            print service+' is up'
        else:
            print service+' is down'



if __name__=='__main__':
    main()