import subprocess
import sys
import time
import uiautomation as auto
import re

def get_argument():
	if len(sys.argv) < 2:
		return None
	return sys.argv[1]

def clear_file(filename):
	try:
		with open(filename, "w") as file:
			file.write("")
	except Exception as e:
		print(f"An error occurred: {e}")
	file.close()

def capture(windowName):
	showAllName = False
	depth = 0xFFFFFFFF
	showPid = False
	indent = 0
	control = auto.WindowControl(searchDepth=1, Name=windowName)
	auto.EnumAndLogControl(control, depth, showAllName, showPid, startDepth=indent)
	auto.Logger.Log('Ends\n')
			

def main():
	clear_file('@AutomationLog.txt')
	Window_Name = get_argument()
	if Window_Name is None:
		Window_Name = 'CardGame'
	capture(Window_Name)

if __name__ == '__main__':
	main()
