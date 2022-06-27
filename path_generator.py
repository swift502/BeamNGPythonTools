# 1. Install Python from https://www.python.org/downloads/
# 2. Install clipboard - run "pip install clipboard" in the Python shell
# 3. Adjust settings down below
# 4. Run this file
# 5. Code block will get generated into your clipboard, press ctrl+v to paste it in your map.json

# Settings
pathName = "tunnels_e"
numberOfNodes = 42
oneWay = 0
drivability = 1
flipDirection = 0

# Code
string = ""
#string += "    "
string += "\"" + pathName + "\" : {\n"
string += "      \"nodes\" : ["

for x in range(numberOfNodes):
	if x != 0:
		string += ", "
	string += "\"" + pathName + str(x + 1) + "\""

string += "],\n"
string += "      \"drivability\" : " + str(drivability) + ",\n"
if oneWay == 1: string += "      \"oneWay\" : " + str(oneWay).lower() + ",\n"
if flipDirection == 1: string += "      \"flipDirection\" : " + str(flipDirection).lower() + ",\n"
string += "    },"

import clipboard
clipboard.copy(string)
