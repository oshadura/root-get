import pylab
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import re
import os
import networkx as nx
from dag4pkg import *

dg = Dag4pkg()
count = 0
deplist = []
namelist = []
nodes_set = set()
nodes_set2 = set()

def getdag(arg1, arg2):
    rule_name = re.compile(".*name:.*")
    rule_deps = re.compile(".*deps:.*")

    manifest_dir = os.environ["ROOT_SOURCES"]
    module_file_path = os.environ["ROOT_MODULES"]
    global count
    count = count + 1

    #Case when we are working with package modules
    if count == 1:
        with open(manifest_dir + "/" + arg1 + ".yml") as manifest_file:
            manifest_file_read = manifest_file.read()
            name = rule_name.findall(manifest_file_read)
            deps = rule_deps.findall(manifest_file_read)
            manifest_file.close()
    #Case when we are working with ouside module dependencies        
    else:
#        path = PathChecker()
#        directory = path.path4module(arg, ROOT_SOURCES)

        with open(module_file_path + "/" + arg2 + "/module.yml") as manifest_file:
            manifest_file_read = manifest_file.read()
            name = rule_name.findall(manifest_file_read)
            deps = rule_deps.findall(manifest_file_read)
            manifest_file.close()

    parc_name = [x.lstrip(' name: ') for x in name]
    parc_dep = [x.lstrip(' deps: ') for x in deps]

    for i in range(len(parc_name)):
        if '"' in parc_name[i]:
            parc_name[i] = parc_name[i].replace('"', '')

    global deplist
    #Adding multiple or single dependency to deplist
    for i in range(len(parc_dep)):
        if ";" in parc_dep[i]:
            z = parc_dep[i].split(";")
            deplist.append(z)
        else:
            deplist.append(parc_dep[i])
    
    #Remove default present deps
    for i in range(len(deplist)):
        if isinstance(deplist[i], str):
            if deplist[i] == "Core" or "RIO":
                if deplist[i] != "MathCore":
                    deplist[i] = deplist[i].replace("Core", "")
                    deplist[i] = deplist[i].replace("RIO", "")
                    deplist[i] = deplist[i].replace("Imt", "")  
        elif isinstance(deplist[i], list):
            for j in range(len(deplist[i])):
                if deplist[i][j] == "Core" or "RIO":
                    if deplist[i][j] != "MathCore":
                        deplist[i][j] = deplist[i][j].replace("Core", "")
                        deplist[i][j] = deplist[i][j].replace("RIO", "")
                        deplist[i][j] = deplist[i][j].replace("Imt", "") 

    for item in deplist:
        if isinstance(item, list):
            for j in item:
                if '' in item:
                    item.remove('')
    
    global namelist
    #For package module names start at index 3 in parc_name list
    if count == 1:
        for i in range(3, len(parc_name)):
            if parc_name[i] not in namelist:
                namelist.append(parc_name[i])
    #For modules just add the name
    else:
        for i in range(len(parc_name)):
            if parc_name[i] not in namelist:
                namelist.append(parc_name[i])
    
    global nodes_set
    global nodes_set2

    #Add namelist to set
    for i in range(len(namelist)):
        nodes_set.add(namelist[i])

    #Add deplist entities to set
    for item in deplist:
        if isinstance(item, str):
            nodes_set.add(item)
        elif isinstance(item, list):
            for val in item:
                nodes_set.add(val)
    
    #remove null values from set
    if '' in nodes_set:
        nodes_set.remove('')

# check if "name" or name is to be checked now and 
# proceed accordingly
    
    with open(manifest_dir + "/" + arg1 + ".yml") as manif_file:
        mread = manif_file.read()
    for node in nodes_set.copy():
        module = node
            #check if entity is present as module name 
            # that is with "" around the name.
        module = '"' + module + '"'
            #if not -> its a module outside the package,
            # get its path 
        if module not in mread:
            if module not in nodes_set2:
                #path = PathChecker()
                #directory = path.path4module(str(i), ROOT_SOURCES)
                with open(module_file_path + "/" + node + "/module.yml") as md:
                    md_read = md.read()
                    name = rule_name.findall(md_read)
                    parc_name = [x.lstrip(' name: ') for x in name]
                nodes_set2.add(module)
                #handling module cases
                getdag(arg1, parc_name[0])

#Case 1 -> main package
getdag('MATH', '')

def grp():
    graph_dict = {}

    Directed_Graph = nx.DiGraph()

    for i in range(len(namelist)):
        graph_dict[namelist[i]] = deplist[i]

    for item in nodes_set:
        dg.add_node_if_not_exists(item)
        #G.add_node(item)

    for key, value in graph_dict.items():
        if isinstance(value, list):
            for val in value:
                if val != '':
                    dg.add_edge(str(key), str(val))
                    Directed_Graph.add_weighted_edges_from([(str(key), str(val), 1)])
        elif isinstance(value, str):
            if value != '':
                dg.add_edge(str(key), str(value))
                Directed_Graph.add_weighted_edges_from([(str(key), str(value), 1)])

    nx.draw(Directed_Graph, with_labels=True, font_weight='bold')

    print("Topologically sorted dependency sequence : ")
    print(dg.topological_sort())

grp()
plt.show() 
#FIXME : save file as pdf or png
#pylab.savefig('n1.png')

#pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
#fig1 = plt.figure()
#fig1.savefig('fig1.png')
#pdf.close()