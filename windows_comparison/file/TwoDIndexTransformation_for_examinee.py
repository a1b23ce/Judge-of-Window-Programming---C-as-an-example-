import os
import sys

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

def get_argument():
	if len(sys.argv) < 2:
		return None
	return sys.argv[1]

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

	with open(inputfile_path, "r", encoding='utf-8') as file:
		lines = file.readlines()

	for temp_line in lines:
		elements = temp_line.strip().split('@')

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
			
	with open(inputfile_path2, "r", encoding='utf-8') as file:
		lines = file.readlines()

	for temp_line in lines:
		elements = temp_line.strip().split('@')

		if len(elements) == 6:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements[:5])) and elements[5] != "(null)" and elements[5] != window_name and elements[5] != "DataGridView" and elements[5] != "最大化" and elements[5] != "最小化" and elements[5] != "系統" and elements[5] != "關閉":
				ELEMENT2.append(Element(int(elements[0]), float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), elements[5]))
		if len(elements) == 6:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements[:5])) and elements[5] != "(null)" and elements[5] != window_name and elements[5] != "DataGridView" and elements[5] != "最大化" and elements[5] != "最小化"  and elements[5] != "系統" and elements[5] != "關閉":
				# 如果相同的 word 已經在字典中，則使用之前的 sequence2
				if elements[5] in word_to_sequence2:
					sequence2 = word_to_sequence2[elements[5]]
				else:
					# 否則創建一個新的 sequence2，並將 word 映射到 sequence2
					sequence2 = len(word_to_sequence2) + 1
					word_to_sequence2[elements[5]] = sequence2

				ELEMENT2.append(Element(sequence, float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), elements[5]))


	placed_ELEMENT2 = [False] * (len(ELEMENT2) + 15)

	for elem in ELEMENT:
		for j, elem2 in enumerate(ELEMENT2):
			if elem2.word == elem.word and not placed_ELEMENT2[j]:
				ELEMENT3.append(Element(elem.index, elem2.x1, elem2.y1, elem2.x2, elem2.y2, elem2.word))
				placed_ELEMENT2[j] = True
				break

	element_num = ELEMENT[-1].index + 1
	for i, elem2 in enumerate(ELEMENT2):
		if not placed_ELEMENT2[i]:
			ELEMENT3.append(Element(element_num, elem2.x1, elem2.y1, elem2.x2, elem2.y2, elem2.word))
			element_num += 1

def index_trans(ELEMENT):
	ELEMENT_2D = []
	element_x2 = []
	element_y2 = []

	outputfile_path = "2-3examinee.txt"

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
				ELEMENT_2D[j].index = elem.index
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
	ELEMENT_2D.sort(key=lambda x: x.index)
	
	with open(outputfile_path, "w", encoding='utf-8') as output_file:
		for elem in ELEMENT_2D:
			output_file.write(f"{elem.index}@{elem.x}@{elem.y}@{elem.word}\n")

def main():
	ELEMENT = []
	Window_Name = get_argument()
	if Window_Name is None:
		Window_Name = 'CardGame'
	fix_seq(ELEMENT, Window_Name)
	index_trans(ELEMENT)
	
if __name__ == "__main__":
	main()
