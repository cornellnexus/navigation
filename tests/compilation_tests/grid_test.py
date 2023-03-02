import unittest
import matplotlib.pyplot as plt

from engine.grid import Grid
from engine.kinematics import get_vincenty_x, get_vincenty_y
from engine.mission import ControlMode

'''
Visualization and unit tests for grid.py
'''


def graph_traversal_path(g, map_name, distance_type, mode=ControlMode.LAWNMOWER):
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
       pass  # passing only for github tests to not have graph pop-ups
       # graph_traversal_path(g, 'Engineering Quad', 'Vincenty', ControlMode.LAWNMOWER)
   #

   def test_paul_mansion(self):
       g = Grid(42.444250, 42.444599, -76.483682, -76.483276)
       pass  # passing only for github tests to not have graph pop-ups
       # graph_traversal_path(g, 'Paul Mansion', 'Vincenty', ControlMode.SPIRAL)

   def test_paul_backyard(self):
       g = Grid(42.444250, 42.444599, -76.483682, -76.483276)
       pass  # passing only for github tests to not have graph pop-ups
       # graph_traversal_path(g, 'Paul Backyard', 'Vincenty', ControlMode.LAWNMOWER_B)


class TestGrid(unittest.TestCase):
   def test_borders_mode(self):
       count = 0
       g = Grid(42.444250, 42.444599, -76.483682, -76.483276)
       full_waypoints = g.get_waypoints(ControlMode.LAWNMOWER)
       for nd in full_waypoints:
           if nd.is_border_node():
               count += 1
       self.assertNotEqual(count, g.get_num_rows(
       ) * g.get_num_cols(), 'is_border_node flag is set correctly')
       self.assertEqual(count, g.get_num_cols() * 2,
                        'is_border_node flag is set correctly')
       border_waypoints = g.get_waypoints(ControlMode.LAWNMOWER_B)
       border_node_count = (g.get_num_cols()*2)
       self.assertEqual(len(border_waypoints), border_node_count)

   def test_node_boundaries(self):
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)
       full_waypoints = g.get_waypoints(ControlMode.LAWNMOWER)

       y_range = get_vincenty_y((lat_min, long_min), (lat_max, long_max))
       x_range = get_vincenty_x((lat_min, long_min), (lat_max, long_max))
       top_right_node = g.nodes[g.get_num_rows()-1][g.get_num_cols()-1]
       self.assertLessEqual(top_right_node.get_m_coords()[
                            0], x_range, "The meters grid shouldn't be larger than the lat bounds")
       self.assertLessEqual(top_right_node.get_m_coords()[
                            1], y_range, "The meters grid shouldn't be larger than the long bounds")

   def test_inside(self):
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)
       self.assertTrue(g.is_inside_triangle(2, 2, 3, 3, 1, 3, 2,
                       2.5), "this point is inside the triangle")
       self.assertFalse(g.is_inside_triangle(2, 2, 3, 3, 1, 3,
                        10, 10), "this point is outside the triangle")
       self.assertTrue(g.is_inside_triangle(2, 2, 3, 3, 1, 3, 2,
                       2), "this point is inside the triangle")

   def test_is_on_border_triangle(self):
       count = 0
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)
      
       g.activate_triangle(1,1,5,5,9,1)
       g.find_border_nodes()

       count = 0
       rows = g.nodes.shape[0]
       cols = g.nodes.shape[1]
       for row in range(rows):
           for col in range(cols):
               node = g.nodes[row][col]
               if node.is_active_node() and g.is_on_border(row, col, rows-1, cols-1):
                   count += 1

       self.assertEqual(len(g.border_nodes), count)

   def test_is_on_border_rectangle(self):
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)
      
       rows = g.nodes.shape[0]
       cols = g.nodes.shape[1]

       g.activate_rectangle(0, 0, rows, cols)
       g.find_border_nodes()

       count = 0
       for row in range(rows):
           for col in range(cols):
               node = g.nodes[row][col]
               if node.is_active_node() and g.is_on_border(row, col, rows-1, cols-1):
                   count += 1
                  
       self.assertEqual(len(g.border_nodes), count)

   def test_is_on_border_circle(self):   
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)
      
       rows = g.nodes.shape[0]
       cols = g.nodes.shape[1]

       g.activate_circle(0, 0, 5)
       g.find_border_nodes()

       count = 0
       for row in range(rows):
           for col in range(cols):
               node = g.nodes[row][col]
               if node.is_active_node() and g.is_on_border(row, col, rows-1, cols-1):
                   count += 1
                  
       self.assertEqual(len(g.border_nodes), count)
      
   def test_find_border_nodes(self):
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)
      
       rows = g.nodes.shape[0]
       cols = g.nodes.shape[1]
      
       g.activate_rectangle(0, 0, rows, cols)

       borderNodes = []
       for row in range(rows):
           for col in range(cols):
               node = g.nodes[row][col]
               if node.is_active_node() and g.is_on_border(row, col, rows-1, cols-1):
                   borderNodes.append((node, row, col))

       g.find_border_nodes()

       self.assertEqual(g.border_nodes, borderNodes)

   def test_get_neighbor_nodes_VersionNone(self):
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)
      
       rows = g.nodes.shape[0]
       cols = g.nodes.shape[1]

       g.activate_rectangle(0, 0, rows, cols)

       self.assertEqual(g.get_neighbor_node(-1, 0, rows, cols), None)

   def test_get_neighbor_nodes(self):
       lat_min, lat_max, long_min, long_max = 42.444250, 42.444599, -76.483682, -76.483276
       g = Grid(lat_min, lat_max, long_min, long_max)

       rows = g.nodes.shape[0]
       cols = g.nodes.shape[1]

       g.activate_rectangle(0, 0, rows, cols)

       for row in range(rows):
           for col in range(cols):
               node = g.nodes[row][col]
               self.assertEqual(g.get_neighbor_node(row, col, rows, cols), node)

if __name__ == '__main__':
   unittest.main()
