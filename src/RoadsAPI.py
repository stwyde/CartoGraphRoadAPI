from collections import defaultdict
import numpy as np
from pprint import  pprint

class RoadLoader:

    def __init__(self, pathToBundledVertices = './DataFiles/output_verticesWiki.txt',
                 pathToBundledEdges = './DataFiles/output_edgesWiki.txt',
                 pathToOriginalVertices = './DataFiles/Original Vertices.txt',
                 pathToOriginalEdges = './DataFiles/OriginalEdges.txt',
                 pathToSemanticTree = './DataFiles/output_semanticTreeWiki.txt'):

        self.bundledVertices= {}
        with open(pathToBundledVertices) as ptbv:
            for line in ptbv:
                lst = line.split()
                self.bundledVertices[lst[0]] = lst[1:]

        self.bundledEdges = defaultdict(list)
        with open(pathToBundledEdges) as pte:
            for line in pte:
                lst = line.split()
                self.bundledEdges[lst[0]].append(lst[1:])

        self.originalVertices = {}
        with open(pathToOriginalVertices) as ptov:
            for line in ptov:
                lst = line.split()
                if len(lst) == 1: continue
                self.originalVertices[lst[0]] = lst[1:]

        self.inBoundEdges = defaultdict(list)
        self.outBoundEdges = defaultdict(list)
        with open(pathToOriginalEdges) as ptoe:
            for line in ptoe:
                lst = line.split()
                if len(lst) == 1: continue
                self.inBoundEdges[lst[0]].append(lst[1])
                self.outBoundEdges[lst[1]].append(lst[0])
        self.edgesSemanticTree = {}

        if pathToSemanticTree:
            with open(pathToSemanticTree) as ptst:
                for line in ptst:
                    lst = line.split()
                    self.edgesSemanticTree[lst[0]] = lst[1:]





    def get_vertices_and_edges_at_viewport(self, view_port = [0, 0, 0, 0]):
        vertices = self.originalVertices.keys()
        verticesInViewPort = {}
        other = {}
        for vertex in vertices:
            vertexInfo = self.originalVertices[vertex]

            if(self.__verticeIsInViewPort([float(vertexInfo[0]), float(vertexInfo[1])], view_port)):
                verticesInViewPort[vertex] = vertexInfo

        return verticesInViewPort, other



    def __verticeIsInViewPort(self, vertexCoor, view_port = [0, 0, 0, 0]):
        xmin = view_port[0]
        xmax = view_port[2]
        ymin = view_port[1]
        ymax = view_port[3]

        if xmax > float(vertexCoor[0]) > xmin and ymin < float(vertexCoor[1]) < ymax:
            return True
        else:
            return False






#cTests = RoadLoader(pathToBundledVertices='./DataFiles/TestFiles/philippines/outputvertices.txt',
#                    pathToBundledEdges='./DataFiles/TestFiles/philippines/outputEdges.txt',
#                    pathToOriginalVertices='./DataFiles/TestFiles/philippines/philippines_list_vertices.txt',
#                   pathToOriginalEdges='./DataFiles/TestFiles/philippines/philippines_list_edges.txt',
#                    pathToSemanticTree='./DataFiles/TestFiles/philippines/semantic_edges.txt')
cTests = RoadLoader()
ov = cTests.originalVertices.keys()
bv = cTests.bundledVertices.keys()

#oe = cTests.originalEdges.keys()
be = cTests.bundledEdges.keys()

st = cTests.edgesSemanticTree.keys()

#print(cTests.originalVertices[ov[11]], cTests.bundledVertices[bv[11]], oe[1], cTests.bundledEdges[be[11]], cTests.edgesSemanticTree[st[11]])

veInViewPort = cTests.get_vertices_and_edges_at_viewport([-20, -20, 20, 20])
