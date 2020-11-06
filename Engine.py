from UserUtils import *
from FileUtils import *
# from Graph import Graph
from GUI import GUI
from obstacle import *


class Engine:

    def run(self):
        longMin, longMax, latMin, latMax = getLongLatMinMaxFromUser()
        graph = Obstacle(longMin, longMax, latMin, latMax)
        # graph.printAllCoordinates()

        coordsList = graph.startTraversal()
        #
        # coordsGenerated = graph.getAllCoordinatesGenerated()
        #
        # writeCoordsToCSVFile(coordsList)
        #
        # shouldDisplayGUI = getDisplayGuiFromUserInput()
        #
        # for coord in coordsList:
        #     coordsGenerated.remove(coord)
        #
        # print("----Coords not traversed----")
        # if (shouldDisplayGUI):
        #     gui = GUI(longMax, latMax)
        #     gui.animateRobotMovingGivenCoordList(coordsList)
        # # print(graph.getAllCoordinatesGenerated())
        # print("COORDINATES: \n\n\n\n\n")
        # print(coordsList)
        # return coordsList


engine = Engine()
engine.run()
