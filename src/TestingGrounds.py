origVert = open("../simpleData/Original Vertices.txt", "r")
origEdges = open("../simpleData/WikiEdgesInput.txt", "r")
newVerts = open("../simpleData/outputvertices.txt", "r")
newEdges = open("../simpleData/outputEdges.txt", "r")
semanticTree = open("../simpleData/semantic_edges.txt", "r")

def hunt(childEdgeId, frontStack, backStack, childEdges, topParents):
    if childEdgeId in childEdges:
        frontStack.append(childEdges[childEdgeId][0])
        backStack.insert(0, childEdges[childEdgeId][1])
        newChildEdge = childEdges[childEdgeId][2]
        #print(newChildEdge)
        return hunt(newChildEdge, frontStack, backStack, childEdges, topParents)

    elif childEdgeId in topParents:
        frontStack.append(topParents[childEdgeId][0])
        backStack.insert(0,topParents[childEdgeId][1])
        #merges front and back stacks
        for node in backStack:
            frontStack.append(node)
        return frontStack

def findPath(source, destination, childEdges, topParents):
    frontStack = [source]
    backStack = [destination]
    for entry in childEdges:
        if source in childEdges[entry][0] and destination in childEdges[entry][1]:
            return hunt(childEdges[entry][2], frontStack, backStack, childEdges, topParents)

#nonrecursive version of hunt
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

#(-7.5, -5, -7.5, -5,)

def getViewPortPaths(xmin, xmax, ymin, ymax, vertices, childEdges, topParents, outboundPaths, inboundPaths):
    pointsinPort = []
    pathsToMine = []
    for point in vertices:
        if xmax > float(vertices[point][0]) > xmin and ymin < float(vertices[point][1]) < ymax:
            pointsinPort.append(point)
            try:
                for dest in outboundPaths[point]:
                    pathsToMine.append((point, dest))
            except KeyError:
                pass
            try:
                for src in inboundPaths[point]:
                    pathsToMine.append([src, point])
            except KeyError:
                pass

    print("Points in the viewport: ")
    print(pointsinPort)
    paths = []
    print("Finding paths now. Paths to do: " + str(len(pathsToMine)))
    for path in pathsToMine:
        paths.append(findPath(path[0], path[1], childEdges, topParents))
        if(len(paths) % 100 == 0):
            print(len(paths))
    return paths

origVert = [x.rstrip() for x in origVert]
origEdges = [x.rstrip() for x in origEdges]
newVerts = [x.rstrip() for x in newVerts]
newEdges = [x.rstrip() for x in newEdges]
semanticTree = [x.rstrip() for x in semanticTree]
del(origVert[0])

vertices = {}
for line in origVert:
    a,b,c = line.split(" ")
    vertices[a] = [b,c]

newVertices = {}
for line in newVerts:
    a,b,c = line.split(" ")
    newVertices[a] = [b,c]

del(origEdges[0])
outboundPaths = {}
#inboundPaths is a dictinary where the key is a vertex and the values are an array which is composed of all the values which have roads going into the key value. This is the reverse of outboundPaths where the key has outbound roads to the values
inboundPaths = {}
pairings = []
for line in origEdges:
    a,b = line.split(" ")
    pairings.append((a,b))
    if a in outboundPaths:
        outboundPaths[a].append(b)

    else:
        outboundPaths[a] = [b]
    if b in inboundPaths:
        inboundPaths[b].append(a)

    else:
        inboundPaths[b] = [a]

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
print(getViewPortPaths(-5.5, -5, -5.5, -5, vertices, childEdges, topParents, outboundPaths,inboundPaths))
#This brute forces through everything. Estimated runtime: 300 hours. RIPO SKIPO
# paths = {}
# i=0
# for pairing in pairings:
#     frontStack = [pairing[0]]
#     backStack = [pairing[1]]
#     lastEdge = "hehe xD" #what's this for again?
#     i+=1
#     for entry in childEdges:
#         if pairing[0] in childEdges[entry][0] and pairing[1] in childEdges[entry][1]:
#             #print(lastEdge)
#             #removes line to make future pathing easier. This only happens for the initial unbundled edge so it should be okay, especially since the relationship is secured in inputEdges
#             #childEdges.remove(entry)
#             #print entry
#             #print childEdges[entry][2]
#             finalPath = hunt(childEdges[entry][2], frontStack, backStack, childEdges, topParents)
#             paths[pairing] = finalPath
#             if(len(paths[pairing]) > 15):
#                 print(paths[pairing])
#             break
#     if(i%10000 == 0):
#         print(i)
#         #looks like it takes 40 minutes to do 10 thousand paths
print("All roads generated. Have a great day! (hehe xd)")

#New implementation preferred: dict[src:dict[dest:[edgeId, weight, ParentID]]] BUT how do we find inbound edges quickly? do we make a reversed one?