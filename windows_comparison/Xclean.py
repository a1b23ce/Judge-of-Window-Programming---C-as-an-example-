import os
import subprocess
import time
import concurrent.futures
import sys

# 資料夾路徑
folder_path = 'examinee'

def Clean(folder_path):
	# 創建一個集合來存儲已處理過的資料夾路徑
	processed_folders = set(['examinee'])

	# 遍歷資料夾中的檔案與子資料夾
	for root, dirs, files in os.walk(folder_path):
		if root not in processed_folders:
			try:
				# 運行程式
				for file in ["marked_model_image.png", "marked_examinee_image.png", "picture_model.png", "picture_examinee.png", "window_screenshot.png", "sorted_original_data.txt", "UpperLeftCorner.txt", "correct_examinee.txt"]:
					file_path = os.path.join(root, file)
					if os.path.exists(file_path):
						os.remove(file_path)
					else:
						print(f"File not found: {file_path}")
				
				# 將已處理過的資料夾加入集合
				processed_folders.add(root)
				
			except subprocess.CalledProcessError as e:
				print(f"Error executing {exe_path}: {e}")
		
	# 刪除其他檔案
	for file in ["examinee_accuracy.txt", "statistics.txt", "model.txt", "2-3model.txt", "2-3examinee.txt", "1-2.txt", "result.txt", "model/window_screenshot.png", "model/sorted_original_data.txt", "model/UpperLeftCorner.txt"]:
		file_path = os.path.join(file)
		if os.path.exists(file_path):
			os.remove(file_path)
		else:
			print(f"File not found: {file_path}")

def main():
	Clean(folder_path)

if __name__ == "__main__":
	main()
