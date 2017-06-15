from collections import defaultdict


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


        #self.test[]


    def get_vertices_and_edges_at_viewport(self, view_port = [0, 0, 0, 0]):
        pass


    def verticeIsInViewPort(self, verticeCoor = [0, 0], view_port = [0, 0, 0, 0]):
        return True

    def verticeToNode(self, verticeId):
        pass

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
