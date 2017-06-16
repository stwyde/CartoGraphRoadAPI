origVert = open("../DataFiles/TestFiles/philippines/philippines_list_vertices.txt", "r")
origEdges = open("../DataFiles/TestFiles/philippines/philippines_list_edges.txt", "r")
newVerts = open("../DataFiles/TestFiles/philippines/outputvertices.txt", "r")
newEdges = open("../DataFiles/TestFiles/philippines/outputEdges.txt", "r")
semanticTree = open("../DataFiles/TestFiles/philippines/semantic_edges.txt", "r")

def hunt(childEdgeId, frontStack, backStack, childEdges, topParents):
    for line in childEdges:
        if childEdgeId in line[0]:
            frontStack.append(line[1])
            backStack.insert(0, line[2])
            return hunt(line[3], frontStack, backStack, childEdges, topParents)
    for line in topParents:
        if childEdgeId in line[0]:
            frontStack.append(line[1])
            backStack.insert(0, line[2])
            #merges front and back stacks
            for node in backStack:
                frontStack.append(node)
            return frontStack


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

#Now work on pathing!
topParents = []
childEdges = []
for line in semanticTree:
     line2 = line
     splitLine = line2.split(" ")
     if len(splitLine) == 4:
         childEdges.append(splitLine)
     elif len(splitLine) == 3:
         topParents.append(splitLine)
     else:
         print("ERROR, SEMANTIC TREE CONTAINS IMPROPERLY FORMATTED OBJECT")

paths = {}
for pairing in pairings:
    frontStack = [pairing[0]]
    backStack = [pairing[1]]
    lastEdge = "hehe xD"
    for entry in childEdges:
        if pairing[0] in entry[1] and pairing[1] in entry[2]:
            #removes line to make future pathing easier. This only happens for the initial unbundled edge so it should be okay, especially since the relationship is secured in inputEdges
            childEdges.remove(entry)
            finalPath = hunt(entry[3], frontStack, backStack, childEdges, topParents)
            paths[pairing] = finalPath
            break
