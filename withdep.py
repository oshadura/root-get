import os
import sys
from os.path import expanduser

arg1 = sys.argv[1]
arg2 = sys.argv[2]

#cwd = expanduser("~")

dir = []
dir2 = []
pkg = []
paths = []
pkg2 = []
pt2 = []

currentpath = arg1+"/"+arg2+"/CMakeLists.txt"

with open(arg1+"/"+arg2+"/CMakeLists.txt", 'r') as f:
    for line in f:
        if 'add_root_subdirectory' in line:
            line.strip("\n")
            data = line[line.find("(")+1:line.find(")")]
            dir.append(data)

for x in range(len(dir)):
    pkgs = dir[x].split(" ")
    pkg.append(pkgs)

for i in range(len(dir)):
    if pkg[i][1] == 'ALL':
        paths.append(arg1+"/"+arg2+"/"+pkg[i][0])

for pt in paths:
    with open(pt+"/CMakeLists.txt", 'r') as t:
        for line in t:
            if 'ROOT_STANDARD_LIBRARY_PACKAGE' in line:
                pt2.append(pt)
                data2 = line[line.find("(")+1:line.find(")")]
                dir2.append(data2)

for x in range(len(dir2)):
    pkgs2 = dir2[x].split(" ")
    pkg2.append(pkgs2)

pkgnames = []

for i in range(len(pkg2)):
    pkgnames.append(pkg2[i][0] + ":")

deps = {'Foam:' : ['Hist', 'MathCore'],
        'Fumili:' : ['Graf', 'Hist', 'MathCore'],
        'Genetic:' : ['MathCore', 'TMVA'],
        'MathCore:' : ['Imt'],
        'MathMore:' : ['MathCore'],
        'Matrix:' : ['MathCore'],
        'Minuit:' : ['Graf', 'Hist', 'Matrix', 'MathCore'],
        'Minuit2:' : ['MathCore', 'Hist'],
        'MLP:' : ['Hist', 'Matrix', 'Tree', 'Graf', 'Gpad', 'TreePlayer', 'MathCore'],
        'Physics:' : ['Matrix', 'MathCore'],
        'Quadp:' : ['Matrix'],
        'Rtools:' : ['Core', 'MathCore', 'RInterface'],
        'SPlot:' : ['Matrix', 'Hist', 'Tree', 'TreePlayer', 'Graf3d', 'Graf', 'MathCore'],
        'Unuran:' : ['Core', 'Hist', 'MathCore']
        }

for i in range (len(pkgnames)):
    print(pkgnames[i])
    print(" path: " + pt2[i] + "/")
    if pkgnames[i] in deps:
        z = pkgnames[i]
        k = deps.get(z)
        print(" deps: ",end='')
        for j in range(len(k)):
            print (k[j],end=' ')
        print ("")
    else:
        continue
