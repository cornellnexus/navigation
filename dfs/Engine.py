from UserUtils import *
from FileUtils import *
from Graph import Graph
from GUI import GUI

class Engine:

    def run(self):
        longMin,longMax,latMin,latMax = getLongLatMinMaxFromUser()
        graph = Graph(longMin, longMax, latMin, latMax)
        #graph.printAllCoordinates()

        coordsList = graph.startDFSTraversalAtCoordinate(latMin,longMin) #all coords traversed

        coordsGenerated = graph.getAllCoordinatesGenerated()

        


        writeCoordsToCSVFile(coordsList)

        shouldDisplayGUI = getDisplayGuiFromUserInput()

        for coord in coordsList:
            coordsGenerated.remove(coord)

        print("----Coords not traversed----")
        print(coordsGenerated)

        if (shouldDisplayGUI):
            gui = GUI(longMax,latMax)
            gui.animateRobotMovingGivenCoordList(coordsList)

         
engine = Engine()
engine.run()