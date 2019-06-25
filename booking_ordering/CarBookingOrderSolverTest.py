import unittest
from CarBookingOrderSolver import CarBookingOrderSolver

class CarbookingOrderSolverTest(unittest.TestCase):

    def test_json_data_1(self):
        cb = CarBookingOrderSolver()
        cb.solve('test_data_1.json')

    def test_json_data_2(self):
        cb = CarBookingOrderSolver()
        cb.solve('test_data_2.json')

    def test_json_data_empty(self):
        cb = CarBookingOrderSolver()
        cb.solve('test_data_empty.json')
        self.assertEqual(cb.get_cost(),-1)
        self.assertEqual(len(cb.get_booking_order()),0)


if __name__ == '__main__':
    unittest.main()
