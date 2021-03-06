#-*- coding:utf-8 -*-

import socket
import threading
import struct
import sys
import Queue
import os

def getAppPath():
    path=sys.path[0]
    if os.path.isfile(path):
        path,name=os.path.split(path)
    return path

class log(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.filepath=os.path.join(getAppPath(),path)
        self.fp=open(self.filepath,'a')
        
    def run(self):
        global logqueue
        while True:
            content=logqueue.get()
            self.fp.write(content)
            self.fp.flush()
            print content
        self.fp.close()
        print 'log exit'
        sys.exit(2)

class Worker(threading.Thread):
    def __init__(self,arg):
        threading.Thread.__init__(self)
        self.client=arg[0]
        self.ipaddr=arg[1]
        
    def run(self):
        global logqueue
        try:
            self.client.settimeout(3)
            bs=self.client.recv(4)
            content_len,=struct.unpack('i',bs)
            content=self.client.recv(int(content_len))
            content='['+str(self.ipaddr[0])+']:'+content
            logqueue.put(content)
        except:
            return
        finally:
            self.client.close()
            
            
class Server():
    def __init__(self):
        self.ip=''
        self.port=5678
        self.sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    
    def Accept(self):
        self.sockfd.bind((self.ip,self.port))
        self.sockfd.listen(128)
        while True:
            (client,ipaddr)=self.sockfd.accept()
            worker=Worker((client,ipaddr))
            worker.start()
        self.sockfd.close()
        print 'server exit'
        sys.exit(1)
            
            
            
            
            
logqueue=Queue.Queue()      
def main():
    logger=log('logSummary.log')
    logger.setDaemon(True)
    logger.start()
    server=Server()
    server.Accept()
            
if __name__=='__main__':
    main()
            