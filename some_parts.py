import Keigetpv
import Chset
import time
import setScanrate
import threading
import csv
import os
import vttotemp
import am

def measurepart(Tsv,dt):
    # 測定
    t1 = time.time()
    #t2 = t1-t3
    #t3 = t1
    Tsv = float(Tsv) + dt*t2
    Chset.setSv(Tsv)
    pv2000 = float(Keigetpv.getPv2000())*1000000
    pv2182A = float(Keigetpv.getPv2182A())*1000000
    vttotemp.VtToTemp(pv2000)
    vttotemp.VtToTemp(pv2182A)
    return t1, t2, t3, Tsv, Chset.setSv(Tsv), pv2000, pv2182A, vttotemp.VtToTemp(pv2000), vttotemp.VtToTemp(pv2182A)
    
dt = 0.2
x = measurepart(dt)
def vis_and_logpart(x):
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
        
def completionpart(Tsv,Tf):
    # 終了条件
    while True:
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
