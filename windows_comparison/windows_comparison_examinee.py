import os
import subprocess
import time
import concurrent.futures
import sys

# 視窗名稱
Window_Name = None

# 資料夾路徑
folder_path = 'examinee'

def get_last_sixth_line(output_file):
	output_path = output_file + '/' + 'UpperLeftCorner.txt'
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
				with open(output_path, 'w', encoding='utf-8') as output_file:
					output_file.write(output_text)
				return elements[5]
			else:
				return "倒數第三行元素數量不足六個"
		else:
			return "檔案行數不足三行"
	except FileNotFoundError:
		return "檔案不存在"

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
				Window_Name = get_last_sixth_line(root)
				subprocess.run(["python", "file/TwoDIndexTransformation_for_examinee.py", Window_Name, root])
				subprocess.run(["python", "file/DirectionMethod(2D_LCS).py", root])
				subprocess.run(["python", "file/DrawTable_model.py", root])
				subprocess.run(["python", "file/DrawTable_examinee.py", root])
				subprocess.run(["python", "file/MarkOriginalImage.py", 'M', root])
				subprocess.run(["python", "file/MarkOriginalImage.py", 'E', root])
				record_result(os.path.basename(root))
				
				os.remove("1-2.txt")
				os.remove("2-3examinee.txt")
				
				# 將已處理過的資料夾加入集合
				processed_folders.add(root)
				
			except subprocess.CalledProcessError as e:
				print(f"Error executing {exe_path}: {e}")
	
	os.remove("model.txt")
	os.remove("2-3model.txt")
	os.remove("result.txt")

def main():
	global Window_Name
	if Window_Name is None:
		Window_Name = 'CardGame'
		
	run_exe(folder_path)

if __name__ == "__main__":
	main()
