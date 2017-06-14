import csv
class RoadLoader:

    def __init__(self, pathToBundledVertices = './DataFiles/output_verticesWiki.txt',
                 pathToEdges = './DataFiles/output_edgesWiki.txt',
                 pathToOriginalVertices = './DataFiles/Original Vertices.txt'):
        self.bundledVertices= []
        with open(pathToBundledVertices) as ptbv: #this seem like bad way to do this
            for line in ptbv:
                self.bundledVertices.append(line.split())
        self.bundledEdges = []
        with open(pathToEdges) as pte:
            for line in pte:
                self.bundledEdges.append(line.split())
        self.originalVertices = []
        with open(pathToOriginalVertices) as ptov:
            for line in ptov:
                lst  = line.split()
                if len(lst) == 1: continue
                self.originalVertices.append(lst)



    def get_vertices_and_edges_at_viewport(self, view_port = [0, 0, 0, 0]):

        pass

cTests = RoadLoader()
print(cTests.originalVertices[:10])
