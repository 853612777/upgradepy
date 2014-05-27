#-*- coding:utf-8 -*-

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
    f=zipfile.ZipFile(src)
    f.extractall(path=dst,pwd=passwd)
    f.close()
    
    
def copyfile(src,dst):
    '''1、目录必须存在,2、会覆盖原先存在的文件'''
    import shutil
    shutil.copy(src,dst)

def getVersionFromServer(url):
    '''version格式:x.x.x.x'''
    import urllib2
    urlObj=None
    try:
        re = urllib2.Request(url)
        urlObj = urllib2.urlopen(re)
        version=urlObj.read()
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

def getUpgradeFile(root,version):
    rt=getStringFromServer(root)
    ver=getStringFromServer(version)
    rt=rt.replace('\n', '')
    ver=ver.replace('\n', '')
    return (rt+'/uPP_testV'+ver+'.zip')


    
    