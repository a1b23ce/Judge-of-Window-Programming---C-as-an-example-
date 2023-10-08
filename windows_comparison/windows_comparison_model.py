import os
import subprocess
import time
import concurrent.futures
import sys

# 視窗名稱
Window_Name = None

# 資料夾路徑
folder_path = 'model'
	
def get_last_sixth_line():
	try:
		with open('1-2.txt', 'r', encoding='utf-8') as file:
			lines = file.readlines()
			
		if len(lines) >= 6:
			elements = lines[-6].strip().split('@')  # 以'@'分隔符號分開元素
			if len(elements) >= 6:
				# 取第二到第五個元素
				selected_elements = elements[1:5]
				# 將選定的元素以' '為分隔符號合併成字串
				output_text = ' '.join(selected_elements)
				# 將結果寫入output.txt
				with open(folder_path + '/UpperLeftCorner.txt', 'w', encoding='utf-8') as output_file:
					output_file.write(output_text)
				return elements[5]
			else:
				return "倒數第三行元素數量不足六個"
		else:
			return "檔案行數不足三行"
	except FileNotFoundError:
		return "檔案不存在"

def run_exe(folder_path):
	subprocess.run(["python", "file/CaptureWindowInfo.py", folder_path])
	Window_Name = get_last_sixth_line()
	subprocess.run(["python", "file/TwoDIndexTransformation_for_model.py", Window_Name, folder_path])
#	os.remove("1-2.txt")

def main():
	global Window_Name
	if Window_Name is None:
		Window_Name = 'CardGame'
	
	run_exe(folder_path)
	

if __name__ == "__main__":
	main()
