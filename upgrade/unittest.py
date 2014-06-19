#-*- coding:utf-8 -*-


import subprocess
import re

def ReadMountFile(path):
    fp=None
    result=[]
    try:
        fp=open(path,'r')
        lines=fp.readlines();
        for line in lines:
            line=line.strip()
            if ''!=line and line.startswith('#')==False:
                result.append(line)
        return result
    except:
        return []
    finally:
        if fp:
            fp.close()
            
def getAlreadyMount():
    '''获取已经挂载的目录'''
    cmd='mount -l'
    proc=subprocess.Popen(cmd,shell=True)
    content=proc.communicate()[0]
    result=[]
    pattern=re.compile('192\.168\.\d+\.\d+')
    matchs=re.findall(pattern,content)
    for m in matchs:
        digit=m.split('.')
        if digit[2]!='2' and digit[3]!='1' and digit[3]!='255':
            print m
            result.append(m)
    return result
    
def getAlreadyMount(IP):
    result=[]
    pattern=re.compile('(192\.168\.\d+\.\d+)(.*) on (.*) type (.*) \(.*\)')
    for line in content.strip().split('\n'):
        m=re.search(pattern,line)
        if m:
            mountline=''
            if m.group(4)=='cifs':
                mountline+='[smb][{0}:{1}][{2}:{3}]'.format(IP,m.group(3),m.group(1),m.group(2))
            else:
                mountline+='[nfs][{0}:{1}][{2}{3}]'.format(IP,m.group(3),m.group(1),m.group(2))
            result.append(mountline)
    return result    


if __name__=='__main__':
    for a in ReadMountFile(r'c:\users\sven\desktop\mount.txt'):
        print a