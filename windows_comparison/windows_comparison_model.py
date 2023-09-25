import os
import subprocess
import time
import concurrent.futures
import sys

# 視窗名稱
Window_Name = None
exe_Name = None

# 資料夾路徑
folder_path = 'model'

def get_argument():
	if len(sys.argv) < 2:
		return None
	return sys.argv[1]

def run_exe(folder_path):
		subprocess.run(["python", "file/CaptureWindowInfo.py", folder_path])
		subprocess.run(["python", "file/TwoDIndexTransformation_for_model.py", Window_Name])
		os.remove("1-2.txt")

def main():
	global Window_Name, exe_Name
	Window_Name = get_argument()
	if Window_Name is None:
		Window_Name = 'CardGame'
	exe_Name = Window_Name + '.exe'
	
	run_exe(folder_path)
	

if __name__ == "__main__":
	main()
