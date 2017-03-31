import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

import unittest
from xsvlib import XSV

class TestXSVLib(unittest.TestCase):

    def test_basic(self):
        xsv = XSV("example.csv")
        self.assertEqual(xsv.preview(), ["a", "b", "c"])

        rows = [row for row in xsv.rows()]
        self.assertEqual(rows[0], ["a", "b", "c"])
        self.assertEqual(rows[1], ["1", "2", "3"])

        xsv.add_column("summation", lambda row: sum(map(int, row)))
        rows = [row for row in xsv.rows()]
        self.assertEqual(rows[0], ["a", "b", "c", "summation"])
        self.assertEqual(rows[1], ["1", "2", "3", 6])

        xsv.remove_column(1)
        rows = [row for row in xsv.rows()]
        self.assertEqual(rows[0], ["a", "c", "summation"])
        self.assertEqual(rows[1], ["1", "3", 6])

        xsv.rename_column(1, "b")
        rows = [row for row in xsv.rows()]
        self.assertEqual(rows[0], ["a", "b", "summation"])
        self.assertEqual(rows[1], ["1", "3", 6])

        xsv.reorder_column([2, 0, 1])
        rows = [row for row in xsv.rows()]
        self.assertEqual(rows[0], ["summation", "a", "b"])
        self.assertEqual(rows[1], [6, "1", "3"])

        xsv.map_column(1, int)
        rows = [row for row in xsv.rows()]
        self.assertEqual(rows[0], ["summation", "a", "b"])
        self.assertEqual(rows[1], [6, 1, "3"])
        
        xsv.save("example.new.csv")

if __name__ == '__main__':
    unittest.main()
