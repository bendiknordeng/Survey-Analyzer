import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pickle
import numpy as np

class MarkRects:

	def __init__(self, path):
		self.path = path
		self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
		self.rect_id = []

		raw_image = Image.open(path)
		W, H = raw_image.size

		scale = H/900

		WIDTH, HEIGHT = int(W / scale), int(H / scale)

		self.window = tk.Toplevel()
		self.window.title("Select Area")
		self.window.geometry('%sx%s' % (WIDTH, HEIGHT))
		self.window.configure(background='grey')

		img = ImageTk.PhotoImage(raw_image.resize((WIDTH, HEIGHT)))
		self.canvas = tk.Canvas(self.window, width=img.width(), height=img.height(),
						   borderwidth=0, highlightthickness=0)
		self.canvas.focus_set()
		self.canvas.pack(expand=True)
		self.canvas.img = img  # Keep reference in case this code is put into a function.
		self.canvas.create_image(0, 0, image=img, anchor=tk.NW)

		self.canvas.bind('<Button-1>', self.get_mouse_posn)
		self.canvas.bind('<B1-Motion>', self.update_sel_rect)
		self.canvas.bind('<BackSpace>', self.delete_last_box)
		self.canvas.bind('<Return>', self.end)

		self.window.mainloop()

		self.rects = [(np.array(self.canvas.coords(i))*scale).astype(int) for i in self.rect_id]

		self.window.destroy()

	def get(self):
		return self.rects

	def save(self, filepath):
		with open(filepath, 'wb') as f:
			pickle.save(self.rects, f)

	def get_mouse_posn(self, event):
		self.topx, self.topy = event.x, event.y

		# Create selection rectangle (invisible since corner points are equal).
		self.rect_id.append(self.canvas.create_rectangle(self.topx, self.topy, self.topx, self.topy, dash=(2,2), fill='', outline='green'))

	def update_sel_rect(self, event):
		if not self.rect_id:
			return
		self.botx, self.boty = event.x, event.y
		self.canvas.coords(self.rect_id[-1], self.topx, self.topy, self.botx, self.boty)  # Update selection rect.

	def delete_last_box(self, event):
		if not self.rect_id:
			return

		print('Backspace')

		self.canvas.delete(self.rect_id[-1])
		self.rect_id = self.rect_id[:-1]

	def end(self, event):
		self.window.quit()

if __name__ == '__main__':
	path = filedialog.askopenfilename()
	print(path)
	marked = MarkRects(path)
	print(marked.get())
