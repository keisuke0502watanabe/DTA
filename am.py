import ambient
import vttotemp
import Keigetpv

def amb(t3,pv2192A,a):
    ambi = ambient.Ambient(42763, "311dc99d4fd11d1a") # ご自分のチャネルID、ライトキーに置き換えてください
#     pvc=pv-273.2
#     pvc=int(round(pvc,1))
#     print(pvc)
    pv2182A = float(Keigetpv.getPv2182A())*1000000
    pv2000 = float(Keigetpv.getPv2000())*1000000
    r = ambi.send({"d1": t3,"d2": pv2182A,"d3": vttotemp.VtToTemp(pv2000)})
    