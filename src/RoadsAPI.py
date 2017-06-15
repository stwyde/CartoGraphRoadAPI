from collections import defaultdict
import numpy as np
from pprint import  pprint

class RoadLoader:

    def __init__(self, pathToBundledVertices = './DataFiles/output_verticesWiki.txt',
                 pathToBundledEdges = './DataFiles/output_edgesWiki.txt',
                 pathToOriginalVertices = './DataFiles/Original Vertices.txt',
                 pathToOriginalEdges = './DataFiles/OriginalEdges.txt',
                 pathToSemanticTree = None):

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
                lst  = line.split()
                if len(lst) == 1: continue
                self.originalVertices[lst[0]] = lst[1:]

        self.originalEdges = defaultdict(list)
        with open(pathToOriginalEdges) as ptoe:
            for line in ptoe:
                lst = line.split()
                if len(lst) == 1: continue
                self.originalEdges[(lst[0], lst[1])]
        self.edgesSemanticTree = {}
        if pathToSemanticTree:
            with open(pathToSemanticTree) as ptst:
                for line in ptst:
                    lst = line.split()
                    self.edgesSemanticTree[lst[0]] = lst[1:]





    def get_vertices_and_edges_at_viewport(self, view_port = [0, 0, 0, 0]):
        vertices = self.originalVertices.keys()
        verticesInViewPort = {}
        for vertex in vertices:
            vertexInfo = self.originalVertices[vertex]

            if(self.verticeIsInViewPort([float(vertexInfo[0]), float(vertexInfo[1])], view_port)):
                verticesInViewPort[vertex] = vertexInfo

        return verticesInViewPort


    def verticeIsInViewPort(self, verticeCoor = [0.0, 0.0], view_port = [0.0, 0.0, 0.0, 0.0]):

        '''
        Formula taken from "https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not"
        :param verticeCoor:
        :param view_port: view_port given as a list where [x-min, y-min, x-max, y-max]
        :return:
        '''

        ab = self.findABvector((view_port[0], view_port[3]), (view_port[0], view_port[1])) #(x-min, y-max), (x-min, y-min)
        am = self.findABvector((view_port[0], view_port[3]), verticeCoor) #(x-min, y-max), (verticeCoor)
        bc = self.findABvector((view_port[0], view_port[1]), (view_port[2], view_port[1]))#(x-min, y-min) and (x-max, y-min)
        bm = self.findABvector((view_port[0], view_port[1]), verticeCoor)#(x-min, y-min), (verticeCoor)

        first = 0 <= np.dot(ab, am)
        second = np.dot(ab, am) <= np.dot(ab, ab)

        third = 0 <= np.dot(bc, bm)
        forth = np.dot(bc, bm) <= np.dot(bc, bc)





        return first and second and third and forth

    def verticeToNode(self, verticeId):
        pass

    def findABvector(self, A, B):
        return (A[0] - B[0], A[1] - B[1])

   # def



cTests = RoadLoader(pathToBundledVertices='./DataFiles/TestFiles/outputvertices.txt',
                    pathToBundledEdges='./DataFiles/TestFiles/outputEdges.txt',
                    pathToOriginalVertices='./DataFiles/TestFiles/philippines_list_vertices.txt',
                    pathToOriginalEdges='./DataFiles/TestFiles/philippines_list_edges.txt',
                    pathToSemanticTree='./DataFiles/TestFiles/semantic_edges.txt')
ov = cTests.originalVertices.keys()
bv = cTests.bundledVertices.keys()

oe = cTests.originalEdges.keys()
be = cTests.bundledEdges.keys()

st = cTests.edgesSemanticTree.keys()

print(cTests.originalVertices[ov[11]], cTests.bundledVertices[bv[11]], oe[1], cTests.bundledEdges[be[11]], cTests.edgesSemanticTree[st[11]])

veInViewPort = cTests.get_vertices_and_edges_at_viewport([100, -1, 600, -600])
pprint(veInViewPort)

def isInsideRec(M):
    A = (5,0)
    B = (0,2)
    C = (1,5)
    D = (6,3)



    AB = (A[0] - B[0], A[1]-B[1])
    AM = (A[0] - M[0], A[1]-M[1])

    BC = (B[0] - C[0], B[1]-C[1])
    BM = (B[0] - M[0], B[1] - M[1])

    first = 0 <= np.dot(AB, AM)
    second = np.dot(AB, AM) <= np.dot(AB, AB)

    third  = 0 <= np.dot(BC, BM)
    forth = np.dot(BC, BM) <= np.dot(BC, BC)


    print(first, second, third, forth)

#isInsideRec((6,1))

