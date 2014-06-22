#-*- coding:utf-8 -*-
#vers=0.0.0.1
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
import threading

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

def getCMDReturn(cmd):
    try:
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        ret=proc.communicate()[0]
        lines=ret.strip().split('\n')
        result=[]
        for line in lines:
            result.append(line.strip())
        return result
    except:
        return []    
    
    
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
    

def ReadMountFile(path):
    fp=None
    result=[]
    try:
        fp=open(path,'r')
        lines=fp.readlines();
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
        if fp:
            fp.close()
            

    
def getAlreadyMount(IP):
    rets=getCMDReturn('mount -l')
    result=[]
    pattern=re.compile('(192\.168\.\d+\.\d+):{0,1}(.*) on (.*) type (.*) \(.*\)')
    for line in rets:
        m=re.search(pattern,line)
        if m:
            if m.group(4)=='cifs':
                result.append(['smb',IP,m.group(3),m.group(1),m.group(2)])
            else:
                result.append(['nfs',IP,m.group(3),m.group(1),m.group(2)])
    return result


def pingSuccess(IP):
    rets=getCMDReturn('ping {0} -c 2'.format(IP))
    for r in rets:
        if 'received' in r:
            m=re.search('(\d) received',r)
            if m:
                count=m.group(1)
                try:
                    if int(count)>=1:
                        return True
                except:
                    return False
    return False


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


def getHostIP():
    IPs=getHostIPs()
    if len(IPs)==0:
        return ''
    if len(IPs)==1:
        return IPs[0]
    try:
        for ip in IPs:
            tmp=ip.split('.')
            tmp[3]='1'
            newip='.'.join(tmp)
            success=pingSuccess(newip)
            if success:
                return ip
        return ''
    except:
        return ''


def getMountStatement(item,user,passwd):
    if len(item)!=5:
        return ''
    result=''
    if 'smb'==item[0]:
        result='mount -t cifs -o username={0},password={1},iocharset=utf8 //{2}{3} {4}'.format(user,passwd,item[3],item[4],item[2])
    elif 'nfs'==item[0]:
        result='mount -t nfs {0}:{1} {2}'.format(item[3],item[4],item[2])
    else:
        return ''
    return result


def getTotalMountItems(ip,items):
    if ''==ip:
        return []
    Need=[]
    for item in items:
        if ip in item[1]:
            Need.append(item)
    return Need

def getLeftNeedMount(Total,Already):
    Left=[]
    for item in Total:
        if item not in Already:
            Left.append(item)
    return Left


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


class Mounter(threading.Thread):
    def __init__(self,uri,user,passwd):
        super(Mounter,self).__init__()
        self.hostIP=getHostIP()
        self.mountlistUri=uri
        self.mountlistString=''
        self.user=user
        self.passwd=passwd
        self.MountFails=[]
    
    def checkMountlist(self):
        mountlist=getMountlistFromApache(self.mountlistUri)
        if self.mountlistString == mountlist:
            return False
        else:
            return True
            
    def executeMount(self,item):
        if pingSuccess(item[3])==False:
            return False
        else:
            cmd=getMountStatement(item,self.user,self.passwd)
            if ''==cmd:
                return True
            proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            ret=proc.communicate()[0]
            if None!=ret and ('timed out' in ret or 'mount error' in ret or 'Unable' in ret):
                print cmd
                return False
            return True
            
    def toMountLeft(self):
        Total= getTotalMountItems(self.hostIP,self.mountlistString)
        Already=getAlreadyMount(self.hostIP)
        Left=getLeftNeedMount(Total,Already)
        for item in Left:
            if self.executeMount(item)==False:
                if item not in self.MountFails:
                    self.MountFails.append(item)
    
    def toMountFails(self):
        fails=self.MountFails
        self.MountFails=[]
        for failitem in fails:
            if self.executeMount(failitem)==False:
                self.MountFails.append(failitem)
            
        
    def run(self):
        self.mountlistString=getMountlistFromApache(self.mountlistUri)
        self.toMountLeft()
        while True:
            time.sleep(30)
            if self.checkMountlist()==False:
                self.toMountLeft()
            self.toMountFails()




class MountQuery(threading.Thread):
    def __init__(self,mounter):
        super(MountQuery,self).__init__()
        self.mounter=mounter
        
    def Bind(self):
        sockfd=None
        try:
            sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sockfd.bind(('',6789))
            return sockfd
        except socket.error:
            if sockfd:
                sockfd.close()
            try:
                sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sockfd.bind(('',6788))
                return sockfd
            except:
                return None
                
    def verify(self,client):
        try:
            client.settimeout(3)
            text=client.recv(10)
            if '1234567890'==text:
                return True
            else:
                return False
        except:
            return False
            
    def SendString(self,client,info):
        info=str(info)
        length=len(info)
        bs=struct.pack('i',length)
        try:
            client.send(bs)
            client.send(info)
        except:
            pass
        
    def run(self):
        sockfd=self.Bind()
        if None==sockfd:
            return
        sockfd.listen(16)
        while True:
            connection,address=sockfd.accept()
            if self.verify(connection):
                info=getAlreadyMount(self.mounter.hostIP)
                self.SendString(connection,info)
            else:
                pass
            connection.close()
        sockfd.close()
    




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
    