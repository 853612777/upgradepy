#-*- coding:utf-8 -*-
import os
import time
import shutil
import sys
import subprocess
import socket
import struct
import urllib2
import stat
import re

def readINI(lines):
    result={}
    try:
        for line in lines:
            tmp=line.strip().split('=')
            result[tmp[0].strip()]=tmp[1].strip()
        return result
    except:
        return None

def getString(values,key,default):
    if values==None:
        return default
    try:
        return values[key]
    except:
        return default
    
def getAppPath():
    path=sys.path[0]
    if os.path.isfile(path):
        path,name=os.path.split(path)
    return path

def libsCheck_core(libs):
    '''返回不存在的库名字'''
    libspath=['/usr/local/lib','/usr/lib']
    result=[]
    isexist=False
    for lib in libs:
        for libpath in libspath:
            tmppath=os.path.join(libpath,lib)
            if os.path.exists(tmppath):
                isexist=True
                break
        if isexist:
            isexist=False
        else:
            result.append(lib)
    return result

def libsCheck(config):
    libs=config.libs
    ret=libsCheck_core(libs)
    if []==ret:
        return
    else:
        logger.write('[libs check error]:'+str(ret))

def getlibs(values,key):
    if values==None:
        return []
    try:
        result=values[key]
        if ''==result:
            return []
        tmp=result.split(';')
        ret=[]
        for t in tmp:
            if ''!=t:
                ret.append(t)
        return ret
    except:
        return []
    
def getIPs(values,key):
    if values==None:
        return[]
    try:
        result=values[key]
        if ''==result:
            return []
        tmp=result.split(';')
        ret=[]
        for t in tmp:
            if ''!=t:
                ret.append(t)
        return ret
    except:
        return []

def getURIs(values,key):
    if values==None:
        return[]
    try:
        result=values[key]
        if ''==result:
            return []
        tmp=result.split(';')
        ret=[]
        for t in tmp:
            if ''!=t:
                ret.append(t)
        return ret
    except:
        return []
    
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
    

def URItest(URI):
    urlobj=None
    try:
        req=urllib2.Request(URI)
        urlobj=urllib2.urlopen(req,timeout=2)
        return True
    except:
        return False
    finally:
        if urlobj:
            urlobj.close()


def getURI(URIs):
    if []==URIs:
        return '192.168.5.204'
    for uri in URIs:
        if URItest(uri):
            return uri
    return URIs[0]

def getIP(ips,port):
    if []==ips:
        return '192.168.5.204'
    for ip in ips:
        if telnet(ip,port,1,2):
            return ip
    return ips[0]


class Config():
    def __init__(self,path):
        self.home=getAppPath()
        self.inipath=self.home+'/'+path
    
    def Read(self):
        fp=None
        try:
            fp=open(self.inipath,'r')
            lines=fp.readlines()
            values=readINI(lines)
            self.versionLocal=getString(values,'version','0.0.0.0')
            self.Pid=getString(values,'pid','0')
            self.appname=getString(values,'appname','uServer')
            self.apphome=getString(values,'apphome','/home/server')
            self.exePath=getString(values,'exePath','/home/server/uServer/bin')
            self.URIs=getURIs(values,'URIs')
            self.URI=getURI(self.URIs)
            self.logport=getString(values,'logport','5678')
            self.logips=getIPs(values,'logips')
            self.logip=getIP(self.logips,self.logport)
            self.selfstarting=getString(values,'selfstarting','python /home/server/uServerUpgrade.py')
            self.libs=getlibs(values,'libs')
            return True
        except:
            return False
        finally:
            if fp:
                fp.close()
    
    def Write(self):
        fp=None
        try:
            fp=open(self.inipath,'w')
            fp.write('version = '+self.versionLocal+'\n')
            fp.write('pid = '+self.Pid+'\n')
            fp.write('appname = '+self.appname+'\n')
            fp.write('apphome = '+self.apphome+'\n')
            fp.write('exePath = '+self.exePath+'\n')
            fp.write('URIs = '+';'.join(self.URIs)+'\n')
            fp.write('logips = '+';'.join(self.logips)+'\n')
            fp.write('logport = '+self.logport+'\n')
            fp.write('selfstarting = '+self.selfstarting+'\n')
            fp.write('libs = '+';'.join(self.libs)+'\n')
            return True
        except:
            return False
        finally:
            if fp:
                fp.close()
    
    def UpdateVersion(self,version):
        self.versionLocal=version
    def UpdatePid(self,pid):
        self.Pid=str(pid)

def download(url,filename):
    urlobj=None
    fp=None
    try:
        re = urllib2.Request(url)
        urlobj = urllib2.urlopen(re)
        rs=urlobj.read()
        fp=open(filename, 'wb')
        fp.write(rs)
        return True
    except:
        return False
    finally:
        if urlobj:
            urlobj.close()
        if fp:
            fp.close()
            
def MkDir(path):
    if os.path.exists(path):
        return
    else:
        os.mkdir(path)

def MkDirs(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)
        
def RemoveFilesDirs(path):
    if os.path.exists(path)==False:
        return
    if os.path.isfile(path):
        try:
            os.remove(path)
        except:
            pass
    elif os.path.isdir(path):
        for item in os.listdir(path):
            dst=os.path.join(path,item)
            RemoveFilesDirs(dst)
        try:
            os.rmdir(path)
        except:
            pass
    
def getFileFromServer(url):
    urlobj=None
    try:
        re = urllib2.Request(url)
        urlobj = urllib2.urlopen(re)
        rs=urlobj.read()
        return rs
    except:
        return None
    finally:
        if urlobj:
            urlobj.close()


def unzip(src,dst,passwd=None):
    '''路径不必存在'''
    import zipfile
    try:
        f=zipfile.ZipFile(src)
        f.extractall(path=dst,pwd=passwd)
        f.close()
    except:
        raise Exception('unzip fail')
    

def CopyFiles(src,dst):
    ''''''
    if os.path.exists(src)==False:
        return
    MkDirs(dst)
    for f in os.listdir(src):
        srcfile=src+'/'+f
        if os.path.isfile(srcfile):
            shutil.copy(srcfile,dst+'/'+f)
        elif os.path.isdir(srcfile):
            CopyFiles(srcfile,dst+'/'+f)
            
def getVersionFromServer(url):
    '''version:x.x.x.x'''
    urlObj=None
    try:
        re = urllib2.Request(url)
        urlObj = urllib2.urlopen(re)
        version=urlObj.read()
        version=str(version).replace('\n', '')
        return version
    except:
        return '0.0.0.0'
    finally:
        if urlObj:
            urlObj.close()
            
def getStringFromServer(url):
    urlObj=None
    try:
        re = urllib2.Request(url)
        urlObj = urllib2.urlopen(re)
        content=urlObj.read()
        return content
    except:
        return ''
    finally:
        if urlObj:
            urlObj.close()
    
def getVersionFromFile(path):
    fp=None
    try:
        fp=open(path,'r')
        version=fp.read()
        version=str(version).replace('\n', '')
        return version
    except:
        return '0.0.0.0'
    finally:
        if fp:
            fp.close()

def VersionConvert(version):
    '''将字符串版本变成元组形式'''
    try:
        vers=version.split('.')
        if len(vers)!=4:
            return (0,0,0,0)
        return (int(vers[0]),int(vers[1]),int(vers[2]),int(vers[3]))
    except:
        return (0,0,0,0)

def CompareVersion(ver1,ver2):
    '''ver1>ver2,1;ver1=ver2,0;ver1<ver2,-1'''
    if ver1[0]>ver2[0]:
        return 1
    elif ver1[0]<ver2[0]:
        return -1
    else:
        if ver1[1]>ver2[1]:
            return 1
        elif ver1[1]<ver2[1]:
            return -1
        else:
            if ver1[2]>ver2[2]:
                return 1
            elif ver1[2]<ver2[2]:
                return -1
            else:
                if ver1[3]>ver2[3]:
                    return 1
                elif ver1[3]<ver2[3]:
                    return -1
                else:
                    return 0
 
def getUpgradeFileUrl(uri,appname,version):
    if uri.endswith('/')==False:
        uri+='/'
    return uri+appname+'V'+version+'.zip'

def getUpgradeFileName(appname,version):
    return appname+'V'+version+'.zip'

class Client():
    def __init__(self,config):
        self.logip=config.logip
        self.logips=config.logips
        self.logport=config.logport
    
    def sendstring_core(self,ip,port,content):
        sockfd=None
        content_len=len(content)
        bs=struct.pack('i',content_len)
        try:
            sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
            sockfd.settimeout(2)
            sockfd.connect((ip,int(port)))
            sockfd.send(bs)
            sockfd.send(content)
            return True
        except:
            return False
        finally:
            if sockfd:
                sockfd.close()
    
    def SendString(self,content):
        success=False
        for ip in self.logips:
            if self.sendstring_core(ip,self.logport,content):
                success=True
        if False==success:
            print 'all logSummary Hosts are down'
        

class log():
    def __init__(self,path):
        self.filepath=path
        
    def write(self,content):
        pre=time.strftime(r"[%Y/%m/%d-%H:%M:%S]:",time.localtime())
        content=pre+'['+str(os.getpid())+']:'+content+'\n'
        try:
            fp=open(self.filepath,'a')
            fp.write(content)
            fp.close()
        except:
            pass
        client.SendString(content)


def NeedUpgrade(versionRemote,versionLocal):
    try:
        remote= VersionConvert(versionRemote)
        local= VersionConvert(versionLocal)
        if CompareVersion(remote,local)==1:
            return True
        else:
            return False
    except:
        return False


def WriteRcLocal(content):
    fp=None
    path=r'/etc/rc.local'
    try:
        fp=open(path,'r')
        lines=fp.readlines()
        fp.close()
        
        for line in lines:
            if line.strip()==content:
                return True
        
        fp=open(path,'w')
        pos=len(lines)-1
        lines.insert(pos,content+'\n')
        fp.writelines(lines)
        return True
    except:
        return False
    finally:
        if fp:
            fp.close()
        

def Upgrade(config):
    versionRemotePath=config.URI+'/version.txt'
    versionRemote=getVersionFromServer(versionRemotePath)
    versionLocal=config.versionLocal
    URIRemotePath=config.URI+'/'
    LocalTemp=os.path.join(getAppPath(),time.strftime(r"%Y_%m_%d_%H_%M_%S",time.localtime()))
    appname=config.appname
    apphome=config.apphome
    DstDir=apphome+'/'
    if NeedUpgrade(versionRemote,versionLocal):
        fileurl=getUpgradeFileUrl(URIRemotePath,appname,versionRemote)
        filename=getUpgradeFileName(appname,versionRemote)
        MkDir(LocalTemp)
        filefullpath=LocalTemp+'/'+filename
        if False==download(fileurl,filefullpath):
            logger.write('[Upgrade fail]: download zip file fail:'+fileurl)
            RemoveFilesDirs(LocalTemp)
            return
        
        try:
            unzip(filefullpath,LocalTemp)
        except:
            logger.write('[Upgrade fail]: unzip file fail:'+filefullpath)
            RemoveFilesDirs(LocalTemp)
            return
        
        RemoveFilesDirs(filefullpath)
        
        if False==KillServer(config):
            logger.write('[KillServer fail]:can not kill pid:'+config.Pid)
        
        try:
            CopyFiles(LocalTemp,DstDir)#after killserver or error:Text file busy
        except:
            logger.write('[CopyFiles fail]:can not copy files to dst:'+DstDir)
            RemoveFilesDirs(LocalTemp)
            return
        
        if False==StartServer(config):
            logger.write('[StartServer fail]: can not start server: '+config.appname)
            RemoveFilesDirs(LocalTemp)
            return
        
        config.UpdateVersion(versionRemote)
        config.Write()
        
        logger.write('[restart Server successfully]:PID:'+config.Pid)
        logger.write('[Upgrage successfully]:Version:'+versionLocal+' => '+versionRemote)
        RemoveFilesDirs(LocalTemp)
        

def mainLoop():
    while True:
        Upgrade(config)
        time.sleep(60)
    
    
def getPIDs(keyword):
    '''根据关键字得到PID'''
    cmd="ps ax|grep -w "+keyword+" |grep -v python|grep -v grep |awk '{print $1}'"
    result=[]
    try:
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        pids=proc.stdout.readlines()
        for pid in pids:
            result.append(int(pid.strip()))
        return result
    except:
        return []
    

def chmod(path):
    exts=set(['.cpp','.log','.h','.hpp','.c','.txt','.xml','.sql'])
    if os.path.exists(path)==False:
        return
    if os.path.isfile(path):
        fi,ext=os.path.splitext(path)
        if ext in exts:
            return
        else:   
            os.chmod(path, stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
            return
    if os.path.isdir(path):
        basepath=path
        for f in os.listdir(path):
            path=os.path.join(basepath,f)
            chmod(path)

    
def StartServer(config):
    exefile=config.exePath+'/'+config.appname
    if os.path.exists(exefile)==False:
        return False
    
    chmod(config.apphome)
    
    cmd='cd '+config.exePath+'&&./'+config.appname
    keyword=config.appname
    try:
        subprocess.Popen(cmd,stderr=subprocess.STDOUT,shell=True)
        time.sleep(2)
        pids=getPIDs(keyword)
        if []==pids:
            config.UpdatePid(0)
            return False
        else:
            if pids[0]==config.Pid:
                logger.write('[StartServer error]:has not been killed before')
                return False
            config.UpdatePid(pids[0])
            config.Write()
            return True
    except:
        config.UpdatePid(0)
        return False
    
def KillServer(config):
    try:
        keyword=config.appname
        pids=getPIDs(keyword)
        if []!=pids:
            for pid in pids:
                os.kill(pid, 9)
            config.UpdatePid(0)
        return True
    except:
        return False
    

def selfStarting(config):
    if config.versionLocal=='0.0.0.0' and config.Pid=='0':
        if WriteRcLocal(config.selfstarting)==False:
            logger.write('write self-starting error')
            sys.exit(2)
    
def getHostIPs():
    '''获取主机IP，可能有两个'''
    cmd='ifconfig'
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    content=proc.communicate()[0]
    result=[]
    pattern=re.compile('192\.168\.\d+\.\d+')
    matchs=re.findall(pattern,content)
    for m in matchs:
        digit=m.split('.')
        if digit[2]!='2' and digit[3]!='1' and digit[3]!='255':
            result.append(m)
    return result



if __name__ == '__main__':
    config=Config('Config.ini')
    if False==config.Read():
        print 'read ini error'
        sys.exit(1)
    client=Client(config)
    logger=log(getAppPath()+'/logUpgrade.log')
    logger.write('python Upgrade.py start')
    selfStarting(config)#自启动
    print 'selfStarting done...'
    libsCheck(config)#检查依赖库
    print 'libsCheck done...'
    KillServer(config)
    bstart=StartServer(config)
    print 'StartServer done...'
    if bstart:
        logger.write('[StartServer successfully]:appname:'+config.appname+',PID:'+config.Pid)
    try:
        mainLoop()
        logger.write('[Upgrade.py error]:'+__file__+' has exited')
    except KeyboardInterrupt:
        print 'Ctrl^C'
    