#-*- coding:utf-8 -*-
import os
import time
import shutil

def getINI(lines):
    try:
        for line in lines:
            line=line.strip().
    

class Config():
    def __init__(self,path):
        self.path=path
    
    def Read(self):
        fp=None
        try:
            fp=open(self.path,'r')
            lines=fp.readlines()
            self.versionLocal=lines[0]
            self.Pid=lines[1]
            self.versionLocal=lines[2]
            return True
        except:
            return False
        finally:
            if fp:
                fp.close()
    
    def Write(self):
        fp=None
        try:
            fp=open(self.path,'w')
            lines=fp.readlines()
            self.versionLocal=lines[0]
            self.Pid=lines[1]
            self.versionLocal=lines[2]
            return True
        except:
            return False
        finally:
            if fp:
                fp.close()
    

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
    '''目录不存在也没关系'''
    import zipfile
    try:
        f=zipfile.ZipFile(src)
        f.extractall(path=dst,pwd=passwd)
        f.close()
    except:
        raise Exception('unzip fail')
    
    
def copyfile(src,dst):
    '''1、目录必须存在,2、会覆盖原先存在的文件'''
    shutil.copy(src,dst)

def CopyFiles(src,dst):
    '''src:目录,dst:目录'''
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
    '''version格式:x.x.x.x'''
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
    '''将字符串版本转换为元组'''
    try:
        vers=version.split('.')
        if len(vers)!=4:
            return (0,0,0,0)
        return (int(vers[0]),int(vers[1]),int(vers[2]),int(vers[3]))
    except:
        return (0,0,0,0)

def CompareVersion(ver1,ver2):
    '''ver1大于ver2返回1;等于0,小于-1'''
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


def NeedUpgrade(remoteUrl,localPath):
    try:
        remote= VersionConvert(getVersionFromServer(remoteUrl))
        local= VersionConvert(getVersionFromFile(localPath))
        if CompareVersion(remote,local)==1:
            return True
        else:
            return False
    except:
        return False
    
def getUpgradeFileUrl(root,version):
    rt=getStringFromServer(root)
    rt=rt.replace('\n', '')
    filename=getUpgradeFileName(root,version)
    return rt+'/'+filename

def getUpgradeFileName(root,version):
    ver=getStringFromServer(version)
    ver=ver.replace('\n', '')
    return 'uPP_testV'+ver+'.zip'

def UpdateVersion(path,version):
    fp=None
    try:
        fp=open(path,'w')
        fp.write(version)
        return True
    except:
        return False
    finally:
        if fp:
            fp.close()


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

    
    