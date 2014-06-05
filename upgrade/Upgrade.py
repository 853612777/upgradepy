#-*- coding:utf-8 -*-
import os
import time
import shutil
import sys
import subprocess

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
    
class Config():
    def __init__(self,path):
        self.inipath=path
        self.home=sys.path[0]
    
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
            self.URI=getString(values,'URI','http://192.168.1.204/')
            self.logip=getString(values,'logip','192.168.1.204')
            self.selfstarting=getString(values,'selfstarting','python /home/server/uServerUpgrade.py')
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
            fp.write('URI = '+self.URI+'\n')
            fp.write('logip = '+self.logip+'\n')
            fp.write('selfstarting = '+self.selfstarting+'\n')
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
    import urllib2
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
    import urllib2
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
    '''Ŀ¼������Ҳû��ϵ'''
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
    import urllib2
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
    import urllib2
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

class log():
    def __init__(self,path):
        self.filepath=path
        
    def write(self,content):
        pre=time.strftime(r"[%Y/%m/%d-%H:%M:%S]:",time.localtime())
        try:
            fp=open(self.filepath,'a')
            fp.write(pre+content+'\n')
            fp.close()
        except:
            pass


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
    LocalTemp=time.strftime(r"%Y_%m_%d_%H_%M_%S",time.localtime())
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
        
        CopyFiles(LocalTemp,DstDir)
        
        if False==KillServer(config):
            logger.write('[KillServer fail]:can not kill pid:'+config.Pid)
        
        if False==StartServer(config):
            logger.write('[StartServer fail]: can not start server'+config.appname)
        
        config.UpdateVersion(versionRemote)
        config.UpdatePid()
        config.Write()
        
        logger.write('[Upgrage successfully]:Version:'+versionLocal+' => '+versionRemote)
        RemoveFilesDirs(LocalTemp)
        

def mainLoop():
    while True:
        Upgrade()
        time.sleep(60)
    
    
def getPID(keyword):
    '''根据关键字得到PID'''
    cmd="ps ax|grep "+keyword+" |grep -v grep |awk '{print $1}'"
    try:
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        pid=proc.stdout.read()
        return int(pid.strip())
    except:
        return -1
    
def StartServer(config):
    cmd=config.apphome+'/'+config.appname
    keyword=cmd
    try:
        subprocess.Popen(cmd,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT,shell=True)
        time.sleep(2)
        pid=getPID(keyword)
        if -1==pid:
            config.UpdatePid(0)
            return False
        else:
            config.UpdatePid(pid)
            return True
    except:
        config.UpdatePid(0)
        return False
    
def KillServer(config):
    pid=config.Pid
    keyword=config.apphome+'/'+config.appname
    another=getPID(keyword)
    if -1==another:
        logger.write('[pid error]:can not find pid by keyword')
    if pid!=another:
        logger.write('[pid error]:config pid not eq getPID() pid')
    if 0!=pid:
        os.kill(pid, 9)
        config.UpdatePid(0)
    if 0==pid and -1!=another:
        os.kill(another, 9)
        config.UpdatePid(0)
    return True
    

def selfStarting(config):
    if config.versionLocal=='0.0.0.0' and config.Pid=='0':
        if WriteRcLocal(config.selfstarting)==False:
            logger.write('write self-starting error')
            sys.exit(2)
    

if __name__ == '__main__':
    logger=log(time.strftime(r"%Y_%m_%d_%H_%M_%S",time.localtime())+'.log')
    logger.write('python app start')
    config=Config('Config.ini')
    if False==config.Read():
        logger.write('read ini error')
        sys.exit(1)
    selfStarting(config)
    KillServer(config)
    StartServer(config)
    mainLoop()
    