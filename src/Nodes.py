class node:
    xcord = 0
    ycord = 0
    nodeID = ""
    terminalNode = False
    adjacentNodes = [] #array just due to ease in iterating
    terminalPaths = {"node id": "node path"}

    def __init__(self, inputverticesTextFile, inputEdgesTextFile, pairingsTextFile):
        xcord = inputverticesTextFile.xcord
        ycord = inputverticesTextFile.ycord
        nodeID = inputverticesTextFile.nodeID
        #set if terminalNode (true) or intermediateNode (False) by looking at source file:
        terminalNode = inputverticesTextFile.sourceType
        self.generateAdjacentNodes(inputEdgesTextFile)
        self.generateTerminalPaths(inputEdgesTextFile, pairingsTextFile)

    def generateAdjacentNodes(self, inputEdgesTextFile):
        #run through the edges list
        #if edge source == nodeID: adjacentNodes.append edgeDestinationID
        self.adjacentNodes.append("BONOBONODE")

    def generateTerminalPaths(self, inputEdgesTextFile, pairingsTextFile):
        #append to terminalPaths, go through oldinputEdgesTextFile and use the pairings as keys, then go trhough input edges and search for them!
        self.terminalPaths[pairingsTextFile.nodeID] = self.generatePath(self.nodeID, pairingsTextFile.nodeID, inputEdgesTextFile)

    def generatePath(self, start, stop, paths):
        #find the path. IDK how
        print("BONOBOS")