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

def close_exe_window(exe_name):
	os.system(f"taskkill /F /IM {exe_name}")

def run_exe(folder_path):
	# 遍歷資料夾中的檔案與子資料夾
	for root, dirs, files in os.walk(folder_path):
		for file in files:
			if file == exe_Name:
				exe_path = os.path.join(root, file)
				try:
					# 使用subprocess執行執行檔
					process = subprocess.Popen(exe_path, shell=True)
					
					# 運行程式
					subprocess.run(["python", "file/FindWindow.py", Window_Name])
					subprocess.run(["python", "file/FormattedOutput.py"])
					subprocess.run(["python", "file/TwoDIndexTransformation_for_model.py", Window_Name])
					os.remove("1-2.txt")
					os.remove("@AutomationLog.txt")
					
					# 等待1秒後關閉執行檔
					time.sleep(1)
					process.terminate()
					
					# 如果terminate無法關閉，則使用close_exe_window強制終止進程
					if process.returncode is None:
						close_exe_window(file)
					
				except subprocess.CalledProcessError as e:
					print(f"Error executing {exe_path}: {e}")

def main():
	global Window_Name, exe_Name
	Window_Name = get_argument()
	if Window_Name is None:
		Window_Name = 'CardGame'
	exe_Name = Window_Name + '.exe'
	
	run_exe(folder_path)
	

if __name__ == "__main__":
	main()
