import itertools
from itertools import combinations
import time
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

def choose_rule(choice):
	if choice == 2:
		return is_ENL
	elif choice == 3:
		return is_LOL
	elif choice == 4:
		return is_LOE
	else:
		return is_ENE

# 讀取兩組測資
d1 = []
d2 = []

total_nodes_visited = 0

class MaximumSimilarityFound(Exception):
	pass

class BadaccuracyFound(Exception):
	pass

def find_similar_objects(data1, data2, rule):
	similar_objects = []
	max_similarity = 0
	total_objects = len(data1)

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

	dp_cache = {}

	def dfs(index, current_combo):
		global total_nodes_visited
		if index > max(len(data1), len(data2)):
#			print("相似度過低")
			print("Similarity is too low.")
			raise BadaccuracyFound
		nonlocal max_similarity, similar_objects

		# Convert the current combo to a tuple to use as a cache key
		current_combo_key = tuple(current_combo)

		# Check if the current combo is already calculated
		if current_combo_key in dp_cache:
			return dp_cache[current_combo_key]

		# 檢查是否需要提前終止搜索
		if len(current_combo) <= len(similar_objects) and max_similarity != 0 and len(similar_objects) >= max(len(data1), len(data2))/2:
			# 如果當前分支的深度小於等於先前記錄的最大深度，提前終止搜索
			return False

		if index == len(data1):
			total_nodes_visited += 1
			# Check if the current combination satisfies the rules
			valid_combo = True
			similarity_count = 0
			for pair1, pair2 in itertools.combinations(current_combo, 2):
				(_, i1, j1, text1a) = pair1
				(_, i2, j2, text2a) = pair2

				# Find corresponding pairs in data2
				matching_pair_a = next(((p1, q1, p2, q2) for (id1b, p1, q1, text1b) in data2 for (id2b, p2, q2, text2b) in data2 if (
					(text1a == text1b) and (text2a == text2b) and rule(i1, j1, i2, j2, p1, q1, p2, q2))), None)

				matching_pair_b = next(((p1, q1, p2, q2) for (id1b, p1, q1, text1b) in data2 for (id2b, p2, q2, text2b) in data2 if (
					(text1a == text1b) and (text2a == text2b) and rule(i2, j2, i1, j1, p2, q2, p1, q1))), None)

				if matching_pair_a is None and matching_pair_b is None:
					valid_combo = False
					break

				similarity_count += 1

			if valid_combo and similarity_count > max_similarity:
				max_similarity = similarity_count
				similar_objects = current_combo.copy()

#				print(f"Found similar objects: {similar_objects}")

			# Save the result in the cache
			dp_cache[current_combo_key] = valid_combo

			# If we found a solution with the maximum similarity, stop searching
			if len(similar_objects) == total_objects and max_similarity == (total_objects * (total_objects - 1)) // 2:
#				print("Found the maximum similarity!")
				raise MaximumSimilarityFound("Maximum similarity found")
			return valid_combo

		# Include the current item in the combination
		result_with_current = dfs(index + 1, current_combo + [data1[index]])

		# Skip the current item in the combination
		result_without_current = dfs(index + 1, current_combo)

		# Save the result in the cache
		dp_cache[current_combo_key] = result_with_current or result_without_current

		return result_with_current or result_without_current

	dfs(0, [])

	return similar_objects

def get_argument():
	if len(sys.argv) < 2:
		return None
	return sys.argv[1]

def main():
	global file_path, total_nodes_visited
	file_path = get_argument()
	if file_path is None:
		file_path = 'model'
	similar_objects = []
	
	with open("2-3model.txt", "r", encoding="utf-8") as file1, open("2-3examinee.txt", "r", encoding="utf-8") as file2:
		for line in file1:
			d1.append(line.strip().split('@'))

		for line in file2:
			d2.append(line.strip().split('@'))
	
	longest_similar_objects = []		# 儲存最長的 similar_objects
	data_list = []						# 儲存 similarity_percentage, total_nodes_visited, elapsed_time
	largest_similarity_percentage = 0	# 儲存最高相似度
	for i in range(1, 5):
		selected_rule = choose_rule(i)
		# 歸零
		total_nodes_visited = 0
		similar_objects = []
		
		start_time = time.time()
		try:
			similar_objects = find_similar_objects(d2, d1, selected_rule)
		except MaximumSimilarityFound as e:
			similar_objects = d2
#			print(e)
		except BadaccuracyFound as f:
			similar_objects = []
#			print(f)
		end_time = time.time()
		
		elapsed_time = end_time - start_time
		similarity_percentage = len(similar_objects) / max(len(d1), len(d2)) * 100
		data_list.append((similarity_percentage, total_nodes_visited, elapsed_time))
		
		# 檢查是否是最高的相似度
		if similarity_percentage >= largest_similarity_percentage:
			largest_similarity_percentage = similarity_percentage
			longest_similar_objects = similar_objects				# 不一定是最長
				
	# 輸出相似度
	with open('result.txt', 'w', encoding='utf-8') as result_file:
		if largest_similarity_percentage >= 50:
			result_file.write(f"{largest_similarity_percentage:.2f}%\n")
		else:
			result_file.write(f"<50%\n")
	
	# 輸出相似物件
	with open(file_path + '/' + "correct_examinee.txt", "w", encoding='utf-8') as output_file:
		for item in longest_similar_objects:
			output_file.write(f"{item[0]} {item[1]} {item[2]}\n")
	# 輸出node數跟運行時間
	with open('statistics.txt', 'a', encoding='utf-8') as statistics_file:
		Student_ID = file_path[len("examinee\\"):]	# 去除file_path前面的examinee\
		statistics_file.write(f"{Student_ID} ")
		for data in data_list:
			similarity_percentage, total_nodes_visited, elapsed_time = data
			statistics_file.write(f"{similarity_percentage:2f} {total_nodes_visited} {elapsed_time:4f} ")
		statistics_file.write(f"\n")

if __name__ == "__main__":
	main()
