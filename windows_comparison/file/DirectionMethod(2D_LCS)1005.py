import itertools
from itertools import combinations
import sys
# 定義判定方式
# v

file_path = None

def is_ENE(i1, j1, i2, j2, p1, q1, p2, q2):
	if i1 < i2 and j1 < j2:
		return p1 <= p2 and q1 <= q2
	elif i1 < i2 and j1 > j2:
		return p1 <= p2 and q1 >= q2
	elif i1 < i2 and j1 == j2:
		return p1 <= p2
	elif i1 == i2 and j1 < j2:
		return q1 <= q2
	else:
		return False
# X


def is_ENL(i1, j1, i2, j2, p1, q1, p2, q2):
	if i1 < i2 and j1 < j2:
		return p1 <= p2 and q1 <= q2
	elif i1 < i2 and j1 > j2:
		return p1 <= p2 and q1 >= q2
	elif i1 < i2 and j1 == j2:
		return p1 < p2
	elif i1 == i2 and j1 < j2:
		return q1 < q2
	else:
		return False
# X


def is_LOL(i1, j1, i2, j2, p1, q1, p2, q2):
	if i1 < i2 and j1 < j2:
		return p1 < p2 or q1 < q2
	elif i1 < i2 and j1 > j2:
		return p1 < p2 or q1 > q2
	elif i1 < i2 and j1 == j2:
		return p1 < p2
	elif i1 == i2 and j1 < j2:
		return q1 < q2
	else:
		return False
# V


def is_LOE(i1, j1, i2, j2, p1, q1, p2, q2):
	if i1 < i2 and j1 < j2:
		return p1 < p2 or q1 < q2
	elif i1 < i2 and j1 > j2:
		return p1 < p2 or q1 > q2
	elif i1 < i2 and j1 == j2:
		return p1 <= p2
	elif i1 == i2 and j1 < j2:
		return q1 <= q2
	else:
		return False


# 讀取兩組測資
d1 = []
d2 = []


def find_similar_objects(data1, data2):
	similar_objects = []
	max_similarity = 0

	def update_text_content(data):
		# Helper function to update text content with a numeric suffix
		text_counts = {}
		updated_data = []

		for item in data:
			_, _, _, text = item
			if text in text_counts:
				text_counts[text] += 1
				new_text = f"{text}({text_counts[text]})"
			else:
				new_text = text
				text_counts[text] = 1

			updated_data.append((item[0], item[1], item[2], new_text))

		return updated_data

	data1 = update_text_content(data1)
	data2 = update_text_content(data2)
	dp = {}

	def dfs(index, current_combo):
		nonlocal max_similarity, similar_objects, dp

		if index == len(data1):
			# Check if the current combination satisfies the rules
			valid_combo = True
			similarity_count = 0
			for pair1, pair2 in combinations(current_combo, 2):
				(id1a, i1, j1, text1a) = pair1
				(id2a, i2, j2, text2a) = pair2
				
				# Find corresponding pairs in data2
				matching_pair_a = next(((p1, q1, p2, q2) for (id1b, p1, q1, text1b) in data2 for (id2b, p2, q2, text2b) in data2 if (
					(text1a == text1b) and (text2a == text2b) and is_LOL(i1, j1, i2, j2, p1, q1, p2, q2))), None)

				matching_pair_b = next(((p1, q1, p2, q2) for (id1b, p1, q1, text1b) in data2 for (id2b, p2, q2, text2b) in data2 if (
					(text1a == text1b) and (text2a == text2b) and is_LOL(i2, j2, i1, j1, p2, q2, p1, q1))), None)

				if matching_pair_a is None and matching_pair_b is None:
					valid_combo = False
					break

				similarity_count += 1

			if valid_combo and similarity_count > max_similarity:
				max_similarity = similarity_count
				similar_objects = current_combo.copy()
				print(similar_objects)
				print("Found an ans")
				print()

			return

		# Include the current item in the combination
		dfs(index + 1, current_combo + [data1[index]])

		# Skip the current item in the combination
		dfs(index + 1, current_combo)

	dfs(0, [])

	# Output the result to a txt file
	with open(file_path + '/' + "correct_examinee.txt", "w") as output_file:
		output_file.write(" ".join(str(item[0]) for item in similar_objects))

	return similar_objects

def get_argument():
	if len(sys.argv) < 2:
		return None
	return sys.argv[1]
	
def main():
	global file_path
	file_path = get_argument()
	if file_path is None:
		file_path = 'model'

	with open("2-3model.txt", "r", encoding="utf-8") as file1, open("2-3examinee.txt", "r", encoding="utf-8") as file2:
		for line in file1:
			d1.append(line.strip().split('@'))

		for line in file2:
			d2.append(line.strip().split('@'))

	# 找出相似物件
	similar_objects = find_similar_objects(d2, d1)
	print("相似物件：", similar_objects)
	if(len(d1)>=len(d2)):
		num_of_objects = len(d1)
	else:
		num_of_objects = len(d2)
	similarity_percentage = len(similar_objects) / num_of_objects * 100
	with open('result.txt', 'w', encoding='utf-8') as result_file:
		result_file.write(f"{similarity_percentage:.2f}%\n")
		print("相似度：", similarity_percentage, "%")

if __name__ == "__main__":
	main()
	
