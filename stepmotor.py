import gpiod
import time
import Keigetpv

# GPIO設定
CW_PIN = 18   # GPIO18 をCW用に使用
CCW_PIN = 17  # GPIO17 をCCW用に使用

# パルス信号のパラメータ
pulse_count = 100      # 送信するパルス数
pulse_width = 0.0005   # パルスの幅（秒）
pulse_delay = 0.0005   # パルス間の遅延（秒）

# モーターにパルスを送信する関数
def send_pulses(line, pulses):
    for i in range(pulses):
        line.set_value(1)  # HIGH
        time.sleep(pulse_width)
        line.set_value(0)  # LOW
        time.sleep(pulse_delay)

def op_stepmortor(pulse_count):
    # 使用可能なチップを自動的に見つける
    chip_path = None
    for i in range(10):  # 0から9までのチップを確認
        try:
            chip = gpiod.Chip(f'gpiochip{i}', gpiod.Chip.OPEN_BY_NAME)
            chip_path = f'gpiochip{i}'
            chip.close()
            break
        except:
            continue

    if chip_path is None:
        print("使用可能なGPIOチップが見つかりませんでした")
        exit(1)
        
    print(f"使用するGPIOチップ: {chip_path}")
    chip = gpiod.Chip(chip_path, gpiod.Chip.OPEN_BY_NAME)

    try:
        # CWとCCWのGPIOラインを取得
        cw_line = chip.get_line(CW_PIN)
        ccw_line = chip.get_line(CCW_PIN)
        
        # 出力モードに設定
        cw_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
        ccw_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
        
        # 初期状態は0
        cw_line.set_value(0)
        ccw_line.set_value(0)
        
        print("GPIOピンを初期化しました")
        print("操作方法:")
        print("  f: 時計回り(CW, clockwise, to push)に回転")
        print("  b: 反時計回り(CCW, counter clock wise, to pull)に回転")
        print("  q: プログラム終了, quit the control of the stepping mortor")
        
        # メインループ
        while True:
            pressure,Vp=Keigetpv.get_pressure()
            print("P/MPa", "Voltage")
            print(pressure, Vp)
            command = input("コマンドを入力してください (f/b/q): ").strip().lower()
            
            if command == 'f':
                print("時計回り(CW: clockwise, to push)に回転...")
                send_pulses(cw_line, pulse_count)
                print("完了")
                
            elif command == 'b':
                print("反時計回り(CCW: counter clockwise, to pull)に回転...")
                send_pulses(ccw_line, pulse_count)
                print("完了")
                
            elif command == 'q':
                print("To change the pulse count or Finish controlling the steping mortor")
                break
                
            else:
                print(f"無効なコマンド: {command}")
                
    except KeyboardInterrupt:
        print("\nプログラムが中断されました")
        
    finally:
        # GPIOリソースを解放
        try:
            cw_line.release()
            ccw_line.release()
        except:
            pass
        
        chip.close()
        print("GPIOリソースを解放しました")

op_stepmortor(pulse_count)