#omron rs232c 
import serial
import time
import struct
# from operator import xor
import chksumKei
import setSerKei
import traceback

def clear_buffer(ser):
    """シリアルバッファをクリア"""
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
    except Exception as e:
        print("Buffer clear error: {}".format(str(e)))

def getPv2000(max_retries=3):
    """Kei2000からデータを取得（リトライ機能付き）"""
    for attempt in range(max_retries):
        try:
            ser = setSerKei.setSerKei2000()
            ser.timeout = 1  # タイムアウトを1秒に設定
            ser.write_timeout = 1
            ser.open()
            clear_buffer(ser)

            # コマンド送信
            y = ":FETCh?"
            x = y.encode()
            ser.write(x)
            ser.write(b'\r')
            
            # データ受信
            c = ""
            start_time = time.time()
            while True:
                if time.time() - start_time > ser.timeout:
                    raise TimeoutError("Kei2000 response timeout")
                    
                if ser.in_waiting > 0:
                    recv_data = ser.read()
                    a = struct.unpack_from("B", recv_data, 0)
                    b = chr(a[0])
                    c += b
                    if len(c) == 15:
                        return c
                        
        except Exception as e:
            print("Kei2000 attempt {} failed: {}".format(attempt + 1, str(e)))
            if attempt == max_retries - 1:
                print("Kei2000: Max retries reached")
                return None
            time.sleep(0.1)  # リトライ前に短い待機
        finally:
            try:
                ser.close()
            except:
                pass

def getPv2182A(max_retries=3):
    """Kei2182Aからデータを取得（リトライ機能付き）"""
    for attempt in range(max_retries):
        try:
            ser = setSerKei.setSerKei2182A()
            ser.timeout = 1
            ser.write_timeout = 1
            ser.open()
            clear_buffer(ser)

            # コマンド送信
            y = ":FETCh?"
            x = y.encode()
            ser.write(x)
            ser.write(b'\r')
            
            # データ受信
            c = ""
            start_time = time.time()
            while True:
                if time.time() - start_time > ser.timeout:
                    raise TimeoutError("Kei2182A response timeout")
                    
                if ser.in_waiting > 0:
                    recv_data = ser.read()
                    a = struct.unpack_from("B", recv_data, 0)
                    b = chr(a[0])
                    c += b
                    if len(c) == 15:
                        return c
                        
        except Exception as e:
            print("Kei2182A attempt {} failed: {}".format(attempt + 1, str(e)))
            if attempt == max_retries - 1:
                print("Kei2182A: Max retries reached")
                return None
            time.sleep(0.1)
        finally:
            try:
                ser.close()
            except:
                pass

def getPv2000pressure(max_retries=3):
    """Kei2000から圧力データを取得（リトライ機能付き）"""
    for attempt in range(max_retries):
        try:
            ser = setSerKei.setSerKei2000forPressure()
            ser.timeout = 1
            ser.write_timeout = 1
            ser.open()
            clear_buffer(ser)

            # コマンド送信
            y = ":FETCh?"
            x = y.encode()
            ser.write(x)
            ser.write(b'\r')
            
            # データ受信
            c = ""
            start_time = time.time()
            while True:
                if time.time() - start_time > ser.timeout:
                    raise TimeoutError("Kei2000 pressure response timeout")
                    
                if ser.in_waiting > 0:
                    recv_data = ser.read()
                    a = struct.unpack_from("B", recv_data, 0)
                    b = chr(a[0])
                    c += b
                    if len(c) == 15:
                        return c
                        
        except Exception as e:
            print("Kei2000 pressure attempt {} failed: {}".format(attempt + 1, str(e)))
            if attempt == max_retries - 1:
                print("Kei2000 pressure: Max retries reached")
                return None
            time.sleep(0.1)
        finally:
            try:
                ser.close()
            except:
                pass

def get_pressure():
    """圧力値を取得（エラーハンドリング付き）"""
    try:
        voltage = getPv2000pressure()
        if voltage is None:
            return None, None
        voltage = float(voltage)
        pressure = (voltage - 0.000013) * 133400 / 5.00586 + 0.1
        return pressure, voltage
    except Exception as e:
        print("Pressure calculation error: {}".format(str(e)))
        return None, None

# テスト用コード
if __name__ == "__main__":
    print("Testing Kei2000...")
    print(getPv2000())
    print("\nTesting Kei2182A...")
    print(getPv2182A())
    print("\nTesting Kei2000 pressure...")
    print(getPv2000pressure())
    print("\nTesting pressure calculation...")
    print(get_pressure())