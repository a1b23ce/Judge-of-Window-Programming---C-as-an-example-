from PIL import Image, ImageDraw
import pandas as pd
import random
import sys

file_path = 'model'
model_or_examinee = None	# M:model E:examiniee

def DrawSquare():
	Squares = []
		
	# 開啟圖片
	if model_or_examinee == 'M':
		image = Image.open('model' + '/' +'window_screenshot.png')
	else:
		image = Image.open(file_path + '/' +'window_screenshot.png')
	# 創建畫布對象
	draw = ImageDraw.Draw(image)
	# 讀取座標數據
	if model_or_examinee == 'M':
		data = pd.read_csv('model' + '/' + 'sorted_original_data.txt', delimiter='@', header=None, names=['序號', 'x1座標', 'y1座標', 'x2座標', 'y2座標', '文字', '新序號', '新x座標', '新y座標'])  # 使用@符號作為分隔符
	else:
		data = pd.read_csv(file_path + '/' + 'sorted_original_data.txt', delimiter='@', header=None, names=['序號', 'x1座標', 'y1座標', 'x2座標', 'y2座標', '文字', '新序號', '新x座標', '新y座標'])  # 使用@符號作為分隔符
	# 讀取左上角座標
	if model_or_examinee == 'M':
		with open('model' + '/' + 'UpperLeftCorner.txt', "r") as f:
			UpperLeftCorner_coordinate = [int(num) for num in f.read().split()]
	else:
		with open(file_path + '/' + 'UpperLeftCorner.txt', "r") as f:
			UpperLeftCorner_coordinate = [int(num) for num in f.read().split()]
	
	# 讀取要圈出的序號
	with open(file_path + '/correct_examinee.txt', "r") as f:
		correct_coordinates = [line.split() for line in f.read().splitlines()]
	
	if model_or_examinee == 'M':
		for index, row in data.iterrows():
			# 如果序號在correct_numbers中，則畫紅色方框
			for coord in correct_coordinates:
				if int(row['序號']) == int(coord[0]):
					x1 = row['x1座標'] - UpperLeftCorner_coordinate[0] + 35
					y1 = row['y1座標'] - UpperLeftCorner_coordinate[1] + 5
					x2 = row['x2座標'] - UpperLeftCorner_coordinate[0] + 35
					y2 = row['y2座標'] - UpperLeftCorner_coordinate[1] + 5
					new_square = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
					Squares.append(new_square)
	else:
		for index, row in data.iterrows():
			# 如果序號在correct_coordinates中，繪製紅色方框
			for coord in correct_coordinates:
				if int(row['新序號']) == int(coord[0]) and int(row['新x座標']) == int(coord[1]) and int(row['新y座標']) == int(coord[2]):
					x1 = row['x1座標'] - UpperLeftCorner_coordinate[0] + 35
					y1 = row['y1座標'] - UpperLeftCorner_coordinate[1] + 5
					x2 = row['x2座標'] - UpperLeftCorner_coordinate[0] + 35
					y2 = row['y2座標'] - UpperLeftCorner_coordinate[1] + 5

					new_square = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
					Squares.append(new_square)
	
	for square in Squares:
		draw.polygon(square, outline="red", width=3)
			
	# 儲存結果圖片
	if model_or_examinee == 'M':
		image.save(file_path + '/' + 'marked_model_image.png')
	else:
		image.save(file_path + '/' + 'marked_examinee_image.png')

	# 顯示圖片（可選）
#	image.show()
	
def get_arguments():
    if len(sys.argv) < 3:
        return None
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    return arg1, arg2
	
def main():
	global file_path, model_or_examinee
	arguments = get_arguments()
	if arguments is not None:
		arg1, arg2 = arguments
		model_or_examinee = arg1
		file_path = arg2
	else:
		file_path = 'model'
	
	DrawSquare()

if __name__ == "__main__":
	main()
