#-*- coding:utf-8 -*-

import socket
import threading
import struct
import sys
import Queue

class log(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.filepath=sys.path[0]+'/'+path
        self.fp=open(self.filepath,'a')
        
    def run(self):
        global logqueue
        while True:
            content=logqueue.get()
            self.fp.write(content)
            self.fp.flush()
            
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
        bs=self.client.recv(4)
        content_len,=struct.unpack('i',bs)
        content=self.client.recv(int(content_len))
        content='['+str(self.ipaddr)+']:'+content
        logqueue.put(content)

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
            