#-*- coding:utf-8 -*-
from core import *

host='192.168.1.204'#服务器ip
root='/uPP_test'#根目录
versionRemote='http://'+host+root+'/version.txt'#服务器上的版本号
RemotePath='http://'+host+root+'/URI.txt'#需下载文件的路径
versionLocal=r'version.txt'#本地版本号
LocalTemp=r'uPPTemp'#本地临时文件夹,程序会自动新建和自动删除
DstDir=r'./'#目的文件夹，拷贝下载下来并解压缩后的文件到这个文件夹
logger=log(r'uPP_Upgrade_Log.txt')#日志文件路径

interval=60#60秒，检查是否有更新


def Upgrade():
    if NeedUpgrade(versionRemote,versionLocal):
        fileurl=getUpgradeFileUrl(RemotePath,versionRemote)
        filename=getUpgradeFileName(RemotePath,versionRemote)
        MkDir(LocalTemp)
        filefullpath=LocalTemp+'/'+filename
        if False==download(fileurl,filefullpath):
            logger.write('[Upgrade fail]: download file fail:'+fileurl)
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
        
        version_local=getVersionFromFile(versionLocal)
        version_remote=getVersionFromServer(versionRemote)
        if False==UpdateVersion(versionLocal,version_remote):
            logger.write('[Upgrade fail]: update local version.txt fail:'+versionLocal)
            RemoveFilesDirs(LocalTemp)
            return
        
        logger.write('[Upgrage successfully]:Version:'+version_local+' => '+version_remote)
        RemoveFilesDirs(LocalTemp)
        
        

def main():
    while True:
        Upgrade()
        time.sleep(interval)

if __name__ == '__main__':
    logger.write('app start')
    main()
    