from infile import InFile
from outfile import OutFile

# Usage example
in_file = InFile("busy_day.in")
print(in_file.weights)
print(in_file.orders[10])

out_file = OutFile("busy_day.out")
out_file.load(0, 1, 2, 10)
out_file.unload(0, 1, 2, 10)
out_file.deliver(1, 4, 2, 10)
out_file.wait(1, 400)
out_file.write()
