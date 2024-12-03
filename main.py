import PIL.Image
import numpy as np
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import messagebox

def image_to_ascii(image_path, output_width=150):  
    img = PIL.Image.open(image_path).convert('L')
    
    width_percent = output_width / float(img.size[0])
    height = int(float(img.size[1]) * float(width_percent) * 2)
    img = img.resize((output_width, height))

    ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    pixels = np.array(img)
    
    ascii_str = ''
    for row in pixels:
        for pixel in row:
            char_index = int((pixel / 255) * (len(ascii_chars) - 1))
            ascii_str += ascii_chars[char_index]
        ascii_str += '\n'
    
    return ascii_str

class ASCIIArtGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Generator")
        
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)
        
        self.select_btn = tk.Button(control_frame, text="Chọn Ảnh", command=self.select_image)
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="Độ rộng:").pack(side=tk.LEFT, padx=5)
        self.width_entry = tk.Entry(control_frame, width=10)
        self.width_entry.insert(0, "150")
        self.width_entry.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(control_frame, text="Lưu ASCII", command=self.save_ascii)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.text_area = scrolledtext.ScrolledText(root, width=150, height=50, font=('Courier New', 6))
        self.text_area.pack(padx=10, pady=10)
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            try:
                width = int(self.width_entry.get())
                ascii_art = image_to_ascii(file_path, width)
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', ascii_art)
            except ValueError:
                messagebox.showerror("Lỗi", "Độ rộng phải là một số nguyên")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể chuyển đổi ảnh: {str(e)}")
                
    def save_ascii(self):
        if not self.text_area.get('1.0', tk.END).strip():
            messagebox.showwarning("Cảnh báo", "Không có ASCII art để lưu!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get('1.0', tk.END))
                messagebox.showinfo("Thành công", "Đã lưu ASCII art thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ASCIIArtGUI(root)
    root.mainloop()
