class node:
    xcord = 0
    ycord = 0
    nodeID = ""
    terminalNode = False
    adjacentNodes = [] #array just due to ease in iterating
    terminalPaths = {"node id": "node path"}

    def __init__(self, inputverticesTextFile):
        xcord = inputverticesTextFile.xcord
        ycord = inputverticesTextFile.ycord
        nodeID = inputverticesTextFile.nodeID
