
#-*- coding:utf-8 -*-
#vers=0.0.0.1


import urllib2
import re
from collections import defaultdict
import socket
import struct

def getMountItem(line):
    '''type,dstIP,dstPath,srcIP,srcPath'''
    try:
        item=['','','','','']
        pattern=re.compile('\[([^\[\]]+?)\]')
        ms=re.findall(pattern,line)
        item[0]=ms[0]
        tmp=ms[1].split(':')
        item[1]=tmp[0]
        item[2]=tmp[1]
        tmp=ms[2].split(':')
        item[3]=tmp[0]
        item[4]=tmp[1]
        return item
    except:
        return ['','','','','']

def getMountlistFromApache(uri):
    urlobj=None
    result=[]
    try:
        req=urllib2.Request(uri)
        urlobj=urllib2.urlopen(req)
        lines=urlobj.read()
        lines=lines.strip().split('\n')
        for line in lines:
            line=line.strip()
            if ''!=line and line.startswith('#')==False:
                item=getMountItem(line)
                if ['','','','','']!=item:
                    result.append(item)
        return result
    except:
        return []
    finally:
        if urlobj:
            urlobj.close()

class MountChecker():
    def __init__(self,uri):
        self.uri='http://{0}/uServer/mountlist.txt'.format(uri)
        self.mountlist=getMountlistFromApache(self.uri)
        self.Hostmap=defaultdict(list)
        
    def getHostMountMap(self):
        '''获取IP与对应的挂载'''
        for item in self.mountlist:
            self.Hostmap[item[1]].append(item)
        return self.Hostmap
    
    def Connect(self,IP):
        try:
            sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sockfd.settimeout(2)
            sockfd.connect((IP,6789))
            return sockfd
        except:
            try:
                sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sockfd.settimeout(2)
                sockfd.connect((IP,6788))
                return sockfd
            except:
                return None
    
    def getHaveMounted(self,IP):
        '''获取已经挂载的情况'''
        sockfd=None
        try:
            sockfd=self.Connect(IP)
            if None==sockfd:
                return []
            sockfd.send('1234567890')
            bs=sockfd.recv(4)
            length,=struct.unpack('i',bs)
            text=sockfd.recv(int(length))
            result=[i for i in text.split('\n') if ''!=i]
            return result
        except:
            return []
        finally:
            if sockfd:
                sockfd.close()
                
    def PrintMountStatus(self):
        hosts=self.getHostMountMap()
        for ip in hosts.keys():
            mounted=self.getHaveMounted(ip)
            for need in hosts[ip]:
                if str(need) in mounted:
                    print 'Mounted [{0}][{1}:{2}][{3}:{4}]'.format(need[0],need[1],need[2],need[3],need[4])
                else:
                    print 'Not Mounted [{0}][{1}:{2}][{3}:{4}]'.format(need[0],need[1],need[2],need[3],need[4])
    
    
    
if __name__=='__main__':   
    mountChecker=MountChecker('192.168.1.204')    
    mountChecker.PrintMountStatus()

    
    