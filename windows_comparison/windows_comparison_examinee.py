import os
import subprocess
import time
import concurrent.futures

# 視窗名稱
Window_Name = 'CardGame'
exe_Name = Window_Name + '.exe'

# 資料夾路徑
folder_path = 'examinee'

def record_result(examinee_number):				#examinee_number: 所在資料夾名稱
	with open("result.txt", "r", encoding='utf-8') as file:
		first_line = file.readline()		
	examinee_accuracy = examinee_number	+ " " + first_line
	with open("examinee_accuracy.txt", "a", encoding='utf-8') as file:
		file.write(examinee_accuracy)

def close_exe_window(exe_name):
    os.system(f"taskkill /F /IM {exe_name}")

def run_exe(folder_path):
	# 遍歷資料夾中的檔案與子資料夾
	for root, dirs, files in os.walk(folder_path):
		for file in files:
			if file == exe_Name:
				exe_path = os.path.join(root, file)			# 取得 CardGame.exe 的完整路徑
				parent_folder = os.path.basename(os.path.dirname(exe_path))	# 取得上一層資料夾路徑
				try:
					# 使用subprocess執行執行檔
					process = subprocess.Popen(exe_path, shell=True)
					
					# 運行程式
					subprocess.run(["python", "file/FindWindow.py", Window_Name])
					subprocess.run(["python", "file/FormattedOutput.py"])
					subprocess.run(["python", "file/TwoDIndexTransformation_for_examinee.py", Window_Name])
					subprocess.run(["python", "file/TwoD_LCS.py"])
					record_result(parent_folder)
					
					os.remove("1-2.txt")
					os.remove("2-3examinee.txt")
					os.remove("@AutomationLog.txt")
					
					# 等待0.2秒後關閉執行檔
					time.sleep(0.2)
					process.terminate()
					
	                # 如果terminate無法關閉，則使用close_exe_window強制終止進程
					if process.returncode is None:
						close_exe_window(file)
					
				except subprocess.CalledProcessError as e:
					print(f"Error executing {exe_path}: {e}")

def main():
	run_exe(folder_path)
	os.remove("model.txt")
	os.remove("2-3model.txt")
	os.remove("result.txt")

if __name__ == "__main__":
	main()
