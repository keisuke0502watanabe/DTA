#omron rs232c 
import serial
import time
import struct
# from operator import xor
import chksumKei
import setSerKei

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
            c+=b
            if len(c) == 15:
                break

    ser.close()

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
            c+=b
            if len(c) == 15:
                break
    ser.close()
    return c

def getPv2000pressure():
    
    ser=setSerKei.setSerKei2000forPressure()
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
            c+=b
            if len(c) == 15:
                break

    ser.close()

    return c

'''
def send_command(command):
    ser=setSerKei.setSerKei2000forPressure()
    """K2000にコマンドを送信し、応答を取得する"""
    ser.write((command + "\n").encode())  # コマンド送信
    time.sleep(0.1)  # 少し待つ
    response = ser.readline().decode().strip()  # 応答を取得
    return response
'''
def get_pressure():
    
    try:
        voltage = float(getPv2000pressure())  # 数値変換
        #print(voltage)
        pressure = (voltage - 0.000013) * 133400 / 5.00586 + 0.1  # 圧力計算
        return pressure,voltage
    except ValueError:
        return None  # 変換失敗時
# while True:
#     getPv2000()
#     getPv2182A()
#     time.sleep(1)
    
'''
print(getPv2000())
print(getPv2182A())
print(getPv2000pressure())
print(get_pressure())
'''