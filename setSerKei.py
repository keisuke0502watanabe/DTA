#Set the parameters for serial with omron
import serial

def setSerKei2000():
    with serial.Serial('/dev/ttyUSB3') as ser2000:
        ser2000.baudrate=9600
        ser2000.bytesize=serial.EIGHTBITS
        ser2000.parity=serial.PARITY_NONE
        ser2000.stopbits=serial.STOPBITS_ONE
        ser2000.xonxoff=False
        ser2000.timeout=5
        
    return ser2000

def setSerKei2182A():
    with serial.Serial('/dev/ttyUSB2') as ser2182A:
        ser2182A.baudrate=9600
        ser2182A.bytesize=serial.EIGHTBITS
        ser2182A.parity=serial.PARITY_NONE
        ser2182A.stopbits=serial.STOPBITS_ONE
        ser2182A.xonxoff=False
        ser2182A.timeout=5
        
    return ser2182A

def setSerKei2000forPressure():
    with serial.Serial('/dev/ttyUSB0') as ser2000pressure:
        ser2000pressure.baudrate=9600
        ser2000pressure.bytesize=serial.EIGHTBITS
        ser2000pressure.parity=serial.PARITY_NONE
        ser2000pressure.stopbits=serial.STOPBITS_ONE
        ser2000pressure.xonxoff=False
        ser2000pressure.timeout=5
        
    return ser2000pressure

#print(setSerKei2000())
#print(setSerKei2182A())