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

```
Chamber/throat/nozzle parameters: actual (design)
Throat radius: 0.1
Chamber radius: 0.1654422907003848
Nozzle radius: 1.446461162018512
Throat area: 0.031415926535897934
Chamber area: 0.08598900863665494
Nozzle area: 6.572996894038938
Expansion ratio: 209.22498932279439 (200)
Contraction ratio: 2.7371151552190627 (3)
Nozzle length: 4.26872286882395
Total length: 4.644528975338909
```

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
