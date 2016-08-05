import io
import os
import sys

from lib.gbkParser import *

command = ""
while command != "exit":
	command = input("Please enter a command.\n")

	try:
		if command == "execute":
			#getMajorCapsid("K:/phage/dat/caudo_with_major-capsid", True)
			getMajorCapsid_ConvertToFasta("D:/PHANTOME/Viruses-caudo_with_major-capsid", True)
			#allGbkToJson(path="K:/PHANTOME/Viruses-caudo_with_major-capsid", debugOn=True)
			#gbkReport.getAllAlias(path="K:/PHANTOME/Viruses-caudo_with_major-capsid")
		break
	except ValueError:
		print("Error: " + ValueError)