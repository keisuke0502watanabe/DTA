import Keigetpv
import ChsetSv
import time
import setScanrate
import threading
import csv
import os
import vttotemp


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

k = 0
l = 0
for i in range(int(x)):
    if text[k][l] == k+1:
        print(k)
        Tsv = text[k][l+1]
        Tf = text[k][l+2]
        rate = text[k][l+3]
        wait = text[k][l+4]
        dt = rate/60
        time.sleep(wait)
        while True:
                time.sleep(2)
                t1 = time.time()
                t2 = t1-t3
                t3 = t1
                Tsv = float(Tsv) + dt*t2
                ChsetSv.setSv(Tsv)
                pv2000 = float(Keigetpv.getPv2000())*1000000
                pv2182A = float(Keigetpv.getPv2182A())*1000000
                vttotemp.VtToTemp(pv2000)
                vttotemp.VtToTemp(pv2182A)
                am.amb(round(t1-t0,3),pv2182A,vttotemp.VtToTemp(pv2000))
                f = open(str(filenameResults)+".csv", mode='a')
                result = "{:.3f}\t {:.3f}\t {:.10f}\t {:.10f}\t {:.10f}\t {:.10f}\n".format(float(Tsv),float(t1-t0),pv2000,pv2182A,vttotemp.VtToTemp(pv2000),vttotemp.VtToTemp(pv2182A))
                if rate > 0:
                    hoc = "heat"
                elif rate < 0:
                    hoc = "cool"
                print(round(Tsv,3),round(t1-t0,3),pv2000,pv2182A,vttotemp.VtToTemp(pv2000),vttotemp.VtToTemp(pv2182A))
                f.write(result + hoc)
                print(round(Tsv,3),round(t1-t0,3),pv2000,pv2182A,vttotemp.VtToTemp(pv2000),vttotemp.VtToTemp(pv2182A))
                f.write(result)
                if rate > 0:
                    if float(Tsv) >= float(Tf):
                        print("finish")
                        break
                else:
                    if float(Tsv) <= float(Tf):
                        print("finish")
                        break
                f.close()
        k += 1

