import tkinter as tk
from tkinter import PhotoImage
import subprocess
from PIL import Image, ImageTk
import importlib
import threading

class MainFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.configure(width=800, height=500)  # Set the frame size

		# 載入背景圖片
		background_image = Image.open("file/cool technology smart robot robot_941684(圖片來源於pngtree.com).jpg")
		background_image = background_image.resize((800, 500), Image.Resampling.LANCZOS)  # 設定新的大小
		background_photo = ImageTk.PhotoImage(background_image)

		# 在畫布上顯示背景圖片
		background_label = tk.Label(self, image=background_photo)
		background_label.image = background_photo
		background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
		
		# 按按鈕後被執行的檔案名稱
		model = 'windows_comparison_model.py'
		examinee = 'windows_comparison_examinee.py'
		
		# 更改按鈕行為與內容
		button1 = tk.Button(self, text="運行標準答案", width=15, height=2, command=lambda: self.execute_and_check(model))
		button2 = tk.Button(self, text="運行考生答案", width=15, height=2, command=lambda: self.execute_and_check(examinee))
		button3 = tk.Button(self, text="顯示結果", width=15, height=2, command=self.show_capture_result)
		
#		button1.place(x=100, y=100)  # 設置按鈕的位置 (x, y)
		button1.pack(side="top", padx=10, pady=80)
		button1.config(font=("微軟黑正體", 16))
		button2.pack(side="top", padx=10, pady=0)
		button2.config(font=("微軟黑正體", 16))
		button3.pack(side="top", padx=10, pady=80)
		button3.config(font=("微軟黑正體", 16))


	def show_capture_result(self):
		self.controller.show_frame(CaptureResult)

	def execute_and_check(self, file_name):
		def execute():
			try:
	#			result = subprocess.run(["python", file_name], capture_output=True, text=True)
				# 使用 subprocess.PIPE 捕獲標準輸出和標準錯誤
				result = subprocess.run(["python", file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
				
				# 獲取標準輸出和標準錯誤的內容
				stdout = result.stdout
				stderr = result.stderr
				
				if result.returncode == 0:
					print(f"{file_name} executed successfully.")
				else:
					print(f"Error executing {file_name}. Return code: {result.returncode}")
				
				print(stdout)
				print(stderr)
				
			except Exception as e:
				print(f"Error executing {file_name}: {e}")
		
		# 使用多線程執行 execute 函數
		execution_thread = threading.Thread(target=execute)
		execution_thread.start()
	
class CaptureResult(tk.Frame):
	examinee_number = None
	original_or_transfer = 'O'
	
	def on_select(self, event):
		selected_index = self.listbox.curselection()
		if selected_index:
			selected_item = self.listbox.get(selected_index)
			
			# 刪除百分比部分
			CaptureResult.examinee_number = selected_item.split(' ')[0]
			
#			print(f"Selected item: {CaptureResult.examinee_number}")
			
			if CaptureResult.original_or_transfer == 'O':
				self.show_original_image(CaptureResult.examinee_number)
			elif CaptureResult.original_or_transfer == 'T':
				self.show_transfered_image(CaptureResult.examinee_number)
	
	def load_file_to_listbox(self):
		try:
			with open("examinee_accuracy.txt", "r", encoding="utf-8") as file:
				lines = file.readlines()
				for line in lines:
					# 清除行尾的換行符號並添加到Listbox
					self.listbox.insert(tk.END, line.strip())
		except FileNotFoundError:
			self.listbox.insert(tk.END, "File not found.")
	
	def show_transfered_image(self, folder_path):
		image_path = 'examinee/' + folder_path + '/picture_model.png'
		image2_path = 'examinee/' + folder_path + '/picture_examinee.png'
		image3_path = 'file/image_not_found_1150x647.png'
		try:
			# 打開圖片文件
			image = Image.open(image_path)
			image2 = Image.open(image2_path)

			# 調整圖像大小
			image = image.resize((300, 300), Image.Resampling.LANCZOS)
			image2 = image2.resize((300, 300), Image.Resampling.LANCZOS)

			# 將圖片轉換為Tkinter PhotoImage對象
			tk_image = ImageTk.PhotoImage(image)
			tk_image2 = ImageTk.PhotoImage(image2)

			# 在標籤中顯示圖片
			self.image_label.config(image=tk_image)
			self.image_label.image = tk_image  # 保持對對象的引用，以防止圖片被垃圾回收
			self.image_label2.config(image=tk_image2)
			self.image_label2.image = tk_image2  # 保持對對象的引用，以防止圖片被垃圾回收

		except FileNotFoundError:
			# 打開圖片文件
			image3 = Image.open(image3_path)

			# 設定目標大小
			target_width = 300
			target_height = 300

			# 計算縮放比例
			width_ratio = target_width / image3.width
			height_ratio = target_height / image3.height
			min_ratio = min(width_ratio, height_ratio)

			# 調整圖像大小
			new_width = int(image3.width * min_ratio)
			new_height = int(image3.height * min_ratio)
			image3 = image3.resize((new_width, new_height), Image.Resampling.LANCZOS)
			
			# 將圖片轉換為Tkinter PhotoImage對象
			tk_image3 = ImageTk.PhotoImage(image3)

			# 在標籤中顯示圖片
			self.image_label.config(image=tk_image3)
			self.image_label.image = tk_image3  # 保持對對象的引用，以防止圖片被垃圾回收
			self.image_label2.config(image=tk_image3)
			self.image_label2.image = tk_image3  # 保持對對象的引用，以防止圖片被垃圾回收
			
		CaptureResult.original_or_transfer = 'T'
		
			
	def show_original_image(self, folder_path):
		image_path = 'examinee/' + folder_path + '/marked_model_image.png'
		image2_path = 'examinee/' + folder_path + '/marked_examinee_image.png'
		image3_path = 'file/image_not_found_1150x647.png'
		try:
			# 打開圖片文件
			image = Image.open(image_path)
			image2 = Image.open(image2_path)

			# 設定目標大小
			target_width = 300
			target_height = 300

			# 計算縮放比例
			width_ratio = target_width / image.width
			height_ratio = target_height / image.height
			min_ratio = min(width_ratio, height_ratio)

			# 調整圖像大小
			new_width = int(image.width * min_ratio)
			new_height = int(image.height * min_ratio)
			image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
			image2 = image2.resize((new_width, new_height), Image.Resampling.LANCZOS)

			# 將圖片轉換為Tkinter PhotoImage對象
			tk_image = ImageTk.PhotoImage(image)
			tk_image2 = ImageTk.PhotoImage(image2)

			# 在標籤中顯示圖片
			self.image_label.config(image=tk_image)
			self.image_label.image = tk_image  # 保持對對象的引用，以防止圖片被垃圾回收
			self.image_label2.config(image=tk_image2)
			self.image_label2.image = tk_image2  # 保持對對象的引用，以防止圖片被垃圾回收

		except FileNotFoundError:
			# 打開圖片文件
			image3 = Image.open(image3_path)

			# 設定目標大小
			target_width = 300
			target_height = 300

			# 計算縮放比例
			width_ratio = target_width / image3.width
			height_ratio = target_height / image3.height
			min_ratio = min(width_ratio, height_ratio)

			# 調整圖像大小
			new_width = int(image3.width * min_ratio)
			new_height = int(image3.height * min_ratio)
			image3 = image3.resize((new_width, new_height), Image.Resampling.LANCZOS)
			
			# 將圖片轉換為Tkinter PhotoImage對象
			tk_image3 = ImageTk.PhotoImage(image3)

			# 在標籤中顯示圖片
			self.image_label.config(image=tk_image3)
			self.image_label.image = tk_image3  # 保持對對象的引用，以防止圖片被垃圾回收
			self.image_label2.config(image=tk_image3)
			self.image_label2.image = tk_image3  # 保持對對象的引用，以防止圖片被垃圾回收
		
		CaptureResult.original_or_transfer = 'O'
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.configure(width=800, height=500)  # Set the frame size
		
		# 創建Canvas並設定大小
		canvas = tk.Canvas(self, width=800, height=500)
		canvas.pack()
		
		# 載入背景圖片
		self.background_image = Image.open("file/cool technology smart robot robot_941684(圖片來源於pngtree.com).jpg")
		self.background_image = self.background_image.resize((800, 500), Image.Resampling.LANCZOS)  # 設定新的大小
		self.background_photo = ImageTk.PhotoImage(self.background_image)
		
		# 插入圖像到Canvas
		canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

		# 插入文字到Canvas
		canvas.create_text(470, 50, text="結果", font=("微軟黑正體", 30, "bold"), fill="white")
		canvas.create_text(320, 100, text="標準答案", font=("微軟黑正體", 20, "bold"), fill="white")
		canvas.create_text(620, 100, text="考生答案", font=("微軟黑正體", 20, "bold"), fill="white")
		
#		label = tk.Label(self, text="結果", width=10, height=2)
#		label.place(x=410, y=10)
#		label.config(font=("微軟黑正體", 16))
		
#		label2 = tk.Label(self, text="標準答案")
#		label2.place(x=270, y=100)
#		label2.config(font=("微軟黑正體", 16))
		
#		label3 = tk.Label(self, text="考生答案")
#		label3.place(x=580, y=100)
#		label3.config(font=("微軟黑正體", 16))
		
		# 創建Listbox
		self.listbox = tk.Listbox(self, height=40, width=15)
		self.listbox.place(x=10, y=50)
		self.listbox.config(font=("Times New Roman", 14))
		
		# 按鈕：載入成績
		button = tk.Button(self, text="載入成績", width=10, height=1, command=lambda: self.load_file_to_listbox())
		button.place(x=25, y=10)
		button.config(font=("微軟黑正體", 14))
		
		# 按鈕：切換圖片模式
		button = tk.Button(self, text="原始圖像", width=10, height=1, command=lambda: self.show_original_image(CaptureResult.examinee_number))
		button.place(x=355, y=140)
		button.config(font=("微軟黑正體", 14))
		
		button = tk.Button(self, text="二維轉換", width=10, height=1, command=lambda: self.show_transfered_image(CaptureResult.examinee_number))
		button.place(x=480, y=140)
		button.config(font=("微軟黑正體", 14))
		
		# 載入文件內容到Listbox
#		self.load_file_to_listbox()

		# 設置點擊事件的回調函數
		self.listbox.bind("<<ListboxSelect>>", self.on_select)
		
		# 創建一個標籤來顯示圖片
		self.image_label = tk.Label(self, width=300, height=300)
		self.image_label.place(x=160, y=200)
		self.image_label2 = tk.Label(self, width=300, height=300)
		self.image_label2.place(x=480, y=200)
		

class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.geometry("800x500")  # Set the window size

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (MainFrame, CaptureResult):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(MainFrame)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()



if __name__ == "__main__":
	app = App()
	app.mainloop()
	


