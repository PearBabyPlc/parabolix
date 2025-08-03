import math

omega = 0.6 #exponent of viscosity-temp power law for combustion gas, estimate
rCurv = 0.941 #HuzelHuang "radius of curvature" you multiply throat radius by idk
awt = 0.95

def printSpacer():
    print()
    print("---///---///---///---///---///---")
    print()

def BartzCorrelation(Rt, muIn, CpIn, Pr, PcIn, Cstar, At, A, Tw, Tc, gam, M):
    sigmaA = (1 + ((gam - 1) / 2)*M**2)
    sigmaB = (1/2) * (Tw/Tc) * sigmaA + (1/2)
    sigma = 1 / (sigmaB**(0.8 - omega/5) * sigmaA**(omega/5))
    Dt = 2 * Rt
    Rc = Rt * rCurv
    mu = muIn / 10000 #millipoise to Pa*s conversion
    Cp = CpIn * 1000 #kJ to J/kg-K conversion
    Pc = PcIn * 100000 #bar to Pa conversion
    hgA = 0.026 / (Dt**0.2)
    hgB = (mu**0.2 * Cp) / (Pr**0.6)
    hgC = (Pc / Cstar)**0.8
    hgD = (Dt / Rc)**0.1
    hgE = (At / A)**0.9
    return hgA * hgB * hgC * hgD * hgE * sigma

def getStressesAndFluxes(positiveGeom, actualParams, positions, designWallTemp):
    injectorX = actualParams.get("injectorX")
    combEndX = actualParams.get("combEndX")
    Rinjector = RcombEnd = injectorY = positiveGeom.get(injectorX)
    Ainjector = AcombEnd = math.pi * injectorY**2
    throatX, Rthroat = min(positiveGeom.items(), key=lambda x: abs(0 - x[0]))
    Athroat = math.pi * Rthroat**2
    stressesAndFluxes = {}
    lastEntry = positions[-1]
    Cstar = lastEntry.Cstar
    for entry in positions:
        if entry.position == "INJECTOR":
            hg = BartzCorrelation(Rthroat, entry.mu, entry.Cp, entry.Pr, entry.P,
                                  Cstar, Athroat, Ainjector, designWallTemp,
                                  entry.T, entry.gam, entry.M)
            Q = hg * ((awt * entry.T) - designWallTemp)
            ptqTup = (entry.P, entry.T, Q, Ainjector)
            stressesAndFluxes.update({injectorX: ptqTup})
        elif entry.position == "COMB END":
            hg = BartzCorrelation(Rthroat, entry.mu, entry.Cp, entry.Pr, entry.P,
                                  Cstar, Athroat, AcombEnd, designWallTemp,
                                  entry.T, entry.gam, entry.M)
            Q = hg * ((awt * entry.T) - designWallTemp)
            ptqTup = (entry.P, entry.T, Q, AcombEnd)
            stressesAndFluxes.update({combEndX: ptqTup})
        elif entry.position == "THROAT":
            hg = BartzCorrelation(Rthroat, entry.mu, entry.Cp, entry.Pr, entry.P,
                                  Cstar, Athroat, Athroat, designWallTemp,
                                  entry.T, entry.gam, entry.M)
            Q = hg * ((awt * entry.T) - designWallTemp)
            ptqTup = (entry.P, entry.T, Q, Athroat)
            stressesAndFluxes.update({throatX: ptqTup})
        else:
            A = entry.AR * Athroat
            R = math.sqrt(A / math.pi)
            xRA, yRA = min(positiveGeom.items(), key=lambda x: abs(R - x[1]))
            hg = BartzCorrelation(Rthroat, entry.mu, entry.Cp, entry.Pr, entry.P,
                                  Cstar, Athroat, A, designWallTemp,
                                  entry.T, entry.gam, entry.M)
            Q = hg * ((awt * entry.T) - designWallTemp)
            ptqTup = (entry.P, entry.T, Q, A)
            stressesAndFluxes.update({xRA: ptqTup})        
    return stressesAndFluxes
