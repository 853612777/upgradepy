#-*- coding:utf-8 -*-

def getStrings(path):
    fp=None
    lines=None
    try:
        fp=open(path,'r')
        lines=fp.readlines()
        return lines
    except:
        return None
    finally:
        if fp:
            fp.close()
            
            

def checkError(lines):
    global keywords
    for line in lines:
        for keyword in keywords:
            if line.find(keyword)!=-1:
                print line.strip()
                break
            
keywords=['fail','error']          
def main():
    lines=getStrings('logSummary.log')
    checkError(lines)      
  
if __name__=='__main__':
    main()