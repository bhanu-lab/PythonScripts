import sys
import platform
import imp

print("Python EXE : " + sys.executable)
print("Architecture : " + platform.architecture()[0])
print("Path to arcpy : " + imp.find_module("arcpy")[1])

raw_input("nnPress ENTER to quit")[/sourcecode]