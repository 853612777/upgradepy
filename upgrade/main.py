from core import *
import time

host='192.168.1.204'
root='uPP_test'


def main():
    while True:
        
        time.sleep(60)
        

if __name__ == '__main__':
    # download(r'http://bbs.southbaytech.co/uc_server/avatar.php?uid=10&size=small',r'C:\Users\Sven\Desktop\down.png')
#     unzip(r'C:\Users\Sven\Desktop\test.zip',r'C:\Users\Sven\Desktop\test\t')
#     copyfile(r'C:\Users\Sven\Desktop\mainapp.py',r'C:\Users\Sven\Desktop\test\m.7z')
    if NeedUpgrade('http://192.168.1.204/uPP_test/version.txt',r'C:\Users\Sven\Desktop\version.txt'):
        fileurl= getUpgradeFile('http://192.168.1.204/uPP_test/URI.txt','http://192.168.1.204/uPP_test/version.txt')
        download(fileurl,r'C:\Users\Sven\Desktop\ddddd.zip')
    else:
        print 'not need'