lines = []

with open("cearun.txt") as cearun:
    for line in cearun:
        lines.append(line)

print("CEARUN file:")
for line in lines:
    print(line)

'''
i guess that I'll look for the lines that start with a bunch of spaces and
the first characters are "INJECTOR"

then make sure the next characters are "COMB END", "THROAT"

then count the number of "EXIT"s
if it's 5 parse as a full block, if any less only parse as many as counted

create a new blockList from the line with "INJECTOR" to the line with
"* THERMODYNAMIC PROPERTIES FITTED TO 20000.K"

create a blockDict, "station": "INJECTOR"

for most properties i.e. "Pinj/P" add to each blockDict (standard 3 and the other EXITs)
if there's a line "WITH EQUILIBRIUM REACTIONS", ignore the Cp line
if there's "WITH FROZEN REACTIONS" ignore until "PERFORMANCE PARAMETERS"

after "PERFORMANCE PERAMETERS", make sure data isn't appended to
the "INJECTOR" dict - straight to the "COMB END"

ignore from "MASS FRACTION" to "* THERMODYNAMIC..."

repeat this block process until none left
when ingesting numbers, make sure that if there is a space and a
single 0 then another space, that the value is multiplied by
10^0.
if there is a minus at the trailing end, multiply by 10^-num


'''
