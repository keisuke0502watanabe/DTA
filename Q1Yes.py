import Keigetpv
import Chino
import time
import datetime
import setScanrate
import threading
import csv
import os
import vttotemp
#import am
import traceback
from natsort import natsorted

#import 
import requests
import stepmotor
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials

 #鍵 

#APIにログイン
#scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#credentials = ServiceAccountCredentials.from_json_keyfile_name(key_name, scope)
#gc = gspread.authorize(credentials)

'''
def columnSet(wks):
    cell_number1 = 'A1'
    input_value1 = 'set Temp. / K'
    #wks = gc.open(sheet_name).sheet1
    wks.update_acell(cell_number1, input_value1)
    cell_number2 = 'B1'
    input_value2 = 'time / s'
    wks.update_acell(cell_number2, input_value2)
    cell_number3 = 'C1'
    input_value3 = 'dt of Kei2000/ microvolts'
    wks.update_acell(cell_number3, input_value3)
    cell_number4 = 'D1'
    input_value4 = 'dt of Kei2182A/ microvolts'
    wks.update_acell(cell_number4, input_value4)
    cell_number5 = 'E1'
    input_value5 = 'dt of Kei2000/K'
    wks.update_acell(cell_number5, input_value5)
    cell_number6 = 'F1'
    input_value6 = 'dt of Kei2182A/K'
    wks.update_acell(cell_number6, input_value6)
    cell_number7 = 'G1'
    input_value7 = 'Heat or cool '
    wks.update_acell(cell_number7, input_value7)
    cell_number8 = 'H1'
    input_value8 = 'Run'
    wks.update_acell(cell_number8, input_value8)
    cell_number9 = 'I1'
    input_value9 = 'Date'
    wks.update_acell(cell_number9, input_value9)
    cell_number10 = 'J1'
    input_value10 = 'Date time'
    wks.update_acell(cell_number10, input_value10)
    cell_number11 = 'K1'
    input_value11 = 'Sample name'
    wks.update_acell(cell_number11, input_value11)
    cell_list = wks.range('A2:K11')

def wksUpdate(wks,cell_list):
    wks.update_cells(cell_list)

def cellListUpdate(wks,sheet_pointer):
            try:
                cell_list = wks.range('A'+str(sheet_pointer)+':K'+str(sheet_pointer+9))                
            except:
                wks.add_rows(10000)
                cell_list = wks.range('A'+str(sheet_pointer)+':K'+str(sheet_pointer+9))

def ambTh(t0, t1, pv2182A, pv2000, filenameError):
        try:
                am.amb(float(round(t1-t0,3)),float(pv2182A),float(vttotemp.VtToTemp(pv2000)))
        except:
                traceback.print_exc()
                f = open(str(filenameError), mode='a')
                f.write(str(time.time()))
                f.write(', row=145 \n')
                f.write(str(traceback.print_exc()))
                f.write('\n')
                f.close()
                line_notify(str(traceback.print_exc()))
''' 
cell_list=[]
sheet_pointer =2
list_pointer = 0
#wks = gc.open(sheet_name).sheet1
#thread1 = threading.Thread(target=columnSet, args=(wks,))
#thread2 = threading.Thread(target=wksUpdate, args=(wks,cell_list,))
#l = 0

#thread3 = threading.Thread(target=cellListUpdate, args=(wks, sheet_pointer,))

#print(sheet_name)

#print(Keigetpv.get_pressure())
#　以下本文
m = 1
text = []
Q1 = input("Do you want to control the stepping mortor. y/n:")
if Q1 =='y':
        pulse_count= input('Input the num ber pulses. (100-2300000) :')
        stepmortor.op_stepmortor(pulse_count)
        
Q2 = input("Have you already measured? y/n:")
sampleName=input("What is the sample name?")
if Q2 == 'y':
    path='/home/yasumotosuzuka/Desktop/dta/Experiment_condition'
    os.chdir(path)
    list=os.listdir(path)
    list=natsorted(list)
    for i in range(len(list)):
        print(str(i) + " : " + list[i])
    
    num = int(input("What is the number of the condition file?:"))
    filenameExpCond = list[num]
    filenameResults = filenameExpCond.replace('ExpCond.csv','Results.csv')
    filenameError = filenameExpCond.replace('ExpCond.csv','Error.csv')
#     filenameResults = filenameExpCond+'_Results.csv'
#     filenameError = filenameExpCond+'Error.csv'

elif Q2 == 'n':
    #sampleName = input("What is name of the samle :")
    filenameExpCond = sampleName + "ExpCond.csv"
    filenameResults = sampleName + "Results.csv"
    filenameError = sampleName + "Error.csv"
    f = open(str(filenameExpCond), mode='a')
    f.close()
    f = open(str(filenameError), mode='a')
    f.close()
print(os.getcwd())
with open(filenameExpCond,'r') as file:
    reader = csv.reader(file)
    line = [row for row in reader]
#     print(len(line))
    
for i in range(1,len(line)):
        print('exp. '+str(i) +' : ')
        print(line[i])
    
os.chdir("/home/yasumotosuzuka/Desktop/dta/Experiment_result")
print(os.path.exists(filenameResults))
print(os.listdir())
if not os.path.exists(filenameResults):
    #thread1.start()
    f = open(str(filenameResults), mode='a')
    f.write("No.\tset Temp./K\ttime/s\tdt(Kei2000)/volts\tdt(Kei2182A)/volts\tTemp(Kei2182A)/K\tHeat or cool\tRun\tDate\tTime of Day\tSampleName\tP/MPa\tVp/volts\tTpv(Chino)\n")
    f.close()


     
#Read exp. condition
Tsv=['Tsv']
Tf=['Tf']
rate=['rate']
wait=['wait']
dt=['dt']
timeExp=0
for k in range(1,len(line)):
    Tsv.append(float(line[k][1]))
    Tf.append(float(line[k][2]))
    # 温度変化の方向を確認し、rateの符号を自動調整
    rate_value = float(line[k][3])
    if Tsv[k] > Tf[k]:  # 冷却実験の場合
        if rate_value > 0:  # 正の値が入力されている場合
            print(f"Warning: 冷却実験ですが、rateが正の値です。自動的に符号を反転します。")
            print(f"Tsv: {Tsv[k]}K, Tf: {Tf[k]}K, 元のrate: {rate_value}K/min")
            rate_value = -rate_value
    elif Tsv[k] < Tf[k]:  # 加熱実験の場合
        if rate_value < 0:  # 負の値が入力されている場合
            print(f"Warning: 加熱実験ですが、rateが負の値です。自動的に符号を反転します。")
            print(f"Tsv: {Tsv[k]}K, Tf: {Tf[k]}K, 元のrate: {rate_value}K/min")
            rate_value = -rate_value
    rate.append(rate_value)
    wait.append(float(line[k][4]))
    dt_round=round(float(line[k][3])/60,3)
    dt.append(dt_round)
    print(k,Tsv, Tf, rate, wait, dt)
    timeExp=timeExp+abs((Tf[k]-Tsv[k])/rate[k])+wait[k]/60
    print(k, timeExp)
timeExp=timeExp-wait[k]/60
print(timeExp)

#csv sheet column settting
    #if i == 0:


#change temp. to first Tsv
Chino.setSv(Tsv[1])
Tsv_prev=Tsv[1]
Tsvtemp=Tsv[1]
wait1st=float(input("How long will you wait before 1st measurement? [sec]: "))
print("The measurement started at "+ str(datetime.datetime.now()))
#line_notify("The measurement started at "+ str(datetime.datetime.now()))
td = datetime.timedelta(minutes=timeExp)
print("The measurement will finish at "+str(datetime.datetime.now()+td))
#line_notify("The measurement will finish at "+str(datetime.datetime.now()+td))
time.sleep(wait1st)

t0 = time.time()
t3 = t0

def update_temperature(rate_k, Tsvtemp, Tf_k, dt_k, t2, Tsv_prev):
    """
    温度制御を行う関数
    Args:
        rate_k: 温度変化率 (K/min)
        Tsvtemp: 現在の温度設定値 (K)
        Tf_k: 目標温度 (K)
        dt_k: 時間間隔 (min)
        t2: 経過時間 (s)
        Tsv_prev: 前回の温度設定値 (K)
    Returns:
        Tsvtemp: 更新された温度設定値 (K)
        Tsv_prev: 更新された前回の温度設定値 (K)
    """
    try:
        # 加熱時: 現在温度が目標温度以下の場合、温度を上昇
        if (rate_k > 0 and float(Tsvtemp) <= float(Tf_k)):
            Tsvtemp = Tsvtemp + dt_k*t2
        # 冷却時: 現在温度が目標温度以上の場合、温度を下降
        elif (rate_k < 0 and float(Tsvtemp) >= float(Tf_k)):
            Tsvtemp = Tsvtemp + dt_k*t2
            
        # 温度設定値が0.1K以上変化した場合のみ、温度制御器に設定値を送信
        if not(round(Tsvtemp,1)==Tsv_prev):
            Chino.setSv(Tsvtemp)
        Tsv_prev=Tsvtemp
    except:
        pass
    return Tsvtemp, Tsv_prev

for k in range(1,len(line)):
    print("Run the measurement number " + str(k) +" ! Tsv= "+str(Tsv[k])+" K" )
    #line_notify("Run the measurement number " + str(k) +" ! Tsv= "+str(Tsv[k])+" K")
    if k ==1:
        print("Wait for " + str(wait1st) +" sec.")
    else:
        print("Wait for " + str(wait[k-1]) +" sec.")
    print(rate[k])
    print(dt[k])
    
    header="No." + "Run " + " Date       Time"+ "     t/s  Tsv / K"+ "   pv2000  "+ "pv2182A"+ "  Tpv2182"+ "   Tpvchino"+" P / MPa"+ " pv2000pressure"
    print(header)

    while True:
        list_pointer+=1
        time.sleep(.5)
        #?
        try:
            a = Chino.getPv()
        except:
            pass
        
        #sheet_pointer
        # 測定
        time.sleep(1)
        t1 = time.time()
        t2 = t1-t3
        t3 = t1
        
        # 最初の測定の場合
        if k==1:
            Tsvtemp, Tsv_prev = update_temperature(rate[k], Tsvtemp, Tf[k], dt[k], t2, Tsv_prev)
        # 2回目以降の測定の場合、待機時間を考慮
        else:
            if t1 > t4+wait[k-1]:
                Tsvtemp, Tsv_prev = update_temperature(rate[k], Tsvtemp, Tf[k], dt[k], t2, Tsv_prev)
        try:
            t1 = time.time()
            pv2000 = float(Keigetpv.getPv2000())
            pv2182A = float(Keigetpv.getPv2182A())
            Tpv2000=vttotemp.VtToTemp(pv2000)
            a = vttotemp.VtToTemp(pv2000)
            Tpv2182A=vttotemp.VtToTemp(pv2182A*1000000)
            Tpvchino=Chino.getPv()
        except:
            pass
                # 記録＆可視化
#        
# threadAmb = threading.Thread(target=ambTh, args=(t0, t1, pv2182A, pv2000,filenameError,))
# threadAmb.start()
        f = open(str(filenameResults), mode='a')
        if rate[k] > 0:
                    hoc = "heat"
        elif rate[k] < 0:
                    hoc = "cool"
        # Get current time
        current_time = datetime.datetime.now()

        # Format with 2 decimal places for seconds
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-7]
        try:
            pressure,Vp=Keigetpv.get_pressure()
        except:
            pass
        
        try:
            print(
            list_pointer, "", 
            k, " ", 
            formatted_time,
            round(float(t1-t0), 1) if (t1 is not None and t0 is not None) else 0.0,
            round(Tsvtemp, 3) if Tsvtemp is not None else 0.0,
            "  ",
            round(pv2000*1000, 2) if pv2000 is not None else 0.0,
            "m ",
            round(pv2182A, 5) if pv2182A is not None else 0.0,
            " ",
            round(Tpv2182A, 2) if Tpv2182A is not None else 0.0,
            "   ",
            round(Tpvchino, 2) if Tpvchino is not None else 0.0,
            round(pressure, 5) if pressure is not None else 0.0,
            Vp if Vp is not None else ""
            )
            #print(k, " ",formatted_time,round(float(t1-t0),1),round(Tsvtemp,3),round(pv2000,2),round(pv2182A,5),round(Tpv2000,2),"   ",round(Tpvchino,2),round(pressure,5),Vp)
            
            result = "{}\t{:.3f}\t {:.10f}\t {:.10f}\t {:.10f}\t {:.10f}\t {} \t {} \t {} \t {} \t {} \t {} \t {}\t{}\n".format(
            list_pointer,
            round(float(Tsvtemp),3) if round(float(Tsvtemp),3) is not None else 0.0,
            round(float(t1-t0),2) if round(float(t1-t0),1) is not None else 0.0,
            pv2000 if pv2000 is not None else 0.0,

            pv2182A if pv2182A is not None else 0.0,
            round(Tpv2182A, 2) if Tpv2182A is not None else 0.0,
            hoc if hoc is not None else "",
            k if k is not None else "",
            datetime.date.today(),
            datetime.datetime.now().time(),
            sampleName if sampleName is not None else "",
            pressure if pressure is not None else 0.0,
            Vp if Vp is not None else "",
            round(Tpvchino, 2) if Tpvchino is not None else 0.0
            )
            '''
            pv2182A,
            #Tpv2000 if round(Tpv2000,2) is not None else 0.0,
            Tpv2182A if round(Tpv2182A,2) is not None else 0.0,
            hoc,
            k,
            datetime.date.today(),
            datetime.datetime.now().time(),
            sampleName,
            pressure,
            Vp,
            Tpvchino
            '''
            
            #print(round(pv2000,2))
            f.write(result)
        #except:
            #pass
        except Exception as e:
            print(f"Error formatting result: {e}")
            #print(298)
            # Either define a default result or skip writing to file
            # For example:
            default_result = f"{Tsvtemp}\t {t1-t0}\t {pv2000}\t {pv2182A}\t ERROR\t {hoc}\t {k} \t {datetime.date.today()} \t {datetime.datetime.now().time()} \t {sampleName} \t {pressure} \t {Vp}\n \t {Tpvchino}"
            f.write(default_result)
        #f.write(result)
        f.close()
        '''
        try:
                    cell_list[list_pointer].value= float(Tsv[k])
                    cell_list[list_pointer+1].value=float(t1-t0)
                    cell_list[list_pointer+2].value=pv2000
                    cell_list[list_pointer+3].value=pv2182A
                    cell_list[list_pointer+4].value=vttotemp.VtToTemp(pv2000)
                    cell_list[list_pointer+5].value=vttotemp.VtToTemp(pv2182A)
                    cell_list[list_pointer+6].value=hoc
                    cell_list[list_pointer+7].value=k
                    cell_list[list_pointer+8].value=str(datetime.date.today())
                    cell_list[list_pointer+9].value=str(datetime.datetime.now().time())
                    cell_list[list_pointer+10].value=sampleName
                    
        except:
                    pass
        '''
        if (list_pointer % 10) == 0:
            print('upload')
            print(header)
        

        '''
            try:
                thread2.start()
            except:
                pass
        '''
            #wks.update_cells(cell_list)
            #list_pointer = 0
            #sheet_pointer += 10
                        
#############  
# 2022/07/05 Watanabe commented out, modified
        '''
            try:
                thread3.start()
            except:
                pass
        '''
#############
        # 終了条件
        try:
            if (rate[k] > 0 and float(Tsvtemp) >= float(Tf[k])):
                print(k)
                print(rate[k])
                print("Run " + str(k) + " was finished")                           
                print("wait for" + str(wait[k]) + " sec.")
                #time.sleep(wait[k])
                t4 = time.time()
                list_pointer=0
                break
                            
            elif (rate[k] < 0 and float(Tsvtemp) <= float(Tf[k])):
                print(k)
                print(Tsv[k])
                print(Tf[k])
                print("Run " + str(k) + " was finished")
                print("wait for" + str(wait[k]) + " sec.")     
                #time.sleep(wait[k])
                t4 = time.time()
                list_pointer=0
                break
        except:
            pass

    
#line_notify("finished")
 