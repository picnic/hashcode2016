

class OutFile(object):
    """output files writer."""

    def __init__(self, path):
        self.path = path
        self.buffer = ""

    def write(self):
        with open(self.path, "w") as f:
            f.write(self.buffer)

    def load(self, drone, warehouse, product_id, nb):
        self.buffer += "%d L %d %d %d\n" % (drone, warehouse, product_id, nb)

    def unload(self, drone, warehouse, product_id, nb):
        self.buffer += "%d U %d %d %d\n" % (drone, warehouse, product_id, nb)

    def deliver(self, drone, customer, product_id, nb):
        self.buffer += "%d D %d %d %d\n" % (drone, customer, product_id, nb)

    def wait(self, drone, nb):
        self.buffer += "%d W %d\n" % (drone, nb)
