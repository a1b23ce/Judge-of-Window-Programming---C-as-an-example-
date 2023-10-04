import numpy as np
from pulp import *
output_file_path = 'result.txt'
input_file_path1 = '2-3model.txt'
input_file_path2 = '2-3examinee.txt'
total_objects = 100  # 總物件對數

'''
def calculate_similarity(T, x_values):
	similarity = 0
	for i in range(len(T)):
		for j in range(len(T)):
			if j > i and x_values[i][j].varValue == 1:
				# 计算相似度的逻辑，你可以根据需要自定义
				# 在這裡計算相似度，並將其添加到similarity中
				similarity += 1  # 假設相似度計算方式為簡單的計數
	return similarity
'''
# 判斷是否為相似的物件對


def is_similar(x_coord1, y_coord1, x_coord2, y_coord2):
	return abs(x_coord1 - x_coord2) < 2 and abs(y_coord1 - y_coord2) < 2


def TLCS(window1, window2):
	# Combine data from both windows
	T = window1 + window2

	# Create a binary variable for each pair of rows
	nrow = len(T)
	x = [[LpVariable(f'x_{i}_{j}', 0, 1, LpBinary)
		  for j in range(nrow)] for i in range(nrow)]

	# Create the LP problem
	prob = LpProblem("TLCS", LpMaximize)

	# Add constraints
	for i in range(nrow):
		for j in range(nrow):
			if j > i:
				prob += x[i][j] + x[j][i] <= 1
				if T[i][3] == T[j][3]:
					prob += x[i][j] == 1
				if T[i][2] == T[j][2] and T[i][3] == T[j][3]:
					prob += x[j][i] == 1
				if T[i][0] < T[j][0] and T[i][1] < T[j][1] and T[i][2] > T[j][2]:
					prob += x[i][j] == 1
				if T[i][0] < T[j][0] and T[i][1] < T[j][1] and T[i][3] > T[j][3]:
					prob += x[j][i] == 1
				if T[i][0] < T[j][0] and T[i][1] > T[j][1] and T[i][2] > T[j][2]:
					prob += x[i][j] == 1
				if T[i][0] < T[j][0] and T[i][1] > T[j][1] and T[i][3] < T[j][3]:
					prob += x[j][i] == 1
				if T[i][0] < T[j][0] and T[i][1] == T[j][1] and T[i][2] >= T[j][2]:
					prob += x[i][j] == 1
				if T[i][0] == T[j][0] and T[i][1] < T[j][1] and T[i][3] >= T[j][3]:
					prob += x[j][i] == 1

	# Set the objective function
	prob += lpSum([x[i][j] for i in range(nrow) for j in range(nrow) if j > i])

	# Solve the problem
	prob.solve()

	# Display the results
	'''for i in range(nrow):
		for j in range(nrow):
			if j > i and value(x[i][j]) == 1:
				print(f'Object {T[i][3]} in both windows')
				print(f'Coordinates: ({T[i][1]}, {T[i][2]})')
				print('---')
			continue
	'''

	similar_pairs = []  # 用來存儲相似的物件對

	# 遍歷所有可能的物件對
	for i in range(nrow):
		for j in range(nrow):
			if j > i and T[i][3] == T[j][3]:  # 只有相同文字內容的物件才比較相似度
				prob += x[i][j] + x[j][i] <= 1
				if is_similar(T[i][1], T[i][2], T[j][1], T[j][2]):
					prob += x[i][j] == 1
					similar_pairs.append((i, j))  # 將相似的物件對加入列表

	# 計算相似度百分比
	similar_objects = len(similar_pairs)  # 相似的物件對數
	similarity_percentage = (similar_objects / total_objects) * 100

	# 最後輸出相似的物件對及其相似度
	print("Similar Pairs:")
	for i, j in similar_pairs:
		similarity = 1  # 相似度為1，因為滿足相似的條件
		print(f"Object {i+1} and Object {j+1-33}: Similarity = {similarity}")

	print(f"Similarity Percentage: {similarity_percentage:.2f}%")
	
	# Output results to a file	
	with open(output_file_path, 'w', encoding='utf-8') as result_file:
		"""
		result_file.write("Similar Pairs:\n")
		for i, j in similar_pairs:
			similarity = 1  # Similarity is assumed to be 1
			result_file.write(f"Object {i+1} and Object {j+1-33}: Similarity = {similarity}\n")
		"""
		result_file.write(f"{similarity_percentage:.2f}%\n")
	print(f"Results have been saved to '{output_file_path}'.")


def read_data_from_file(file_path):
	with open(file_path, 'r', encoding='utf-8') as file:
		lines = file.readlines()
	data = [line.strip().split('@') for line in lines]
	return [[int(row[0]), int(row[1]), int(row[2]), row[3]] for row in data]


if __name__ == '__main__':
	window1 = read_data_from_file(input_file_path1)
	window2 = read_data_from_file(input_file_path2)
	total_objects = len(window1)			#讓總元件數跟2-3model.txt的元件數相同
	TLCS(window1, window2)
