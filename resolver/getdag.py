import re
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import logging
import pylab
from dag4pkg import *

dag = Dag4pkg()
deplist = []
namelist = []
nodes_set = set()
nodes_set_two = set()

def visual_dag(arg1, arg2):
    """Function to get dag as a graphical output"""

    global deplist, namelist
    global nodes_set, nodes_set_two

    #regular expression to extract data
    rule_name = re.compile(".*name:.*")
    rule_deps = re.compile(".*deps:.*")

    #Set local variables for root source files and manifest files
    module_file_path = os.environ["ROOT_MANIFESTS"]

    #Initial case for package manifest file
    if arg2 == '':
        with open(module_file_path + "/" + arg1 + ".yml") as manifest_file:
            manifest_file_read = manifest_file.read()
            name = rule_name.findall(manifest_file_read)
            deps = rule_deps.findall(manifest_file_read)
            manifest_file.close()

    #Case when we are working with ouside module dependencies        
    else:
        with open(module_file_path + "/" + arg2 + "/module.yml") as manifest_file:
            manifest_file_read = manifest_file.read()
            name = rule_name.findall(manifest_file_read)
            deps = rule_deps.findall(manifest_file_read)
            manifest_file.close()

    #variables to get the data from lists
    parc_name = [x.lstrip(' name: ') for x in name]
    parc_dep = [x.lstrip(' deps: ') for x in deps]

    #Cleaning up the variable for parsing usage
    for name_value in range(len(parc_name)):
        if '"' in parc_name[name_value]:
            parc_name[name_value] = parc_name[name_value].replace('"', '')

    #Separate variables present together in manifest
    for dep_value in range(len(parc_dep)):
        if ";" in parc_dep[dep_value]:
            z = parc_dep[dep_value].split(";")
            deplist.append(z)
        else:
            deplist.append(parc_dep[dep_value])

    #Remove default present deps
    #Special check for MathCore as Core considers MathCore also
    for dep_val in range(len(deplist)):
        if isinstance(deplist[dep_val], str):
            if deplist[dep_val] == "Core" or "RIO":
                if deplist[dep_val] != "MathCore":
                    deplist[dep_val] = deplist[dep_val].replace("Core", "")
                    deplist[dep_val] = deplist[dep_val].replace("RIO", "")
                    deplist[dep_val] = deplist[dep_val].replace("Imt", "")
        elif isinstance(deplist[dep_val], list):
            for list_val in range(len(deplist[dep_val])):
                if deplist[dep_val][list_val] == "Core" or "RIO":
                    if deplist[dep_val][list_val] != "MathCore":
                        deplist[dep_val][list_val] = deplist[dep_val][list_val].replace("Core", "")
                        deplist[dep_val][list_val] = deplist[dep_val][list_val].replace("RIO", "")
                        deplist[dep_val][list_val] = deplist[dep_val][list_val].replace("Imt", "")

    #If empty item in the list, remove it
    for dependency in deplist:
        if isinstance(dependency, list):
            if '' in dependency:
                dependency.remove('')

    #For package module names
    if arg2 == '':
        for name_value in range(3, len(parc_name)):
            if parc_name[name_value] not in namelist:
                namelist.append(parc_name[name_value])

    #For modules just add the name
    else:
        for name_value in range(len(parc_name)):
            if parc_name[name_value] not in namelist:
                namelist.append(parc_name[name_value])

    #Add namelist to set
    for mod_name in range(len(namelist)):
        nodes_set.add(namelist[mod_name])

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

    # module names are within '"'
    with open(module_file_path + "/" + arg1 + ".yml") as manif_file:
        mread = manif_file.read()
    for node in nodes_set.copy():
        module = node
        module = '"' + module + '"'

        #module outside package
        if module not in mread:
            if module not in nodes_set_two:
                with open(module_file_path + "/" + node + "/module.yml") as md:
                    md_read = md.read()
                    name = rule_name.findall(md_read)
                    parc_name = [x.lstrip(' name: ') for x in name]
                nodes_set_two.add(module)
                #handling module cases
                visual_dag(arg1, parc_name[0])

arg1 = sys.argv[1]
visual_dag(arg1, '')

def sorted_graph():
    """Function to create and print graph"""

    graph_dict = {}

    Directed_Graph = nx.DiGraph()

    for name in range(len(namelist)):
        graph_dict[namelist[name]] = deplist[name]

    for item in nodes_set:
        dag.add_node_if_not_exists(item)

    for key, value in graph_dict.items():
        if isinstance(value, list):
            for val in value:
                if val != '':
                    dag.add_edge(str(key), str(val))
                    Directed_Graph.add_weighted_edges_from([(str(key), str(val), 1)])
        elif isinstance(value, str):
            if value != '':
                dag.add_edge(str(key), str(value))
                Directed_Graph.add_weighted_edges_from([(str(key), str(value), 1)])

    nx.draw(Directed_Graph, with_labels=True, font_weight='bold')

    print("Topologically sorted dependency sequence : ")
    print(dag.topological_sort())

sorted_graph()

plt.savefig('graph.png')
