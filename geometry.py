import math
import numpy as np
import scipy.integrate as integrate

arcCon = 1.5
arcDiv = 0.382
CCLXX = math.radians(270)
CLXXX = math.radians(180)
XC = math.radians(90)

def getGeometry(designParams):
    Rt = designParams.get("Rt")
    expR = designParams.get("expR")
    conR = designParams.get("conR")
    expA = math.radians(designParams.get("expA"))
    exitA = math.radians(designParams.get("exitA"))
    conA = math.radians(designParams.get("conA"))
    Lstar = designParams.get("Lstar")
    conicA = math.radians(designParams.get("conicA"))
    At = math.pi * Rt**2

    # positive throat arcs
    conAngles = np.linspace(conA, 0.0, num=50)
    divAngles = np.linspace(0.0, expA, num=50)
    tconXs = []
    tconYs = []
    tdivXs = []
    tdivYs = []
    for a in conAngles:
        x = arcCon * Rt * math.cos(CCLXX - a)
        y = arcCon * Rt * math.sin(CCLXX - a) + (1 + arcCon)*Rt
        tconXs.append(x)
        tconYs.append(y)
    for a in divAngles:
        x = arcDiv * Rt * math.cos(CCLXX + a)
        y = arcDiv * Rt * math.sin(CCLXX + a) + (1 + arcDiv)*Rt
        tdivXs.append(x)
        tdivYs.append(y)

    #nozzle tangent func
    Ae = At * expR
    Re = math.sqrt(Ae / math.pi)
    Ln = (Rt*(math.sqrt(expR) - 1) + Re*((1 / math.cos(conicA)) - 1)) / math.tan(conicA)
    xdiv = arcDiv * Rt * math.cos(CCLXX + expA)
    ydiv = arcDiv * Rt * math.sin(CCLXX + expA) + (1 + arcDiv)*Rt
    xexit = xdiv + Ln
    nozXrange = np.linspace(xdiv, xexit, num=250)
    nozzleXs = []
    nozzleYs = []
    for x in nozXrange:
        gx = x / 2
        g = ((-(expA - exitA)) / Ln)*gx + expA
        y = (x - xdiv)*math.tan(g) + ydiv
        nozzleXs.append(x)
        nozzleYs.append(y)

    #converging tangent func
    Ac = At * conR
    Rc = math.sqrt(Ac / math.pi)
    xcon = arcCon * Rt * math.cos(CCLXX - conA)
    ycon = arcCon * Rt * math.sin(CCLXX - conA) + (1 + arcCon)*Rt
    Ltcon = (Rt*(math.sqrt(conR) - 1) + Rc*((1 / math.cos(conA)) - 1)) / math.tan(conA)
    xtcon = xcon - Ltcon
    cconXrange = np.linspace(xtcon, xcon, num=100)
    cconXs = []
    cconYs = []
    for x in cconXrange:
        gx = x / 3
        g = (conA / (Ltcon + xcon)) * (gx + Ltcon)
        y = ((-math.tan(g)) / 2) * (x - xcon) + ycon
        cconXs.append(x)
        cconYs.append(y)

    #chamber linear
    Vc = Lstar * At
    def fThroat(x):
        return math.pi * ((1 + arcCon)*Rt**2 + math.sqrt((arcCon * Rt)**2 - x**2))**2
    def fConv(x):
        gx = x / 3
        g = (conA / (Ltcon + xcon)) * (gx + Ltcon)
        fconi = ((-math.tan(g)) / 2) * (x - xcon) + ycon
        return math.pi * fconi**2
    Vthroat = integrate.quad(lambda x: fThroat(x), xcon, 0)
    Vconv = integrate.quad(lambda x: fConv(x), xtcon, xcon)
    Vrem = Vc - (Vthroat[0] + Vconv[0])
    RcActual = cconYs[0]
    AcActual = math.pi * RcActual**2
    Lrem = Vrem / AcActual
    xinj = xtcon - Lrem
    chamberXs = []
    chamberYs = []
    chamberXrange = np.linspace(xinj, xtcon, num=10)
    for x in chamberXrange:
        chamberXs.append(x)
        chamberYs.append(RcActual)

    #collate into a single bunch of lists and mirror
    geomX = []
    geomY = []
    geomX.extend(chamberXs)
    geomX.extend(cconXs)
    geomX.extend(tconXs)
    geomX.extend(tdivXs)
    geomX.extend(nozzleXs)
    geomY.extend(chamberYs)
    geomY.extend(cconYs)
    geomY.extend(tconYs)
    geomY.extend(tdivYs)
    geomY.extend(nozzleYs)
    mirrX = geomX
    mirrY = []
    for y in geomY:
        my = y * (-1)
        mirrY.append(my)

    #determine actual parameters
    conRactual = AcActual / At
    AnozActual = math.pi * (nozzleYs[-1])**2
    expRactual = AnozActual / At
    Ltotal = Ln - ((xcon - Ltcon) - Lrem)
    actualParams = {
        "expR": expRactual,
        "conR": conRactual,
        "Lnoz": Ln,
        "Lrem": Lrem,
        "Ltotal": Ltotal
    }

    #print parameters
    print("Chamber/throat/nozzle parameters: actual (design)")
    print("Throat radius:", Rt)
    print("Chamber radius:", RcActual)
    print("Nozzle radius:", nozzleYs[-1])
    print("Throat area:", At)
    print("Chamber area:", AcActual)
    print("Nozzle area:", AnozActual)
    expRstring = str("Expansion ratio: " + str(expRactual) + " (" + str(expR) + ")")
    print(expRstring)
    conRstring = str("Contraction ratio: " + str(conRactual) + " (" + str(conR) + ")")
    print(conRstring)
    print("Nozzle length:", Ln)
    print("Total length:", Ltotal)

    geometry = (geomX, geomY, mirrX, mirrY)
    return geometry, actualParams
