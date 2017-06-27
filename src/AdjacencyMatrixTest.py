import datetime
import numpy as np
import heapq


import  csv
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


class PathRetriever():
    def __init__(self, pathToBundledVertices='./DataFiles/output_verticesWiki.txt',
                 pathToBundledEdges='./DataFiles/output_edgesWiki.txt',
                 pathToOriginalVertices='./DataFiles/Original Vertices.txt',
                 pathToOriginalEdges='./DataFiles/OriginalEdges.txt',
                 pathToSemanticTree='./DataFiles/NewSemanticTree.txt',
                 pathToZPop = './DataFiles/zpop.tsv'):

        self.bundledVertices = {}
        with open(pathToBundledVertices, 'r') as ptbv:
            for line in ptbv:
                lst = line.split()
                self.bundledVertices[lst[0]] = lst[1:]

        self.articlesZpop = {}
        with open(pathToZPop, "r") as zpop:
            for line in zpop:
                lst = line.split()
                self.articlesZpop[lst[0]] = lst[1]

        self.originalVertices = {}
        with open(pathToOriginalVertices) as ptov:
            for line in ptov:
                lst = line.split()
                if len(lst) == 1: continue
                self.originalVertices[lst[0]] = lst[1:]
        self.edgeDictionary, self.inboundPaths, self.outboundPaths = self.__getEdgeDictionaries(pathToSemanticTree)
        self.edgeMax = self.getMaxWeight(pathToBundledEdges)

        self.bundledEdges = {}
        with open(pathToBundledEdges) as pte:
            for line in pte:
                lst = line.split()
                self.bundledEdges[(lst[0], lst[1])] = lst[2]

    def __getEdgeDictionaries(self, pathToSemanticTree):
        outboundPaths = {}
        edgeDictionary = {}
        # inboundPaths is a dictionary where the key is a vertex and the values are an array which is composed of all the
        #  values which have roads going into the key value. This is the reverse of outboundPaths where the key has outbound
        #  roads to the values
        inboundPaths = {}
        print("Making the three dictionaries now!")
        with open(pathToSemanticTree,'r') as dictFormingSemanticTree:
            for line in dictFormingSemanticTree:
                elements = line.split(" ")
                edgeDictionary[elements[0]] = elements[1:]  # Edge ID as key,  [src, dest, parent, weight] as vals
                # if both src and dst are in orig Vertices:
                if (elements[1] in self.originalVertices and elements[2] in self.originalVertices):  # elements = [edgeId, src, dst, parent, weight]
                    #       pairings.append((elements[1], elements[2]))
                    if len(elements) == 4:  # here there's EdgeID, src, dest, weight, here we ARE at the parent
                        if elements[1] in outboundPaths:
                            outboundPaths[elements[1]].update({elements[2]: [elements[0], elements[3]]})
                        else:
                            outboundPaths[elements[1]] = {elements[2]: [elements[0], elements[3]]}
                        if elements[2] in inboundPaths:
                            inboundPaths[elements[2]].update({elements[1]: [elements[0], elements[3]]})
                        else:
                            inboundPaths[elements[2]] = {elements[1]: [elements[0], elements[3]]}
                    elif len(
                            elements) == 5:  # here we are still at a child and have to append the parent. format: Src key -> dest Key -> [EdgeId, Weight, Parent if exists], if path[src][dest].size = 3, we gotta keep going, if =2, we at end
                        if elements[1] in outboundPaths:
                            outboundPaths[elements[1]].update({elements[2]: [elements[0], elements[4], elements[3]]})
                        else:
                            outboundPaths[elements[1]] = {elements[2]: [elements[0], elements[4], elements[3]]}
                        if elements[2] in inboundPaths:
                            inboundPaths[elements[2]].update({elements[1]: [elements[0], elements[4], elements[3]]})
                        else:
                            inboundPaths[elements[2]] = {elements[1]: [elements[0], elements[4], elements[3]]}
        return edgeDictionary, inboundPaths, outboundPaths

    def getMaxWeight(self, pathToBundledEdges):
        maxWeight = 1
        with open(pathToBundledEdges, 'r') as edges:
            for edge in edges:
                a,b,c = edge.split(" ")
                if int(c) > maxWeight:
                    maxWeight = c
        return maxWeight

    def getPath(self, childEdgeId, edgeDict, frontStack = [], backStack = []):
        frontStack.append(edgeDict[childEdgeId][0])
        backStack.insert(0, edgeDict[childEdgeId][1])

      #  if(edgeDict[childEdgeId][0] != edgeDict[childEdgeId][1]):
         #   frontStack.append(edgeDict[childEdgeId][0])
        #    backStack.insert(0, edgeDict[childEdgeId][1])


        if(len(edgeDict[childEdgeId]) == 4):
            #we still have parents!
            parentID = edgeDict[childEdgeId][2]
            return self.getPath(parentID, edgeDict, frontStack, backStack)
        elif(len(edgeDict[childEdgeId]) == 3):
            frontStack = frontStack + backStack
            return frontStack

    def get_n_most_prominent_cities(self, n, vertices_in_view_port):
        n_cities = PrioritySet(max_size=n)

        for vertex in vertices_in_view_port:
            z_pop_score = self.articlesZpop[vertex]
            n_cities.add(-float(z_pop_score), vertex)


        return n_cities.heap


    def edgeShouldShow(self,  src, dest, threshold = 3):
        '''
        If sum of the zpop score of the two articles is greater than a threshold the edge should not show
        :param src:
        :param dest:
        :param threshold:
        :return:
        '''
        srcZpop = float(self.articlesZpop[src])
        destZpop = float(self.articlesZpop[dest])

        if srcZpop + destZpop > threshold:
            return False
        else:
            return True

    def getPathsInViewPort(self, xmin, xmax, ymin, ymax, n_cities = 10):
        pointsinPort = []

        for point in self.originalVertices:
            if xmax > float(self.originalVertices[point][0]) > xmin and ymin < float(self.originalVertices[point][1]) < ymax:
                pointsinPort.append(point)  # points in port is an array of pointIDs which are strings.
        cities = self.get_n_most_prominent_cities(n_cities, pointsinPort)
        paths = self.getPathsForEachCity(cities, xmin, xmax, ymin, ymax )
        return paths, pointsinPort

    def getPathsForEachCity(self, citiesToShowEdges, xmin, xmax, ymin, ymax,):
        outpathsToMine = []
        inpathsToMine = []
        threshholdval = 20
        for city in citiesToShowEdges:

            if city[1] in self.outboundPaths:
                for dest in self.outboundPaths[city[1]]:
                    if self.edgeShouldShow(city[1], dest, threshold= threshholdval):
                        outpathsToMine.append(
                            (city[1], dest))  # outpaths and inpaths include points and dest of edges we want to reconstruct

            if city[1] in self.inboundPaths:
                for src in self.inboundPaths[city[1]]:

                    p = self.originalVertices[src]
                    if (xmax < float(p[0]) or float(p[0]) < xmin) or (ymin > float(p[1]) or float(p[1]) > ymax):
                      # pass
                        if self.edgeShouldShow(src, city[1], threshold= threshholdval):
                            inpathsToMine.append([src, city[1]])

        paths = []

        print("Finding paths now. Paths to do: " + str(len(inpathsToMine) + len(outpathsToMine)))
        for path in inpathsToMine:  # path[0] = src, path[1] = dest
            results = self.getPath(self.inboundPaths[path[1]][path[0]][0], self.edgeDictionary, [], [])
            paths.append(results)

            if (len(paths) % 100000 == 0):
                print(len(paths))

        for path in outpathsToMine:
            results = self.getPath(self.outboundPaths[path[0]][path[1]][0], self.edgeDictionary, [], [])
            paths.append(results)

            if len(paths) % 100000 == 0:
                print(len(paths))
        return paths




fc = FileCreator()
dimensionVal = 5
oldTime = datetime.datetime.now()
test = PathRetriever()

paths, pointsInPort = test.getPathsInViewPort(-dimensionVal, dimensionVal, -dimensionVal, dimensionVal, n_cities=2)


newtime = datetime.datetime.now()
print("Time elapsed: " + str(newtime-oldTime))
maxWeight = test.edgeMax
print maxWeight
fc.generateFilesFromSourceDest1(test.originalVertices, test.bundledVertices, paths, pointsInPort, test.bundledEdges, maxWeight)