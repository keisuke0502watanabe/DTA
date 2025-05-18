import Keigetpv
import Chino
import time
import setScanrate
import threading
import csv
import os
import vttotemp
import am

import gspread
from oauth2client.service_account import ServiceAccountCredentials
 #鍵
key_name = 'temperature-measurement60876-d209c19f9f6c.json'
sheet_name = 'DTA'
#APIにログイン
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(key_name, scope)
gc = gspread.authorize(credentials)

filenameResults = input("What is the name of output in CSV file? :")
x = input("How many times do you scan?:")
for i in range(int(x)):
        
    #Set Tinitial

    Ti = input("Set Ti [K] : ")

    ChsetSv.setSv(Ti)
    Tsv = Ti

    #Set Tfinal
    Tf = input("Set Tf [K] : ")

    #Set scaninng rate
    rate = input("Set the scanning rate [K/min] :")
    rate = int(rate)
    # the scanning rate dt in [K/sec]
    dt = rate/60

    wait = input("How many seconds do you wanna wait before starting?")
    #time.sleep(int(wait))



    t0 = time.time()
    t3 = t0
    
    if i+1 == 1:
        text1 = [str(i+1),Tsv,Tf,str(rate),wait]
        text1 = [float(j) for j in text1]
        text = []
        text.append(text1)
        print(text)
    if float(i+1) >= 2 and float(i+1) <= float(x) :
        text2 = [str(i+1),Tsv,Tf,str(rate),wait]
        text2 = [float(j) for j in text2]
        text.append(text2)
        print(text)
        
f = open(str(filenameResults)+".csv", mode='a')
f.write("set Temp. / K\t time / s\t dt of Kei2000/ microvolts \t dt of Kei2182A/ microvolts\t dt of Kei2000/K \t dt of Kei2182A/K \n")
f.close()

os.chdir("/home/pi/Desktop/Experiment_result")
    f = open(str(filenameResults), mode='a')
    f.write("set Temp. / K\t time / s\t dt of Kei2000/ microvolts \t dt of Kei2182A/ microvolts\t dt of Kei2000/K \t dt of Kei2182A/K \t Heat or cool \n")
    f.close()
    t0 = time.time()
    t3 = t0
    k = 0
    l = 0
    sheet_pointer =2
    list_pointer = 0
    
    for i in range(len(text)):
        print(len(text))
        if text[k][l] == k+1:
            Tsv = text[k][l+1]
            Tf = text[k][l+2]
            rate = text[k][l+3]
            wait = text[k][l+4]
            dt = rate/60

       
        
        print(sheet_name)
        
        if i == 0:
            cell_number1 = 'A1'
            input_value1 = 'set Temp. / K'
            wks = gc.open(sheet_name).sheet1
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
            cell_list = wks.range('A2:H11')
        Chino.setSv(Tsv)
        #print("Chino.setSv(Tsv)")
        #print(Chino.getPv())
        #print(Tsv)
        while True:
            #print("before break")
            #Chino.getPv()
            time.sleep(.5)
            a = Chino.getPv()
#                 print(a)
#                 print(float(Tsv))
            print(a-float(Tsv))
            if ((a - Tsv) < 1.0) and ((a - Tsv) > -1.0):
                print("break")
                break
        print("wait")
        time.sleep(wait)
        while True:
            #sheet_pointer
            # 測定
            time.sleep(1)
            t1 = time.time()
            t2 = t1-t3
            t3 = t1
            Tsv = float(Tsv) + dt*t2
            Chino.setSv(Tsv)
            pv2000 = float(Keigetpv.getPv2000())*1000000
            pv2182A = float(Keigetpv.getPv2182A())*1000000
            vttotemp.VtToTemp(pv2000)
            a = vttotemp.VtToTemp(pv2000)
            vttotemp.VtToTemp(pv2182A)
            # 記録＆可視化
            am.amb(float(round(t1-t0,3)),float(pv2182A),float(vttotemp.VtToTemp(pv2000)))
            f = open(str(filenameResults), mode='a')
            if rate > 0:
                hoc = "heat"
            elif rate < 0:
                hoc = "cool"
            print(round(Tsv,3),round(t1-t0,3),pv2000,pv2182A,vttotemp.VtToTemp(pv2000),vttotemp.VtToTemp(pv2182A))
            result = "{:.3f}\t {:.3f}\t {:.10f}\t {:.10f}\t {:.10f}\t {:.10f}\t {}\t {}\n".format(float(Tsv),float(t1-t0),pv2000,pv2182A,vttotemp.VtToTemp(pv2000),vttotemp.VtToTemp(pv2182A),hoc,k+1)
            f.write(result)
            f.close()
            try:
                cell_list[list_pointer].value= float(Tsv)
                cell_list[list_pointer+1].value=float(t1-t0)
                cell_list[list_pointer+2].value=pv2000
                cell_list[list_pointer+3].value=pv2182A
                cell_list[list_pointer+4].value=vttotemp.VtToTemp(pv2000)
                cell_list[list_pointer+5].value=vttotemp.VtToTemp(pv2182A)
                cell_list[list_pointer+6].value=hoc
                cell_list[list_pointer+7].value=k + 1
            except:
                pass
            list_pointer+=8
            
            if list_pointer > 72:
                print('upload')
                wks.update_cells(cell_list)
                list_pointer = 0
                sheet_pointer += 10
                cell_list = wks.range('A'+str(sheet_pointer)+':H'+str(sheet_pointer+9))
                # 終了条件
                if rate > 0:
                    if float(Tsv) >= float(Tf):
                        print("finish")
                        k = k+1
                        break
                else:
                    if float(Tsv) <= float(Tf):
                        print("finish")
                        k = k+1
                        break
                #sheet_pointer
        continue
