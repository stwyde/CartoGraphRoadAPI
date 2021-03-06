import csv
from math import log
class FileCreator():
    def generateFilesFromSourceDest(self, edgesList, verticeDic, bundledVerticeList, pointsInPort =[]):
        verticeOutput = open("./simpleData/verticeForTest.txt", 'w')
        verticeOutputWriter = csv.writer(verticeOutput, delimiter = ' ')

        edgeOutput = open("./simpleData/edgesForTest.txt", 'w')
        edgeOutputWriter = csv.writer(edgeOutput, delimiter = ' ')

        print("Starting here")
        for edge_info in edgesList:
            weight = edge_info[0]
            src = edge_info[1][0]
            dest = edge_info[1][1]
            if src in verticeDic:
               # print(verticeDic[src])
                verticeOutputWriter.writerow([src, verticeDic[src][0], verticeDic[src][1]])
            elif src in bundledVerticeList:
                verticeOutputWriter.writerow([src, bundledVerticeList[src][0], bundledVerticeList[src][1]])
            if dest in verticeDic:
                verticeOutputWriter.writerow([dest, verticeDic[dest][0], verticeDic[dest][1]])
            elif dest in bundledVerticeList:
                verticeOutputWriter.writerow([dest, bundledVerticeList[dest][0], bundledVerticeList[dest][1]])
            edgeOutputWriter.writerow([src, dest, weight])
      #  for point in pointsInPort:
      #      verticeOutputWriter.writerow([point, verticeDic[point][0], verticeDic[point][1]])

        print("Done Here")
        verticeOutput.close()
        edgeOutput.close()

    def generateFilesFromSourceDest1(self, verticeDic, bundledVerticeList, paths, pointsInPort, bundledEdges, edgeMaxWeight):
        verticeOutput = open("./simpleData/verticeForTest.txt", 'w')
        verticeOutputWriter = csv.writer(verticeOutput, delimiter = ' ')

        edgeOutput = open("./simpleData/edgesForTest.txt", 'w')
        edgeOutputWriter = csv.writer(edgeOutput, delimiter = ' ')
        duplicateCatcher = set()
        duplicateEdgeCatcher = set()
        print("Starting here")

        for path in paths:

            #print "path", path
           # print("path", path)
            for i in range(0, len(path)-2):
                src = path[i]
                dest = path[i+1]
                if src == dest: continue
                if src not in duplicateCatcher:
                    if src in verticeDic:
                        verticeOutputWriter.writerow([src, verticeDic[src][0], verticeDic[src][1]])
                    elif src in bundledVerticeList:
                        verticeOutputWriter.writerow([src, bundledVerticeList[src][0], bundledVerticeList[src][1]])
                    duplicateCatcher.add(src)
                if dest not in duplicateCatcher:
                    if dest in verticeDic:
                        verticeOutputWriter.writerow([dest, verticeDic[dest][0], verticeDic[dest][1]])
                    elif dest in bundledVerticeList:
                        verticeOutputWriter.writerow([dest, bundledVerticeList[dest][0], bundledVerticeList[dest][1]])
                    duplicateCatcher.add(dest)
                if (src, dest) not in duplicateEdgeCatcher:
                    print (str(log(float(bundledEdges[(src,dest)]), float(edgeMaxWeight))) + " " + bundledEdges[(src,dest)])
                    weight = max(log(float(bundledEdges[(src,dest)]), float(edgeMaxWeight)) * float(40), 1)
                    edgeOutputWriter.writerow([src, dest, weight])
                    duplicateEdgeCatcher.add((src, dest, weight))
       # for point in pointsInPort:
        #     verticeOutputWriter.writerow([point, verticeDic[point][0], verticeDic[point][1]])


        print("Done Here")
        verticeOutput.close()
        edgeOutput.close()