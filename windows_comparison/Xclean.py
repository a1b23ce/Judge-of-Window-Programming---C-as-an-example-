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
				os.remove(root + '/' + "marked_model_image.png")
				os.remove(root + '/' + "marked_examinee_image.png")
				os.remove(root + '/' + "picture_model.png")
				os.remove(root + '/' + "picture_examinee.png")
				os.remove(root + '/' + "window_screenshot.png")
				os.remove(root + '/' + "sorted_original_data.txt")
				os.remove(root + '/' + "UpperLeftCorner.txt")
				os.remove(root + '/' + "correct_examinee.txt")
				
				# 將已處理過的資料夾加入集合
				processed_folders.add(root)
				
			except subprocess.CalledProcessError as e:
				print(f"Error executing {exe_path}: {e}")
		
	os.remove("model/window_screenshot.png")		
	os.remove("examinee_accuracy.txt")
	os.remove("model/sorted_original_data.txt")
	os.remove("model/UpperLeftCorner.txt")
	
def main():
	Clean(folder_path)

if __name__ == "__main__":
	main()
