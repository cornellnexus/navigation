import unittest
import matplotlib.pyplot as plt

from engine.grid import Grid
from engine.kinematics import get_vincenty_x, get_vincenty_y

'''
Visualization and unit tests for grid.py
'''


def graph_traversal_path(g, map_name, distance_type, mode='full'):
    """
    Plots both the gps and meters grid generated by Grid.py
    """
    traversal_path = g.get_waypoints(mode)
    gps_xlist = []  # longitude
    gps_ylist = []  # latitude
    m_xlist = []
    m_ylist = []

    for node in traversal_path:
        gps_coords = node.get_gps_coords()
        gps_ylist.append(gps_coords[0])
        gps_xlist.append(gps_coords[1])

        m_coords = node.get_m_coords()
        m_xlist.append(m_coords[0])
        m_ylist.append(m_coords[1])

    # Plotting gps grid
    plot1 = plt.figure(1)
    plt.plot(gps_xlist, gps_ylist, marker='o', markerfacecolor='blue')
    plt.plot(gps_xlist[0], gps_ylist[0], marker='o', markerfacecolor='red')
    plt.ylim(min(gps_ylist) - 0.000001, max(gps_ylist) + 0.000001)
    plt.xlim(min(gps_xlist) - 0.000001, max(gps_xlist) + 0.000001)
    plt.title('Grid in GPS coordinates ' + '(' + distance_type + ')')

    # Plotting meters grid
    plot2 = plt.figure(2)
    plt.plot(m_xlist, m_ylist, marker='o', markerfacecolor='blue')
    plt.plot(m_xlist[0], m_ylist[0], marker='o', markerfacecolor='red')
    plt.ylim(min(m_ylist) - 1, max(m_ylist) + 1)
    plt.xlim(min(m_xlist) - 1, max(m_xlist) + 1)
    plt.title(map_name + ' Grid in Meters ' + '(' + distance_type + ')')

    plt.show()
    plt.close()


class VisualizeGrid(unittest.TestCase):
    # uncomment the desired grid to be visualized

    # def test_jessica_house(self):
    #     g = Grid(-76.483682, -76.483276, 42.444250, 42.444599)
    #     graph_traversal_path(g, 'Jessica House', 'Vincenty')

    # def test_pike_room(self):
    #     g = Grid(-76.488495, -76.488419, 42.444496, 42.444543)
    #     graph_traversal_path(g, 'Pike Room', 'Vincenty')

    def test_engineering_quad(self):
        g = Grid(42.444250, 42.444599, -76.483682, -76.483276)
        graph_traversal_path(g, 'Engineering Quad', 'Vincenty', 'full')


class TestGrid(unittest.TestCase):
    def test_borders_mode(self):
        count = 0
        g = Grid(42.444250, 42.444599, -76.483682, -76.483276)
        full_waypoints = g.get_waypoints('full')
        for nd in full_waypoints:
            if nd.is_border_node():
                count += 1
        self.assertNotEqual(count, g.get_num_rows() * g.get_num_cols(), 'is_border_node flag is set correctly')
        self.assertEqual(count, g.get_num_cols() * 2, 'is_border_node flag is set correctly')
        border_waypoints = g.get_waypoints('borders')
        border_node_count = (g.get_num_cols()*2)
        self.assertEqual(len(border_waypoints), border_node_count)

    def test_node_boundaries(self):
        lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
        g = Grid(lat_min, lat_max, long_min, long_max)
        full_waypoints = g.get_waypoints('full')

        y_range = get_vincenty_y((lat_min, long_min), (lat_max, long_max))
        x_range = get_vincenty_x((lat_min, long_min), (lat_max, long_max))
        top_right_node = g.nodes[g.get_num_rows()-1][g.get_num_cols()-1]
        self.assertLessEqual(top_right_node.get_m_coords()[0], x_range, "The meters grid shouldn't be larger than the lat bounds")
        self.assertLessEqual(top_right_node.get_m_coords()[1], y_range, "The meters grid shouldn't be larger than the long bounds")


if __name__ == '__main__':
    unittest.main()
