# parabolix
I misspelled "parabolic" whilst trying to do something in desmos - here's a bad model of a rocket nozzle/combustor.

### Dependencies:
- numpy
- matplotlib.pyplot
- scipy.integrate

## Development
### Done:
- terrible geometry plotter thingy, I don't know if I defined a single actual parabola there (lots of arcs and tan functions)
- CEARUN output file parser: single chamber pressure/mixture, requires transport properties + consider ionised species + equilibrium + finite area (contraction ratio)

### Todo:
- Bartz correlation h_g/heat flux plot, maybe integrate everything and get total heating in watts for each component (chamber, throat, nozzle sections)
- Ultimately an attempt at modelling radiative/regenerative cooling, and estimating materials/masses
- Fix the CEARUN parser so it can handle stuff 
- Longterm perhaps integration of turbopumps/preburners/pressure-fed tankage
- Definitely at some point fix the geometry plotter so it isn't using a bunch of halfassed guesstimations for formulae

## Example output
### Geometry
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

### CEARUN parser
Using [cearun.txt](https://github.com/PearBabyPlc/parabolix/blob/main/cearun.txt) as the input, [parsedVerbose.txt](https://github.com/PearBabyPlc/parabolix/blob/main/parsedVerbose.txt) was generated (by iterating and printing each object in the list returned by `parser.parseCEARUN()`). This is the summarised version (using the `parser.Positions.summary()` method):
```
INJECTOR: A/At = 0.0, T = 3447.03K, P = 50.0bar, V = 0.0m/s
COMB END: A/At = 2.737, T = 3433.9K, P = 47.296bar, V = 361.2m/s
THROAT: A/At = 1.0, T = 3250.61K, P = 28.019bar, V = 1563.2m/s
EXIT: A/At = 9.0, T = 1996.38K, P = 0.75338bar, V = 3830.4m/s
EXIT: A/At = 20.0, T = 1644.42K, P = 0.2582bar, V = 4140.4m/s
EXIT: A/At = 36.0, T = 1413.97K, P = 0.11823bar, V = 4319.3m/s
EXIT: A/At = 64.0, T = 1211.12K, P = 0.05512bar, V = 4463.9m/s
EXIT: A/At = 100.0, T = 1068.27K, P = 0.03047bar, V = 4558.8m/s
EXIT: A/At = 120.0, T = 1013.43K, P = 0.0239bar, V = 4593.8m/s
EXIT: A/At = 144.0, T = 960.63K, P = 0.01875bar, V = 4626.8m/s
EXIT: A/At = 175.0, T = 906.36K, P = 0.01445bar, V = 4660.0m/s
EXIT: A/At = 209.22, T = 858.65K, P = 0.01138bar, V = 4688.6m/s
```
