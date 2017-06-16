origVert = open("../simpleData/Original Vertices.txt", "r")
origEdges = open("../simpleData/WikiEdgesInput.txt", "r")
newVerts = open("../simpleData/output_verticesWiki.txt", "r")
newEdges = open("../simpleData/output_edgesWiki.txt", "r")
semanticTree = open("../simpleData/output_semanticTreeWiki.txt", "r")

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

def hunt2(childEdgeId, frontStack, backStack, childEdges, topParents):
    foundParent = False
    while(foundParent == False):
        haschildParent = False
        for line in childEdges:
            if childEdgeId in line[0]:
                frontStack.append(line[1])
                backStack.insert(0, line[2])
                childEdgeId = line[3]
                haschildParent = True
                break
        if(haschildParent == False):
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
print("Done setting up stuff, now pairing and pathing")
paths = {}
for pairing in pairings:
    frontStack = [pairing[0]]
    backStack = [pairing[1]]
    lastEdge = "hehe xD"
    for entry in childEdges:
        if pairing[0] in entry[1] and pairing[1] in entry[2]:
            #removes line to make future pathing easier. This only happens for the initial unbundled edge so it should be okay, especially since the relationship is secured in inputEdges
            childEdges.remove(entry)
            finalPath = hunt2(entry[3], frontStack, backStack, childEdges, topParents)
            paths[pairing] = finalPath
            print(paths[pairing])
            break
