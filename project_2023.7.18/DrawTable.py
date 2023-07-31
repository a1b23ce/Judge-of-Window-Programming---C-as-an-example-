import matplotlib.pyplot as plt
import pandas as pd
import random

# 讀取座標數據
data = pd.read_csv("2-3.txt", delimiter='@', header=None, names=['序號', 'x座標', 'y座標', '文字'])  # 使用@符號作為分隔符

# 設定表格大小
num_rows = 15
num_cols = 15

# 建立一個2D List，用來存放每個格子的數字
numbers = [[random.randint(1, 100) for _ in range(num_cols)] for _ in range(num_rows)]

# 建立一個新的figure
fig, ax = plt.subplots()

# 繪製表格
for i in range(num_rows):
    for j in range(num_cols):
        # 計算每個格子的左上角座標
        x = j
        y = num_rows - i - 1
        
        # 設定每個格子的大小為1x1，填滿白色
        ax.add_patch(plt.Rectangle((x, y), 1, 1, facecolor='white', edgecolor='black'))
        
        # 在最左邊一列和最上面一行顯示數字
        if i == 0:
			#ax.text(x + 0.5, y + 1.2, str(j), ha='center', va='center')
            ax.text(x + 0.5, y + 1.2, str(j+1), ha='center', va='center')
        if j == 0:
			#ax.text(x - 0.5, y + 0.5, str(i), ha='center', va='center')
            ax.text(x - 0.5, y + 0.5, str(i+1), ha='center', va='center')

# 使用scatter()繪製序號
for index, row in data.iterrows():
    #x = row['x座標']
    #y = num_rows - row['y座標'] - 1
    x = row['x座標'] - 1
    y = num_rows - row['y座標']
    ax.text(x + 0.5, y + 0.5, str(row['序號']), ha='center', va='center')

# 設定x軸和y軸的範圍
ax.set_xlim(0, num_cols)
ax.set_ylim(0, num_rows)

# 移除x軸和y軸的刻度
ax.set_xticks([])
ax.set_yticks([])

# 顯示圖表
plt.show()
