import tkinter as tk
import subprocess
from PIL import Image, ImageTk
import importlib

class MainFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.configure(width=800, height=500)  # Set the frame size

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
		try:
			result = subprocess.run(["python", file_name], capture_output=True, text=True)
			
			if result.returncode == 0:
				print(f"{file_name} executed successfully.")
			else:
				print(f"Error executing {file_name}. Return code: {result.returncode}")
		except Exception as e:
			print(f"Error executing {file_name}: {e}")

class CaptureResult(tk.Frame):
	def on_select(self, event):
		selected_index = self.listbox.curselection()
		if selected_index:
			selected_item = self.listbox.get(selected_index)
			
			# 刪除百分比部分
			examinee_number = selected_item.split(' ')[0]
			
			print(f"Selected item: {examinee_number}")
			
			self.show_image(examinee_number)
	
	def load_file_to_listbox(self):
		try:
			with open("examinee_accuracy.txt", "r") as file:
				lines = file.readlines()
				for line in lines:
					# 清除行尾的換行符號並添加到Listbox
					self.listbox.insert(tk.END, line.strip())
		except FileNotFoundError:
			self.listbox.insert(tk.END, "File not found.")
	
	def show_image(self, folder_path):
		image_path = 'examinee/' + folder_path + '/picture_model.png'
		image2_path = 'examinee/' + folder_path + '/picture_examinee.png'
		try:
			# 打開圖片文件
			image = Image.open(image_path )
			image2 = Image.open(image2_path)

			# 調整圖像大小（此處設置為200x200像素）
			image = image.resize((400, 300), Image.ANTIALIAS)
			image2 = image2.resize((400, 300), Image.ANTIALIAS)

			# 將圖片轉換為Tkinter PhotoImage對象
			tk_image = ImageTk.PhotoImage(image)
			tk_image2 = ImageTk.PhotoImage(image2)

			# 在標籤中顯示圖片
			self.image_label.config(image=tk_image)
			self.image_label.image = tk_image  # 保持對對象的引用，以防止圖片被垃圾回收
			self.image_label2.config(image=tk_image2)
			self.image_label2.image = tk_image2  # 保持對對象的引用，以防止圖片被垃圾回收

		except FileNotFoundError:
			self.image_label.config(text="Image not found.")
			self.image_label2.config(text="Image not found.")
			
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.configure(width=800, height=500)  # Set the frame size

		label = tk.Label(self, text="結果", width=10, height=2)
		label.place(x=410, y=10)
		label.config(font=("微軟黑正體", 16))
		
		label2 = tk.Label(self, text="標準答案")
		label2.place(x=270, y=100)
		label2.config(font=("微軟黑正體", 16))
		
		label3 = tk.Label(self, text="考生答案")
		label3.place(x=580, y=100)
		label3.config(font=("微軟黑正體", 16))
		
		# 創建Listbox
		self.listbox = tk.Listbox(self, height=40, width=15)
		self.listbox.place(x=10, y=50)
		self.listbox.config(font=("Times New Roman", 14))
		
		# 按鈕：載入成績
		button = tk.Button(self, text="載入成績", width=10, height=1, command=lambda: self.load_file_to_listbox())
		button.place(x=25, y=10)
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
	


