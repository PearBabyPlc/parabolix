import matplotlib.pyplot as plt
import geometry as geom
import formulaegg as egg
import parser

plt.style.use('dark_background')

designParams = {
    "Rt": 0.1,
    "expR": 200,
    "conR": 3,
    "expA": 30,
    "exitA": 5,
    "conA": 30,
    "Lstar": 0.95,
    "conicA": 18
}

geometry, actualParams = geom.getGeometry(designParams)
geomX, geomY, mirrX, mirrY = geometry

fig, ax = plt.subplots()
ax.plot(geomX, geomY)
ax.plot(mirrX, mirrY)
ax.grid()
plt.gca().set_aspect('equal')
plt.savefig("parabolix.pdf")
plt.show()
