import os
import sys

# 輸出路徑
outputfile_path3 = None

class Element:
	def __init__(self, a, b, c, d, e, f):
		self.sequence = a
		self.x1 = b
		self.y1 = c
		self.x2 = d
		self.y2 = e
		self.word = f
		self.middle_x = (b + d) / 2
		self.middle_y = (c + e) / 2

class Element2D:
	def __init__(self, a=0, b=0, c=0, d=""):
		self.sequence = a
		self.x = b
		self.y = c
		self.word = d

def get_arguments():
    if len(sys.argv) < 3:
        return None
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    return arg1, arg2

def is_integer(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def index_trans(window_name):
	ELEMENT = []
	ELEMENT_2D = []
	element_x2 = []
	element_y2 = []
	word_to_sequence = {}  # 用來映射 word 到 sequence 的字典

	inputfile_path = "1-2.txt"
	outputfile_path = "2-3model.txt"
	outputfile_path2 = "model.txt"

	# 從文件讀取原始元素數據，並解析每一行
	with open(inputfile_path, "r", encoding='utf-8') as file:
		lines = file.readlines()

	# 解析每一行，將合法的原始元素添加到 ELEMENT 列表中
	for temp_line in lines:
		elements = temp_line.strip().split('@')

		if len(elements) == 5:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements)):
				ELEMENT.append(Element(int(elements[0]), float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), ""))

		if len(elements) == 6:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements[:5])) and elements[5] != "(null)" and elements[5] != window_name and elements[5] != "DataGridView" and elements[5] != "最大化" and elements[5] != "最小化"  and elements[5] != "系統" and elements[5] != "關閉":
				# 如果相同的 word 已經在字典中，則使用之前的 sequence
				if elements[5] in word_to_sequence:
					sequence = word_to_sequence[elements[5]]
				else:
					# 否則創建一個新的 sequence，並將 word 映射到 sequence
					sequence = len(word_to_sequence) + 1
					word_to_sequence[elements[5]] = sequence

				ELEMENT.append(Element(sequence, float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), elements[5]))

	# 提取原始元素的 x2 和 y2 值
	for elem in ELEMENT:
		element_x2.append(elem.x2)
		element_y2.append(elem.y2)
		ELEMENT_2D.append(Element2D())

	element_x2 = sorted(set(element_x2))
	element_y2 = sorted(set(element_y2))

	coordinate_x = 1
	placed_ELEMENT = [False] * (len(ELEMENT) + 5)
	for i, x2 in enumerate(element_x2):
		have_element = False
		for j, elem in enumerate(ELEMENT):
			if elem.middle_x <= x2 and not placed_ELEMENT[j]:
				ELEMENT_2D[j].sequence = elem.sequence
				ELEMENT_2D[j].x = coordinate_x
				ELEMENT_2D[j].word = elem.word
				placed_ELEMENT[j] = True
				have_element = True
		if have_element:
			coordinate_x += 1

	coordinate_y = 1
	placed_ELEMENT = [False] * (len(ELEMENT) + 5)
	for i, y2 in enumerate(element_y2):
		have_element = False
		for j, elem in enumerate(ELEMENT):
			if elem.middle_y <= y2 and not placed_ELEMENT[j]:
				ELEMENT_2D[j].y = coordinate_y
				placed_ELEMENT[j] = True
				have_element = True
		if have_element:
			coordinate_y += 1

	# 按照 sequence 對 ELEMENT_2D 列表進行排序
	ELEMENT_2D.sort(key=lambda x: x.sequence)
	
	# 按照 sequence 對 ELEMENT 列表進行排序
	ELEMENT.sort(key=lambda x: x.sequence)
	
	# 將轉換後的二維元素數據輸出到文件
	with open(outputfile_path, "w", encoding='utf-8') as output_file:
		for elem in ELEMENT_2D:
			output_file.write(f"{elem.sequence}@{elem.x}@{elem.y}@{elem.word}\n")

	# 將修改後的原始元素數據輸出到文件
	with open(outputfile_path2, "w", encoding='utf-8') as output_file2, open(outputfile_path3, "w", encoding='utf-8') as output_file3:
		for elem in ELEMENT:
			x1_str = str(int(elem.x1)) if elem.x1.is_integer() else str(elem.x1)
			y1_str = str(int(elem.y1)) if elem.y1.is_integer() else str(elem.y1)
			x2_str = str(int(elem.x2)) if elem.x2.is_integer() else str(elem.x2)
			y2_str = str(int(elem.y2)) if elem.y2.is_integer() else str(elem.y2)
			output_file2.write(f"{elem.sequence}@{x1_str}@{y1_str}@{x2_str}@{y2_str}@{elem.word}\n")
			output_file3.write(f"{elem.sequence}@{x1_str}@{y1_str}@{x2_str}@{y2_str}@{elem.word}\n")

def main():
	global outputfile_path3
	# 使用 get_arguments 函數獲取命令行參數
	arguments = get_arguments()
	# 檢查是否成功獲取參數
	if arguments is not None:
		arg1, arg2 = arguments
		Window_Name = arg1
		outputfile_path3 = arg2 + '/sorted_original_data.txt'
	else:
		Window_Name = 'CardGame'
	
	index_trans(Window_Name)


if __name__ == "__main__":
	main()
