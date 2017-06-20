origVert = open("../simpleData/Original Vertices.txt", "r")
semanticTree = open("../simpleData/NewSemanticTree.txt", "r")


def getPath(childEdgeId, edgeDict, frontStack = [], backStack = []):
    if(len(edgeDict[childEdgeId]) == 4):
        #we still have parents!
        parentID = edgeDict[childEdgeId][2]
        frontStack.append(edgeDict[parentID][0])
        backStack.insert(0, edgeDict[parentID][1])
        return getPath(parentID, edgeDict, frontStack, backStack)
    elif(len(edgeDict[childEdgeId]) == 3):
        #merge stacks:
        frontStack.append(backStack)
        return frontStack

def getViewPortPaths(xmin, xmax, ymin, ymax, vertices, outboundPaths, inboundPaths, edgeDict):
    pointsinPort = []
    outpathsToMine = []
    inpathsToMine = []
    for point in vertices:
        if xmax > float(vertices[point][0]) > xmin and ymin < float(vertices[point][1]) < ymax:
            pointsinPort.append(point) #points in port is an array of pointIDs which are strings.
            try:
                for dest in outboundPaths[point]:
                    outpathsToMine.append((point, dest)) #outpaths and inpaths include points and dest of edges we want to reconstruct
            except KeyError:
                pass
            try:
                for src in inboundPaths[point]:
                    inpathsToMine.append([src, point])
            except KeyError:
                pass

    print("Points in the viewport: ")
    print(pointsinPort)
    paths = []
    print("Finding paths now. Paths to do: " + str(len(inpathsToMine) +len(outpathsToMine)))
    for path in inpathsToMine: #path[0] = src, path[1] = dest
        paths.append(getPath(inboundPaths[path[1]][path[0]][0], edgeDict,[path[1]], [path[0]]))
        if(len(paths) % 100 == 0):
            print(len(paths))
    for path in outpathsToMine:
        paths.append(getPath(outboundPaths[path[0]][path[1]][0], edgeDict, [path[0]], [path[1]]))
        if (len(paths) % 100 == 0):
            print(len(paths))
    return paths

origVert = [x.rstrip() for x in origVert]
semanticTree = [x.rstrip() for x in semanticTree]
dictFormingSemanticTree = semanticTree
del(origVert[0])
vertices = {}
#Creates a dict with vertex ID as key, then x/y coordinates as values in array list.
for line in origVert:
    a,b,c = line.split(" ")
    vertices[a] = [b,c]


outboundPaths = {}
edgeDictionary = {}
#inboundPaths is a dictinary where the key is a vertex and the values are an array which is composed of all the values which have roads going into the key value. This is the reverse of outboundPaths where the key has outbound roads to the values
inboundPaths = {}
#Todo: set pairings to be the new fangled dictionary thingamabobber
pairings = []
for line in dictFormingSemanticTree:
    elements = line.split(" ")
    edgeDictionary[elements[0]] = elements[1:] #Edge ID as key,  [src, dest, parent, weight] as vals
    #if both src and dst are in orig Vertices:
    if(elements[1] in vertices.keys() and elements[2] in vertices.keys()):
        #todo: reverify this makes sense. elements[1] is src, elements[2] is dest
        pairings.append((elements[1], elements[2]))
        if len(elements) == 4: #here there's EdgeID, src, dest, weight, here we ARE at the parent
            if elements[1] in outboundPaths.keys():
                outboundPaths[elements[1]].update({elements[2]: [elements[0], elements[3]]})
            else:
                outboundPaths[1] = {elements[2]: [elements[0], elements[3]]}
            if elements[2] in inboundPaths.keys():
                inboundPaths[elements[2]].update({elements[1]:[elements[0], elements[3]]})
            else:
                inboundPaths[elements[2]] = {elements[1]:[elements[0], elements[3]]}
        elif len(elements) == 5: #here we are still at a child and have to append the parent. format: Src key -> dest Key -> [EdgeId, Weight, Parent if exists], if path[src][dest].size = 3, we gotta keep going, if =2, we at end
            if elements[1] in outboundPaths.keys():
                outboundPaths[elements[1]].update({elements[2]: [elements[0], elements[4], elements[3]]})
            else:
                outboundPaths[1] = {elements[2]: [elements[0], elements[4], elements[3]]}
            if elements[2] in inboundPaths.keys():
                inboundPaths[elements[2]].update({elements[1]: [elements[0], elements[4], elements[3]]})
            else:
                inboundPaths[elements[2]] = {elements[1]: [elements[0], elements[4], elements[3]]}


print("Done setting up stuff, now pairing and pathing")
print(getViewPortPaths(-5.5, -5, -5.5, -5, vertices, outboundPaths,inboundPaths, edgeDictionary))
print("All roads generated. Have a great day! (hehe xd)")

#New implementation preferred: dict[src:dict[dest:[edgeId, weight, ParentID]]] BUT how do we find inbound edges quickly? do we make a reversed one?