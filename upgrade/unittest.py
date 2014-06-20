#-*- coding:utf-8 -*-


import subprocess
import re

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
            
  



if __name__=='__main__':
    for a in ReadMountFile(r'c:\users\sven\desktop\mount.txt'):
        print a