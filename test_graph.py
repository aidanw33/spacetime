
# test_graph.py
import unittest
from graph import euclidean_distance   # Import the module to be tested
from graph import read_in_geometry
from graph import reflection_line

class TestGraphMethods(unittest.TestCase):
    def test_euclidean_distance(self):
        self.assertEqual(euclidean_distance((0, 0), (1, 0)), 1)
    
    def test_reflection_line(self) :
        self.assertEqual(reflection_line(0, 45), 90)       
        self.assertEqual(reflection_line(0, -45), -90)
        self.assertEqual(reflection_line(90, 45), 0)
        self.assertEqual(reflection_line(45, 0), -45)
        self.assertEqual(reflection_line(-45, 0), 45)
        self.assertEqual(reflection_line(-90, 45), 180)
if __name__ == '__main__':
    unittest.main()