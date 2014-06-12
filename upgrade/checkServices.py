#-*- coding:utf-8 -*-

import socket
import os
import sys
import ctypes

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

def set_color(color, handle=ctypes.windll.kernel32.GetStdHandle(-11)):
    return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)

def main():
    services=getServices()
    for service in services:
        host,port,serviceName=service.split(':')
        if telnet(host,port,1000,2):
            set_color(0x0A)
            print service+' is up'
        else:
            set_color(0x7C)
            print service+' is down'
    set_color(0x0F)



if __name__=='__main__':
    main()
    os.system('pause')