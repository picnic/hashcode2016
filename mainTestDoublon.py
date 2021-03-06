from infile import InFile
from outfile import OutFile
import math
import sys


class NoTimeLeft(Exception):
    pass


class DroneStates(object):
    """Stores the current position + the time needed to execute all the commands for a drone."""
    def __init__(self, in_file):
        self.states = [{"pos": in_file.warehouses[0]["coords"], "time": 0} for _ in range(0, in_file.drones_nb)]
        self.in_file = in_file

    def _compute_distance(self, coords_a, coords_b):
        x = math.pow(coords_a[0] - coords_b[0], 2)
        y = math.pow(coords_a[1] - coords_b[1], 2)
        return math.ceil(math.sqrt(x + y))

    def load(self, drone, warehouse):
        pos = self.states[drone]["pos"]
        dest = self.in_file.warehouses[warehouse]["coords"]
        time = self._compute_distance(pos, dest) + 1
        self.states[drone]["time"] += time
        self.states[drone]["pos"] = dest
        if self.states[drone]["time"] > self.in_file.deadline:
            raise NoTimeLeft

    def deliver(self, drone, order):
        pos = self.states[drone]["pos"]
        dest = self.in_file.orders[order]["coords"]
        time = self._compute_distance(pos, dest) + 1
        self.states[drone]["time"] += time
        self.states[drone]["pos"] = dest
        if self.states[drone]["time"] > self.in_file.deadline:
            raise NoTimeLeft

    #def repeat(self, weights):



def find_warehouse(in_file, product_id):
    for i in range(0, in_file.w):
        if in_file.warehouses[i]["products"][product_id] > 0:
            in_file.warehouses[i]["products"][product_id] -= 1
            return i
    assert False


def solve_easy(in_path, out_path):
    in_file = InFile(in_path)
    out_file = OutFile(out_path)
    states = DroneStates(in_file)
    d = 0  # Current drone number
    print(in_file.orders)
    orderNb = 0
    for order_id in range(0, in_file.c):
        orderNb += 1
        order = in_file.orders[order_id]
        for i in range(0, len(order["product_ids"])):
            for j in range(i + 1, len(order["product_ids"])):
                if order["product_ids"][i] == order["product_ids"][j]:
                    d += 1
                    print"Order : %d        ID1 : %d    ID2 : %d   DOUBLON" % (orderNb, order["product_ids"][i], order["product_ids"][j])
                #else:
                    #print"Order : %d        ID1 : %d    ID2 : %d" % (orderNb, order["product_ids"][i], order["product_ids"][j])
    print(d)

    out_file.write()


solve_easy(sys.argv[1], sys.argv[1][:-2] + "out")
