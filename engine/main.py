import math
import threading
import json

from constants.definitions import ENGINE_PATH
from engine.robot import Robot
from engine.robot_state import Robot_State
from engine.robot import Phase
from engine.mission import Mission
from engine.mission_state import Mission_State
from engine.control_mode import ControlMode
from engine.database import DataBase
from engine.transmission import send_packet_to_gui
from engine.is_raspberrypi import is_raspberrypi
from engine.plot_trajectory import plot_sim_traj

if __name__ == "__main__":
    # Load config from JSON file
    with open(ENGINE_PATH +"/config.json", "r") as fp:
        args = json.load(fp)
    
    # Development flags
    is_transmit = args["is_transmit"] # Set to true when the rpi/robot is communicating w/ the GUI
    is_sim = args["is_sim"] if is_raspberrypi() else not is_raspberrypi() # Set to true when simulating the rpi, set to false when running on rpi
    store_data = args["store_data"] # Set to true when we want to track/store csv data

    r2d2_state = Robot_State(xpos=0, ypos=0, heading=math.pi / 4, epsilon=0.2, max_velocity=0.5, radius=0.2, phase = Phase.TRAVERSE)
    r2d2 = Robot(robot_state=r2d2_state)
    database = DataBase(r2d2) # TODO: Replace w new packet transmission impl
    mission_state = Mission_State(robot=r2d2, base_station_coord=(42.444250, -76.483682),
                init_control_mode=ControlMode.LAWNMOWER)
    m = Mission(mission_state=mission_state)
    
    '''------------------- MISSION EXECUTION -------------------'''
    if is_transmit:
        packet_sender = threading.Thread(target=send_packet_to_gui, args=(
            1, is_sim, r2d2_state, database), daemon=True)  # Thread to read and send robot properties
        packet_sender.start()

    m.execute_mission(database)  # Run main mission

    ''' ---------- MISSION COMPLETE, PLOT TRUTH POSE --------------'''
    plot_sim_traj(m=m) #  Plot the trajectory of the completed mission