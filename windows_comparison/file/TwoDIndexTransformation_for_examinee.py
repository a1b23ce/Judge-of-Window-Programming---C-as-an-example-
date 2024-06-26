import os
import sys

# 輸出路徑
outputfile_path2 = None

class Element:
	def __init__(self, a, b, c, d, e, f):
		self.index = a
		self.x1 = b
		self.y1 = c
		self.x2 = d
		self.y2 = e
		self.word = f
		self.middle_x = (b + d) / 2
		self.middle_y = (c + e) / 2
	
class Element2D:
	def __init__(self, a=0, b=0, c=0, d=""):
		self.index = a
		self.x = b
		self.y = c
		self.word = d

class ElementTrans:
	def __init__(self, a=0, b=0, c=0, d=0, e=0, f="", g=0, h=0, i=0):
		self.index = a
		self.x1 = b
		self.y1 = c
		self.x2 = d
		self.y2 = e
		self.word = f
		self.index_2D = g
		self.x_2D = h
		self.y_2D = i

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

def fix_seq(ELEMENT3, window_name):
	ELEMENT = []
	ELEMENT2 = []
	word_to_sequence = {}  # 用來映射 word 到 sequence 的字典
	word_to_sequence2 = {}

	inputfile_path = "model.txt"
	inputfile_path2 = "1-2.txt"
	
	# 讀取model.txt
	with open(inputfile_path, "r", encoding='utf-8') as file:
		lines = file.readlines()
	
	# 使用 len() 函數計算行數
	model_element_number = len(lines)

	for temp_line in lines:
		elements = temp_line.strip().split('@')

		if len(elements) == 6:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements[:5])) and elements[5] != "(null)" and elements[5] != window_name and elements[5] != "DataGridView" and elements[5] != "最大化" and elements[5] != "最小化"  and elements[5] != "系統" and elements[5] != "關閉":
				ELEMENT.append(Element(int(elements[0]), float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), elements[5]))
	
	# 讀取1-2.txt
	with open(inputfile_path2, "r", encoding='utf-8') as file:
		lines = file.readlines()

	for temp_line in lines:
		elements = temp_line.strip().split('@')

		if len(elements) == 6:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements[:5])) and elements[5] != "(null)" and elements[5] != window_name and elements[5] != "DataGridView" and elements[5] != "最大化" and elements[5] != "最小化"  and elements[5] != "系統" and elements[5] != "關閉":
				# 如果相同的 word 已經在字典中，則使用之前的 sequence2
				if elements[5] in word_to_sequence2:
					sequence2 = word_to_sequence2[elements[5]]
				else:
					# 否則創建一個新的 sequence2，並將 word 映射到 sequence2
					sequence2 = len(word_to_sequence2) + 1
					word_to_sequence2[elements[5]] = sequence2

				ELEMENT2.append(Element(sequence2, float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), elements[5]))
		
	matched_answer = 0
	placed_ELEMENT2 = [False] * (len(ELEMENT2) + 15)	
	for elem in ELEMENT:
		for j, elem2 in enumerate(ELEMENT2):
			if elem2.word == elem.word and not placed_ELEMENT2[j]:
				ELEMENT3.append(Element(elem.index, elem2.x1, elem2.y1, elem2.x2, elem2.y2, elem2.word))
				placed_ELEMENT2[j] = True
				matched_answer += 1
				break
	
	# 處理未對應的元件
	element_num = ELEMENT[-1].index + 1
	for i, elem2 in enumerate(ELEMENT2):
		if not placed_ELEMENT2[i]:
			# 檢查在ELEMENT3中是否有相同文字元件
			word_to_check = elem2.word
			existing_element_index = next((index for index, element in enumerate(ELEMENT3) if element.word == word_to_check), None)
			
			if existing_element_index is not None:
				# 若有相同 'word' 的元素，使用相同 'word' 的元素的索引
				ELEMENT3.append(Element(ELEMENT3[existing_element_index].index, elem2.x1, elem2.y1, elem2.x2, elem2.y2, elem2.word))
			else:
				# 若沒有相同 'word' 的元素，創建新的 'index'，然後加入 ELEMENT3
				ELEMENT3.append(Element(element_num, elem2.x1, elem2.y1, elem2.x2, elem2.y2, elem2.word))
				element_num += 1
	
	ELEMENT3.sort(key=lambda x: x.index)
	
	# 使用 len() 函數計算行數
	examinee_element_number = len(ELEMENT3)
			
	# 比較元素數量，得出最大元素數
	if model_element_number >= examinee_element_number:
		max_num_of_elements = model_element_number
	else:
		max_num_of_elements = examinee_element_number
	
#	with open('matched.txt', 'a', encoding='utf-8') as result_file:
#		result_file.write(f"{matched_answer} / {max_num_of_elements}, {examinee_element_number}\n")
		
	# 如果對到的元件超過一半 回傳True
	if (matched_answer / max_num_of_elements) < 0.5:
		return False
	else:
		return True
	

def index_trans(ELEMENT):
	ELEMENT_2D = []
	ELEMENT_Trans = []
	element_x2 = []
	element_y2 = []

	outputfile_path = "2-3examinee.txt"

	for elem in ELEMENT:
		element_x2.append(elem.x2)
		element_y2.append(elem.y2)
		ELEMENT_2D.append(Element2D())
		ELEMENT_Trans.append(ElementTrans())

	element_x2 = sorted(set(element_x2))
	element_y2 = sorted(set(element_y2))

	coordinate_x = 1
	placed_ELEMENT = [False] * (len(ELEMENT) + 5)
	for i, x2 in enumerate(element_x2):
		have_element = False
		for j, elem in enumerate(ELEMENT):
			if elem.middle_x <= x2 and not placed_ELEMENT[j]:
				ELEMENT_2D[j].index = elem.index
				ELEMENT_2D[j].x = coordinate_x
				ELEMENT_2D[j].word = elem.word
				ELEMENT_Trans[j].index = elem.index
				ELEMENT_Trans[j].x1 = elem.x1
				ELEMENT_Trans[j].y1 = elem.y1
				ELEMENT_Trans[j].x2 = elem.x2
				ELEMENT_Trans[j].y2 = elem.y2
				ELEMENT_Trans[j].word = elem.word
				ELEMENT_Trans[j].index_2D = elem.index
				ELEMENT_Trans[j].x_2D = coordinate_x
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
				ELEMENT_Trans[j].y_2D = coordinate_y
				placed_ELEMENT[j] = True
				have_element = True
		if have_element:
			coordinate_y += 1
	
	
	# 按照 sequence 對 ELEMENT_2D 列表進行排序
	ELEMENT_2D.sort(key=lambda x: x.index)
	'''
	# 原先輸出
	with open(outputfile_path, "w", encoding='utf-8') as output_file:
		for elem in ELEMENT_2D:
			output_file.write(f"{elem.index}@{elem.x}@{elem.y}@{elem.word}\n")
	'''		
	'''
	# 測試用
	with open('1' + outputfile_path, "w", encoding='utf-8') as output_file:
		for elem in ELEMENT_2D:
			output_file.write(f"{elem.index}@{elem.x}@{elem.y}@{elem.word}\n")
	'''
	# 定義一個函數來處理文字相同元件中的 index 最小值
	def set_min_index_for_same_text_elements(elements):
		# 創建一個字典來存儲每個文字對應的最小 index 元素
		text_min_index_map = {}
		
		# 遍歷元素，更新文字對應的最小 index
		for elem in elements:
			text = elem.word
			index = elem.index
			if text not in text_min_index_map or index < text_min_index_map[text].index:
				text_min_index_map[text] = elem

		# 設置每個元素的 index 為文字相同中的最小 index
		for elem in elements:
			elem.index = text_min_index_map[elem.word].index

	# 定義一個自訂的排序函數，按照 sequence、x、y 來排序
	def ELEMENT_2D_custom_sort(elem):
		return (elem.index, elem.x, elem.y)
	# 使用 ELEMENT_2D_custom_sort() 函數來排序 ELEMENT_2D 列表
	ELEMENT_2D.sort(key=ELEMENT_2D_custom_sort)
	
	# 開啟文件並將排序後的元素輸出
	with open(outputfile_path, "w", encoding='utf-8') as output_file:
		for elem in ELEMENT_2D:
			output_file.write(f"{elem.index}@{elem.x}@{elem.y}@{elem.word}\n")
	
	# 定義一個自訂的排序函數，按照 sequence、x_2D、y_2D 來排序
	def ELEMENT_Trans_custom_sort(elem):
		return (elem.index_2D, elem.x_2D, elem.y_2D)
	# 使用 sorted() 函數來排序 ELEMENT_Trans 列表
	ELEMENT_Trans.sort(key=ELEMENT_Trans_custom_sort)
	
	# 將修改後的原始元素資料輸出到sorted_original_data2.txt，並附加 ELEMENT_2D 的 sequence, x, y
	with open(outputfile_path2, "w", encoding='utf-8') as output_file2:
		for elem in ELEMENT_Trans:
			x1_str = str(int(elem.x1)) if elem.x1.is_integer() else str(elem.x1)
			y1_str = str(int(elem.y1)) if elem.y1.is_integer() else str(elem.y1)
			x2_str = str(int(elem.x2)) if elem.x2.is_integer() else str(elem.x2)
			y2_str = str(int(elem.y2)) if elem.y2.is_integer() else str(elem.y2)
			output_file2.write(f"{elem.index}@{x1_str}@{y1_str}@{x2_str}@{y2_str}@{elem.word}@{elem.index_2D}@{elem.x_2D}@{elem.y_2D}\n")
	
def main():
	ELEMENT = []
	global outputfile_path2
	# 使用 get_arguments 函數獲取命令行參數
	arguments = get_arguments()
	# 檢查是否成功獲取參數
	if arguments is not None:
		arg1, arg2 = arguments
		Window_Name = arg1
		outputfile_path2 = arg2 + '/sorted_original_data.txt'
	else:
		Window_Name = 'CardGame'
	
	# 如果對到的元件超過一半 回傳True
	if fix_seq(ELEMENT, Window_Name):
		print("MatchedElementGreaterThanHalf", end='')
		index_trans(ELEMENT)
	else:
		print("MatchedElementLessThanHalf", end='')
		
	
if __name__ == "__main__":
	main()
