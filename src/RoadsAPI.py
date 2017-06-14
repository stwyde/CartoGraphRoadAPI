from collections import defaultdict


class RoadLoader:

    def __init__(self, pathToBundledVertices = './DataFiles/output_verticesWiki.txt',
                 pathToEdges = './DataFiles/output_edgesWiki.txt',
                 pathToOriginalVertices = './DataFiles/Original Vertices.txt',
                 pathToOriginalEdges = './DataFiles/OriginalEdges.txt'):

        self.bundledVertices= {}
        with open(pathToBundledVertices) as ptbv: #this seem like bad way to do this
            for line in ptbv:
                lst = line.split()
                self.bundledVertices[lst[0]] = lst[1:]

        self.bundledEdges = defaultdict(list)
        with open(pathToEdges) as pte:
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
                self.originalEdges[lst[0]].append(lst[1:])


    def get_vertices_and_edges_at_viewport(self, view_port = [0, 0, 0, 0]):

        pass


    def verticeIsInViewPort(self, edgeCoor = [0, 0], view_port = [0, 0, 0, 0]):
        return True



cTests = RoadLoader()
ov = cTests.originalVertices.keys()
bv = cTests.bundledVertices.keys()

oe = cTests.originalEdges.keys()
be = cTests.bundledEdges.keys()

print(cTests.originalVertices[ov[11]], cTests.bundledVertices[bv[11]], cTests.originalEdges[oe[11]], cTests.bundledEdges[be[11]])
