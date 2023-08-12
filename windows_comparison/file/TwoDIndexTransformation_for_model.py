import os
import sys

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

def index_trans(window_name):
	ELEMENT = []
	ELEMENT_2D = []
	element_x2 = []
	element_y2 = []

	inputfile_path = "1-2.txt"
	outputfile_path = "2-3model.txt"
	outputfile_path2 = "model.txt"

	with open(inputfile_path, "r", encoding='utf-8') as file:
		lines = file.readlines()

	for temp_line in lines:
		elements = temp_line.strip().split('@')

		if len(elements) == 5:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements)):
				ELEMENT.append(Element(int(elements[0]), float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), ""))

		if len(elements) == 6:
			if all(is_integer(e) if i == 0 else is_float(e) for i, e in enumerate(elements[:5])) and elements[5] != "(null)" and elements[5] != window_name and elements[5] != "DataGridView" and elements[5] != "最大化" and elements[5] != "最小化" and elements[5] != "關閉":
				ELEMENT.append(Element(int(elements[0]), float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]), elements[5]))

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

	with open(outputfile_path, "w", encoding='utf-8') as output_file:
		for elem in ELEMENT_2D:
			output_file.write(f"{elem.sequence}@{elem.x}@{elem.y}@{elem.word}\n")

	with open(outputfile_path2, "w", encoding='utf-8') as output_file2:
		for elem in ELEMENT:
			x1_str = str(int(elem.x1)) if elem.x1.is_integer() else str(elem.x1)
			y1_str = str(int(elem.y1)) if elem.y1.is_integer() else str(elem.y1)
			x2_str = str(int(elem.x2)) if elem.x2.is_integer() else str(elem.x2)
			y2_str = str(int(elem.y2)) if elem.y2.is_integer() else str(elem.y2)
			output_file2.write(f"{elem.sequence}@{x1_str}@{y1_str}@{x2_str}@{y2_str}@{elem.word}\n")


def main():
	Window_Name = get_argument()
	if Window_Name is None:
		Window_Name = 'CardGame'
	index_trans(Window_Name)


if __name__ == "__main__":
	main()
