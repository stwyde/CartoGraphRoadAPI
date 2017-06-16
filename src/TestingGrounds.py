origVert = open("../simpleData/Original Vertices.txt", "r")
origEdges = open("../simpleData/WikiEdgesInput.txt", "r")
newVerts = open("../simpleData/output_verticesWiki.txt", "r")
newEdges = open("../simpleData/output_edgesWiki.txt", "r")
semanticTree = open("../simpleData/output_semanticTreeWiki.txt", "r")

def hunt(childEdgeId, frontStack, backStack, childEdges, topParents):
    if childEdgeId in childEdges:
        frontStack.append(childEdges[childEdgeId][0])
        backStack.insert(0, childEdges[childEdgeId][1])
        newChildEdge = childEdges[childEdgeId][2]
        print(newChildEdge)
        return hunt(newChildEdge, frontStack, backStack, childEdges, topParents)

    elif childEdgeId in topParents:
        frontStack.append(topParents[childEdgeId][0])
        backStack.insert(0,topParents[childEdgeId][1])
        #merges front and back stacks
        for node in backStack:
            frontStack.append(node)
        return frontStack

def hunt2(childEdgeId, frontStack, backStack, childEdges, topParents):
    foundParent = False
    while(foundParent == False):
        if(childEdgeId in childEdges):
            line = childEdges[childEdgeId]
            frontStack.append(line[0])
            backStack.insert(0, line[1])
            childEdgeId = line[3]
            print(frontStack)

        elif(childEdgeId in topParents):
            line = topParents[childEdgeId]
            frontStack.append(line[0])
            backStack.insert(0, line[1])
            #merges front and back stacks
            for node in backStack:
                frontStack.append(node)
            foundParent = True
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

#Now work on pathing! Commented version implements array of lines, current version uses a dict for semantic tree
# topParents = []
# childEdges = []
# for line in semanticTree:
#      line2 = line
#      splitLine = line2.split(" ")
#      if len(splitLine) == 4:
#          childEdges.append(splitLine)
#      elif len(splitLine) == 3:
#          topParents.append(splitLine)
#      else:
#          print("ERROR, SEMANTIC TREE CONTAINS IMPROPERLY FORMATTED OBJECT")
topParents = {}
childEdges = {}
for line in semanticTree:
     line2 = line
     splitLine = line2.split(" ")
     if len(splitLine) == 4:
         childEdges[splitLine[0]] = splitLine[1:] #Edge ID as key, nodes src dest and parent Edge as vals
     elif len(splitLine) == 3:
         topParents[splitLine[0]] = splitLine[1:] #Edge ID as key, nodes src and dest as vals
     else:
         print("ERROR, SEMANTIC TREE CONTAINS IMPROPERLY FORMATTED OBJECT")

print("Done setting up stuff, now pairing and pathing")

paths = {}
#for pairing in pairings:
pairing = pairings.pop()
frontStack = [pairing[0]]
backStack = [pairing[1]]
lastEdge = "hehe xD" #what's this for again?
for entry in childEdges:
    if pairing[0] in childEdges[entry][0] and pairing[1] in childEdges[entry][1]:
        print(lastEdge)
        #removes line to make future pathing easier. This only happens for the initial unbundled edge so it should be okay, especially since the relationship is secured in inputEdges
        #childEdges.remove(entry)
        print entry
        print childEdges[entry][2]
        finalPath = hunt(childEdges[entry][2], frontStack, backStack, childEdges, topParents)
        paths[pairing] = finalPath
        print(paths[pairing])
        break
