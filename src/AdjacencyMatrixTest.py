import datetime
import numpy as np
import heapq
semanticTree = open('../simpleData/NewSemanticTree.txt', "r")
origVert = open('../simpleData/OriginalVertices.txt', "r")
import csv
from FileCreatorForTestViz import FileCreator


class PrioritySet(object):
    def __init__(self, max_size = 10):
        self.heap = []
        self.set = set()
        self.max_size = max_size


    def add(self,  pri, d):
        if not d in self.set:

            heapq.heappush(self.heap, (pri, d))
            self.set.add(d)
            if len(self.heap) > self.max_size:
                self.pop()

    def pop(self):
        pri, d = heapq.heappop(self.heap)
        self.set.remove(d)
        return d

    def add_all(self, list_to_add):
        for ele in list_to_add:
            self.add(ele[0], ele[1])

    def __str__(self):
        return str(self.heap)

def getPath(childEdgeId, edgeDict, frontStack = [], backStack = [], pathEdgeId= []):

    frontStack.append(edgeDict[childEdgeId][0])
    if(edgeDict[childEdgeId][0] != edgeDict[childEdgeId][1]):
        backStack.insert(0, edgeDict[childEdgeId][1])
        pathEdgeId.append((edgeDict[childEdgeId][-1], (edgeDict[childEdgeId][0], edgeDict[childEdgeId][1])))

    if(len(edgeDict[childEdgeId]) == 4):
        #we still have parents!
        parentID = edgeDict[childEdgeId][2]
        return getPath(parentID, edgeDict, frontStack, backStack, pathEdgeId)
    elif(len(edgeDict[childEdgeId]) == 3):
        frontStack = frontStack + backStack
        return frontStack, pathEdgeId


def getViewPortPaths(xmin, xmax, ymin, ymax, vertices, outboundPaths, inboundPaths, edgeDict, n_cities=10):
    pointsinPort = []
    outpathsToMine = []
    inpathsToMine = []
    for point in vertices:
        if xmax > float(vertices[point][0]) > xmin and ymin < float(vertices[point][1]) < ymax:
            pointsinPort.append(point) #points in port is an array of pointIDs which are strings.
    citiesToShowEdges = get_n_most_prominent_cities(n_cities, pointsinPort, articlesZpop)
    print("cities", citiesToShowEdges)
    for city in citiesToShowEdges:
            try:
               for dest in outboundPaths[city[1]]:
                  outpathsToMine.append((city[1], dest)) #outpaths and inpaths include points and dest of edges we want to reconstruct
            except KeyError:
               pass
            try:
                for src in inboundPaths[city[1]]:
                    p = vertices[src]
                    if (xmax < float(p[0]) or float(p[0]) < xmin) or (ymin > float(p[1]) or float(p[1]) > ymax):
                        inpathsToMine.append([src, city[1]])
            except KeyError:
                pass

    paths = []
    pathsEdgeId = []
    print("Finding paths now. Paths to do: " + str(len(inpathsToMine) +len(outpathsToMine)))
    for path in inpathsToMine: #path[0] = src, path[1] = dest
        results = getPath(inboundPaths[path[1]][path[0]][0], edgeDict,[], [], [])
        paths.append(results[0])
        pathsEdgeId += results[1]

        if(len(paths) % 100000 == 0):
            print(len(paths))

    for path in outpathsToMine:
        results = getPath(outboundPaths[path[0]][path[1]][0], edgeDict, [], [], [])
        paths.append(results[0])
        #pathsEdgeId.append(results[1])
        pathsEdgeId += results[1]

        if len(paths) % 100000 == 0:
            print(len(paths))
            print(pathsEdgeId)

    return paths, pathsEdgeId, pointsinPort

def get_n_most_prominent_cities(n, vertices_in_view_port, articleZpopDict):
    n_cities = PrioritySet(max_size=n)
    print("n_of_vertex", len(vertices_in_view_port))
    counter = 0
    for vertex in vertices_in_view_port:
        z_pop_score = (articleZpopDict[vertex])
        n_cities.add(1/(float(z_pop_score)+1), vertex)
        counter += 1
        if counter % 10000 == 0:
            print("counter ", counter)

    return n_cities.heap


oldTime = datetime.datetime.now()

origVert = [x.rstrip() for x in origVert]
semanticTree = [x.rstrip() for x in semanticTree]
dictFormingSemanticTree = semanticTree

bundledVertices= {}
with open('../simpleData/output_verticesWiki.txt') as ptbv:
    for line in ptbv:
        lst = line.split()
        bundledVertices[lst[0]] = lst[1:]
articlesZpop = {}
with open('../simpleData/zpop.tsv', "r") as zpop:
    for line in zpop:
        lst = line.split()
        articlesZpop[lst[0]] = lst[1]
del(origVert[0])
vertices = {}
#Creates a dict with vertex ID as key, then x/y coordinates as values in array list.
for line in origVert:
    a,b,c = line.split(" ")
    vertices[a] = [b,c]


outboundPaths = {}
edgeDictionary = {}
#inboundPaths is a dictinary where the key is a vertex and the values are an array which is composed of all the values which have roads going into the key value. This is the reverse of outboundPaths where the key has outbound roads to the values
inboundPaths = {}
pairings = []
print("Making the three dictionaries now!")
for line in dictFormingSemanticTree:
    elements = line.split(" ")
    edgeDictionary[elements[0]] = elements[1:] #Edge ID as key,  [src, dest, parent, weight] as vals
    #if both src and dst are in orig Vertices:
    if(elements[1] in vertices and elements[2] in vertices): #elements = [edgeId, src, dst, parent, weight]
        pairings.append((elements[1], elements[2]))
        if len(elements) == 4: #here there's EdgeID, src, dest, weight, here we ARE at the parent
            if elements[1] in outboundPaths:
                outboundPaths[elements[1]].update({elements[2]: [elements[0], elements[3]]})
            else:
                outboundPaths[elements[1]] = {elements[2]: [elements[0], elements[3]]}
            if elements[2] in inboundPaths:
                inboundPaths[elements[2]].update({elements[1]:[elements[0], elements[3]]})
            else:
                inboundPaths[elements[2]] = {elements[1]:[elements[0], elements[3]]}
        elif len(elements) == 5: #here we are still at a child and have to append the parent. format: Src key -> dest Key -> [EdgeId, Weight, Parent if exists], if path[src][dest].size = 3, we gotta keep going, if =2, we at end
            if elements[1] in outboundPaths:
                outboundPaths[elements[1]].update({elements[2]: [elements[0], elements[4], elements[3]]})
            else:
                outboundPaths[elements[1]] = {elements[2]: [elements[0], elements[4], elements[3]]}
            if elements[2] in inboundPaths:
                inboundPaths[elements[2]].update({elements[1]: [elements[0], elements[4], elements[3]]})
            else:
                inboundPaths[elements[2]] = {elements[1]: [elements[0], elements[4], elements[3]]}


print("Done setting up stuff, now pairing and pathing")
dimensionVal = 40
paths, pathsEdgeId, pointsInPort = (getViewPortPaths(-dimensionVal, dimensionVal, -dimensionVal, dimensionVal, vertices, outboundPaths,inboundPaths, edgeDictionary, n_cities=1))
print(len(paths))
print("All roads generated. Have a great day! (hehe xd)")
print("pathsEdge", str(pathsEdgeId))
newtime = datetime.datetime.now()
print("Time elapsed: " + str(newtime-oldTime))
#New implementation preferred: dict[src:dict[dest:[edgeId, weight, ParentID]]] BUT how do we find inbound edges quickly? do we make a reversed one?


fc = FileCreator()

#fc.generateFilesFromSourceDest(pathsEdgeId, vertices, bundledVertices)
fc.generateFilesFromSourceDest1(vertices,bundledVertices, paths)