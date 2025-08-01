# parabolix
I misspelled "parabolic" whilst trying to do something in desmos - here's a bad model of a rocket nozzle/combustor

### Done:
- terrible geometry plotter thingy, I don't know if I defined a single actual parabola there (lots of arcs and tan functions)

### Todo:
- CEARUN output file parser (will only take single mixtures/pressures since I can't be arsed for now)
- Bartz correlation h_g/heat flux plot, maybe integrate everything and get total heating in watts for each component (chamber, throat, nozzle sections)
- Ultimately an attempt at modelling radiative/regenerative cooling, and estimating materials/masses
- Longterm perhaps integration of turbopumps/preburners/pressure-fed tankage
- Definitely at some point fix the geometry plotter so it isn't using a bunch of halfassed guesstimations for formulae

## Example output
![Example output](https://github.com/PearBabyPlc/parabolix/blob/main/parabolix.png)

This was generated with the following input:
```
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
```
