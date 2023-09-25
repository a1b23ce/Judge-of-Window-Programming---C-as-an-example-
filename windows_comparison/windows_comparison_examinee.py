import os
import subprocess
import time
import concurrent.futures
import sys

# 視窗名稱
Window_Name = None
exe_Name = None

# 資料夾路徑
folder_path = 'examinee'

def get_argument():
	if len(sys.argv) < 2:
		return None
	return sys.argv[1]

def record_result(examinee_number):				#examinee_number: 所在資料夾名稱
	with open("result.txt", "r", encoding='utf-8') as file:
		first_line = file.readline()		
	examinee_accuracy = examinee_number	+ " " + first_line
	with open("examinee_accuracy.txt", "a", encoding='utf-8') as file:
		file.write(examinee_accuracy)

def run_exe(folder_path):
	# 創建一個集合來存儲已處理過的資料夾路徑
	processed_folders = set(['examinee'])
	
	# 遍歷資料夾中的檔案與子資料夾
	for root, dirs, files in os.walk(folder_path):
		if root not in processed_folders:
			try:					
				# 運行程式
				subprocess.run(["python", "file/CaptureWindowInfo.py", root])
				subprocess.run(["python", "file/TwoDIndexTransformation_for_examinee.py", Window_Name])
				subprocess.run(["python", "file/TwoD_LCS.py"])
				subprocess.run(["python", "file/DrawTable_examinee.py", root])
				record_result(os.path.basename(root))
				
				os.remove("1-2.txt")
				os.remove("2-3examinee.txt")
				
				# 將已處理過的資料夾加入集合
				processed_folders.add(root)
				
			except subprocess.CalledProcessError as e:
				print(f"Error executing {exe_path}: {e}")

def main():
	global Window_Name, exe_Name
	Window_Name = get_argument()
	if Window_Name is None:
		Window_Name = 'CardGame'
	exe_Name = Window_Name + '.exe'	
		
	run_exe(folder_path)
	os.remove("model.txt")
	os.remove("2-3model.txt")
	os.remove("result.txt")

if __name__ == "__main__":
	main()
