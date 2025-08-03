import math
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import geometry as geom
import formulaegg as egg
import parser

plt.style.use('dark_background')

designParams = {
    "Rt": 0.1,
    "expR": 130,
    "conR": 3,
    "expA": 30,
    "exitA": 5,
    "conA": 30,
    "Lstar": 0.95,
    "conicA": 18
}

egg.printSpacer()
geometry, actualParams = geom.getGeometry(designParams)
geomX, geomY, mirrX, mirrY = geometry
positiveGeom = dict(zip(geomX, geomY))
injectorX = actualParams.get("injectorX")
combEndX = actualParams.get("combEndX")
injectorY = positiveGeom.get(injectorX)
combEndY = positiveGeom.get(combEndX)
injectorLineX = (injectorX, injectorX)
injectorLineY = (injectorY, -injectorY)
combEndLineX = (combEndX, combEndX)
combEndLineY = (combEndY, -combEndY)

egg.printSpacer()
print("Parsed CEARUN data:")
positions = parser.parseCEARUN() #file MUST be named "cearun.txt"
for posEntry in positions:
    print(posEntry.summary())

#egg.printSpacer()
#print("Verbose CEARUN data:")
#for posEntry in positions:
#    print()
#    print(posEntry)

egg.printSpacer()
designWallTemp = 1500
stressesAndFluxes = egg.getStressesAndFluxes(positiveGeom, actualParams, positions, designWallTemp)
plotX = []
plotP = []
plotT = []
plotQ = []
listA = []
for entry in stressesAndFluxes.items():
    x = entry[0]
    ptq = entry[1]
    plotX.append(x)
    pBar = ptq[0] #not actually bar
    plotP.append(pBar)
    plotT.append(ptq[1])
    plotQ.append(ptq[2])
    listA.append(ptq[-1])
    print(x, pBar, ptq[1], ptq[2])

plotXzero = []
for x in plotX:
    plotXzero.append(0)

def getTotalHeating(xarray, ylist, aList):
    it = -1
    yarray = []
    for a in aList:
        it += 1
        r = math.sqrt(a / math.pi)
        c = math.pi * 2 * r
        y = ylist[it] * c
        yarray.append(y)
    return integrate.trapezoid(yarray, xarray)

totalHeating = getTotalHeating(plotX, plotQ, listA)
print("TOTAL HEATING =", totalHeating, "WATTS")
        

fig, (bx, ax) = plt.subplots(2, 1, sharex='col')
ax.plot(geomX, geomY, color='white')
ax.plot(mirrX, mirrY, color='white')
ax.plot(injectorLineX, injectorLineY, linestyle='dashed', color='red')
ax.plot(combEndLineX, combEndLineY, linestyle='dotted', color='yellow')
ax.grid()
plt.gca().set_aspect('equal')
px = ax.twinx()
px.plot(plotX, plotP, color='aqua')
px.set_ylabel('Pressure (Pa)')
#px.set_yscale('log')
bx.plot(plotX, plotT, color='yellow')
bx.set_ylabel('Temperature (K)')
bx.scatter(plotX, plotXzero, marker='*')
qx = bx.twinx()
qx.plot(plotX, plotQ, color='firebrick')
qx.set_ylabel('Heat flux (W/sq m)')
qx.set_yscale('log')
px.grid(linestyle='dashed')
bx.grid()
qx.grid(linestyle='dashed')
plt.savefig("parabolix.pdf")
plt.show()
