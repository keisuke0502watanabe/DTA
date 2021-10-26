#check sum for omron
from operator import xor

def chksum(y):
    #check sum calculation before ETX
    i=0
    list=[]
    chkSum=0
    for i in range(len(y)):
        list.append(ord(y[i]))
    i=0
    chkSum=list[0]
    for i in range(len(list)-1):
        chkSum=xor(chkSum, list[i+1])
    
        #check sum calculation after ETX
    chkSum=xor(chkSum,3)
    chkSumValue=str.upper(str(chkSum))
    chkSumValue=chr(int(chkSumValue)).encode()
    
    return chkSumValue