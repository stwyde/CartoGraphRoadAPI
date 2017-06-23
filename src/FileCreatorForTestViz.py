import csv
class FileCreator():
    def generateFilesFromSourceDest(self, edgesList, verticeDic, bundledVerticeList, pointsInPort, repetead):
        verticeOutput = open("./verticeForTest.txt", 'w')
        verticeOutputWriter = csv.writer(verticeOutput, delimiter = ' ')

        edgeOutput = open("./edgesForTest.txt", 'w')
        edgeOutputWriter = csv.writer(edgeOutput, delimiter = ' ')
      #  rep = open("./repeated.txt", 'w')
     #   reapWriter  = csv.writer(rep, delimiter = ' ')
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

       # reapWriter.writerow([len(repetead)])
       # for edge in repetead:
        #    reapWriter.writerow(edge)
        print("Done Here")
        verticeOutput.close()
        edgeOutput.close()
