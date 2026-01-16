import numpy as N
from datetime import datetime

STD = 1013
ISA = 15

def beräkna_TAS(ALT, IAS, QNH, OAT):
    TH = (ALT + ((STD - QNH) * 27))
    K_ISA = ISA + (-2 * (TH / 1000))
    DH = TH + (120 * (OAT - K_ISA))
    TAS = IAS * (1 + (DH / 1000) * 0.02)
    return f"{TAS:.1f} kt"

def beräkna_WCA(WS, TAS, WD, MT):
    WA = (WD - MT) % 360
    formel = (WS / TAS) * N.sin(N.radians(WA))
    if abs(formel) > 1:
        return "Fel: Vindkomponenten är för stor."
    WCA = N.degrees(N.arcsin(formel))
    MH = (WCA + MT) % 360
    return f"WCA: {WCA:.1f}°\nMH: {MH:.1f}°"

def beräkna_GS(TAS, WS, WD, MH):
    WA = (WD - MH) % 360
    GS = N.sqrt(TAS**2 + WS**2 - 2*TAS*WS*N.cos(N.radians(WA)))
    return f"{GS:.1f} kt"

def beräkna_TH(ALT, QNH):
    TH = (ALT + ((STD - QNH) * 27))
    return f"{TH:.1f} ft"

def beräkna_DH(ALT, QNH, OAT):
    TH = (ALT + ((STD - QNH) * 27))
    K_ISA = ISA + (-2 * (TH / 1000))
    DH = TH + (120 * (OAT - K_ISA))
    return f"{DH:.1f} ft"

def beräkna_VK(RW, WD, WS):
    WA = (WD - RW) % 360
    WA_rad = N.radians(WA)
    SV = N.sin(WA_rad) * WS
    MV = N.cos(WA_rad) * WS

    sid = "från höger" if SV > 0 else "från vänster" if SV < 0 else "ingen sidvind"
    mot = "motvind" if MV > 0 else "medvind" if MV < 0 else "ingen mot-/medvind"

    return (
        f"Sidvind: {abs(SV):.1f} kt ({sid})\n"
        f"Motvind: {abs(MV):.1f} kt ({mot})"
    )

def beräkna_RR(ALT, GND):
    RR = 1.225 * (N.sqrt(ALT) + N.sqrt(GND))
    return f"{RR:.1f} NM"

def beräkna_BT(Tid_On, Tid_Off):
    Tid_On = Tid_On.zfill(4)
    Tid_Off = Tid_Off.zfill(4)
    fmt = "%H%M"
    ONBT = datetime.strptime(Tid_On, fmt)
    OFFBT = datetime.strptime(Tid_Off, fmt)
    if OFFBT < ONBT:
        OFFBT = OFFBT.replace(day=ONBT.day + 1)
    diff = OFFBT - ONBT
    minuter = diff.total_seconds() / 60
    BT = minuter / 60
    return f"{BT:.1f} h ({minuter:.0f} min)"
