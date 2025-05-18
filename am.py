import ambient
import vttotemp
import Keigetpv

def amb(t3,pv2192A,a):
    ambi = ambient.Ambient(50282, "ae582ef6ca0cdef8") # ご自分のチャネルID、ライトキーに置き換えてください
    pv2182A = float(Keigetpv.getPv2182A())*1000000
    pv2000 = float(Keigetpv.getPv2000())*1000000
    r = ambi.send({"d1": t3,"d2": pv2182A,"d3": vttotemp.VtToTemp(pv2000)})
    