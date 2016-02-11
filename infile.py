

class InFile(object):
    """Parser for input files."""

    def __init__(self, path):

        with open(path, "r") as f:
            content = f.readlines()
            content = list(map(lambda x: x[:-1].split(" "), content))
            first_line = content[0]
            self.rows = int(first_line[0])
            self.columns = int(first_line[1])
            self.drones_nb = self.d = int(first_line[2])
            self.deadline = int(first_line[3])
            self.max_load = int(first_line[4])

            self.p = self.products_nb = int(content[1][0])
            self.weights = list(map(int, content[2]))

            self.w = self.warehouses_nb = int(content[3][0])
            self.warehouses = []
            content = content[4:]
            for i in range(0, self.w):
                coords = list(map(int, content[0]))
                products = list(map(int, content[1]))
                self.warehouses.append({"coords": coords, "products": products})
                content = content[2:]

            self.c = self.orders_nb = int(content[0][0])
            self.orders = []
            content = content[1:]
            for i in range(0, self.c):
                coords = list(map(int, content[0]))
                product_ids = list(map(int, content[2]))
                self.orders.append({"coords": coords, "product_ids": product_ids})
                content = content[3:]
