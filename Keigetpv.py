#omron rs232c 
import serial
import time
import struct
# from operator import xor
import chksumKei
import setSerKei
import am

def getPv2000():
    
    ser=setSerKei.setSerKei2000()
    ser.open()

    #for command
    y=":FETCh?"
    x=y.encode()
    ser.write(x)
    
    x=b'\r'
    ser.write(x)
    
    #to receive data
    #print("recv data")
    pv=0
    c=""
    camma=0
    i=0
    while True:
        if ser.in_waiting > 0:
            recv_data=ser.read()
            a = struct.unpack_from("B",recv_data, 0)
            b=a[0]
            b=chr(b)
            #print(b)
            c+=b
            if len(c) == 15:
                #print(c)
                break
            
#             if i == 16:
#                 c=b
# 
#             if b =="\x03":
#                 pv=int(c,16)
#                 pv=round(pv*.1+273.2,1)
#                 am.amb(pv)
#                 break
#             if i > 16:
#                 c+=b
#             i += 1
    ser.close()
    #print("return")
    return c

def getPv2182A():
    
    ser=setSerKei.setSerKei2182A()
    ser.open()

    #for command
    y=":FETCh?"
    x=y.encode()
    ser.write(x)
    
    x=b'\r'
    ser.write(x)
    
    #to receive data
    #print("recv data")
    pv=0
    c=""
    camma=0
    i=0
    while True:
        if ser.in_waiting > 0:
            recv_data=ser.read()
            a = struct.unpack_from("B",recv_data, 0)
            b=a[0]
            b=chr(b)
            #print(b)
            c+=b
            if len(c) == 15:
                print(c)
                break
            
#             if i == 16:
#                 c=b
# 
#             if b =="\x03":
#                 pv=int(c,16)
#                 pv=round(pv*.1+273.2,1)
#                 am.amb(pv)
#                 break
#             if i > 16:
#                 c+=b
#             i += 1
    ser.close()
    #print("return")
    return c

# while True:
#     getPv2000()
#     getPv2182A()
#     time.sleep(1)
    

    