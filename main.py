from infile import InFile
from outfile import OutFile
import math
import operator


class NoTimeLeft(Exception):
    pass


def compute_distance(coords_a, coords_b):
    x = math.pow(coords_a[0] - coords_b[0], 2)
    y = math.pow(coords_a[1] - coords_b[1], 2)
    return math.ceil(math.sqrt(x + y))


class DroneStates(object):
    """Stores the current position + the time needed to execute all the commands for a drone."""
    def __init__(self, in_file):
        self.states = [{"pos": in_file.warehouses[0]["coords"], "time": 0} for _ in range(0, in_file.drones_nb)]
        self.in_file = in_file


    def load(self, drone, warehouse):
        pos = self.states[drone]["pos"]
        dest = self.in_file.warehouses[warehouse]["coords"]
        time = compute_distance(pos, dest) + 1
        self.states[drone]["time"] += time
        self.states[drone]["pos"] = dest
        if self.states[drone]["time"] > self.in_file.deadline:
            raise NoTimeLeft

    def deliver(self, drone, order):
        pos = self.states[drone]["pos"]
        dest = self.in_file.orders[order]["coords"]
        time = compute_distance(pos, dest) + 1
        self.states[drone]["time"] += time
        self.states[drone]["pos"] = dest
        if self.states[drone]["time"] > self.in_file.deadline:
            raise NoTimeLeft


def find_warehouse(in_file, product_id, drone_pos):
    found_warehouses = []
    for i in range(0, in_file.w):
        if in_file.warehouses[i]["products"][product_id] > 0:
            warehouses_pos = in_file.warehouses[i]["coords"]
            dist = compute_distance(warehouses_pos, drone_pos)
            found_warehouses.append({"id": i, "dist": dist})
    found_warehouses.sort(key=operator.itemgetter("dist"))
    in_file.warehouses[found_warehouses[0]["id"]]["products"][product_id] -= 1
    return found_warehouses[0]["id"]


def sort_orders(orders, pos_warehouse):
    new_orders = []
    for i in range(0, len(orders)):
        dist = compute_distance(orders[i]["coords"], pos_warehouse)
        new_orders.append({"size": len(orders[i]["product_ids"]), "index": i, "dist": dist})
    new_orders.sort(key=operator.itemgetter("size", "dist"))
    return new_orders


def solve_easy(in_path, out_path):
    in_file = InFile(in_path)
    out_file = OutFile(out_path)
    states = DroneStates(in_file)
    d = 0  # Current drone number
    w = 0  # Current weight
    products_to_deliver = []
    new_orders = sort_orders(in_file.orders, in_file.warehouses[0]["coords"])
    for o in new_orders:
        order_id = o["index"]
        order = in_file.orders[order_id]
        for product_id in order["product_ids"]:
            # Find a warehouse where the product is available
            warehouse = find_warehouse(in_file, product_id, states.states[d]["pos"])
            if w + in_file.weights[product_id] > in_file.max_load:
                # We have to change the drone

                # The drone number d deliver the product
                try:
                    states.deliver(d, order_id)

                    # If there is still time, output the command
                    for p in products_to_deliver:
                        out_file.deliver(d, order_id, p, 1)
                except NoTimeLeft:
                    pass

                d += 1
                w = 0
                products_to_deliver = []
                if d >= in_file.d:
                    d = 0

            w += in_file.weights[product_id]
            products_to_deliver.append(product_id)
            # The drone number d take this product
            try:
                states.load(d, warehouse)

                # If there is still time, output the command
                out_file.load(d, warehouse, product_id, 1)
            except NoTimeLeft:
                pass

        # Empty the drone at end of order even is some space is left
        try:
            states.deliver(d, order_id)

            # If there is still time, output the command
            for p in products_to_deliver:
                out_file.deliver(d, order_id, p, 1)
        except NoTimeLeft:
            pass

        d += 1
        w = 0
        products_to_deliver = []
        if d >= in_file.d:
            d = 0

    out_file.write()


for name in ["redundancy", "mother_of_all_warehouses", "busy_day"]:
    solve_easy(name + ".in", name + ".out")
