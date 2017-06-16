origVert = open("../DataFiles/TestFiles/whiteboard/textNodes.txt", "r")
origEdges = open("../DataFiles/TestFiles/whiteboard/textEdges.txt", "r")
newVerts = open("../DataFiles/TestFiles/whiteboard/output_verticesTest.txt", "r")
newEdges = open("../DataFiles/TestFiles/whiteboard/output_edgesTest.txt", "r")
semanticTree = open("../DataFiles/TestFiles/whiteboard/output_edgesTest.txt", "r")

origVert = [x.rstrip() for x in origVert]
origEdges = [x.rstrip() for x in origEdges]
newVerts = [x.rstrip() for x in newVerts]
newEdges = [x.rstrip() for x in newEdges]
semanticTree = [x.rstrip() for x in semanticTree]

del(origVert[0])
vertices = {}
for line in origVert:
    a,b,c = line.split(" ")
    vertices[a] = (b,c)
newVertices = {}
for line in newVerts:
    a,b,c = line.split(" ")
    newVertices[a] = (b,c)

del(origEdges[0])
pairings = []
for line in origEdges:
    a,b = line.split(" ")
    pairings.append((a,b))
    print(a + " " + b)