import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class bin_calc():

    def bin_window(self):
        self.bin_win = tk.Toplevel()
        self.bin_win.grab_set()
        self.bin_win.bind("<FocusOut>")
        self.bin_win.geometry('550x600')
        self.bin_win.title('Bin Calculation')

        f1_label = tk.Label(self.bin_win, text='f1: ')
        f1_label.place(x=25, y=20)
        f1_label.config(font=('Calibri', 25))

        self.f1_text = tk.Text(self.bin_win, width=23)
        self.f1_text.place(x=225, y=26, height=32)
        self.f1_text.config(font=('Calibri', 18))
    
        f2_label = tk.Label(self.bin_win, text='f2: ')
        f2_label.place(x=25, y=80)
        f2_label.config(font=('Calibri', 25))

        self.f2_text = tk.Text(self.bin_win, width=23)
        self.f2_text.place(x=225, y=86, height=32)
        self.f2_text.config(font=('Calibri', 18))

        nfft_label = tk.Label(self.bin_win, text='NFFT: ')
        nfft_label.place(x=25, y=140)
        nfft_label.config(font=('Calibri', 25))

        self.nfft_text = tk.Text(self.bin_win, width=23)
        self.nfft_text.place(x=225, y=146, height=32)
        self.nfft_text.config(font=('Calibri', 18))

        alt_msg_bytes = tk.Label(self.bin_win, text='Alt msg bytes: ')
        alt_msg_bytes.place(x=25, y=200)
        alt_msg_bytes.config(font=('Calibri', 25))

        self.alt_msg_text = tk.Text(self.bin_win, width=23)
        self.alt_msg_text.place(x=225, y=206, height=32)
        self.alt_msg_text.config(font=('Calibri', 18))

        num_bin_label = tk.Label(self.bin_win, text='No. of bins: ')
        num_bin_label.place(x=25, y=260)
        num_bin_label.config(font=('Calibri', 25))

        self.num_bin_text = tk.Text(self.bin_win, width=23)
        self.num_bin_text.place(x=225, y=266, height=32)
        self.num_bin_text.config(font=('Calibri', 18),state='disabled')

        num_bytes_label = tk.Label(self.bin_win, text='No. of bytes: ')
        num_bytes_label.place(x=25, y=320)
        num_bytes_label.config(font=('Calibri', 25))

        self.num_bytes_text = tk.Text(self.bin_win, width=23)
        self.num_bytes_text.place(x=225, y=326, height=32)
        self.num_bytes_text.config(font=('Calibri', 18),state='disabled')

        calc_bin_btn = tk.Button(self.bin_win, text='Calculate', bg='#dddddd', command=lambda: self.calc_bin_fn())
        calc_bin_btn.place(x=350, y=550)
        calc_bin_btn.config(font=('Calibri', 12), width=10)

        cancel_bin_btn = tk.Button(self.bin_win, text='Cancel', bg='#dddddd', command=lambda:self.cancel_is_clicked())
        cancel_bin_btn.place(x=450, y=550)
        cancel_bin_btn.config(font=('Calibri', 12), width=10)

    def calc_bin_fn(self):
        
        f1 = int(self.f1_text.get("1.0", "end"))
        f2 = int(self.f2_text.get("1.0", "end"))
        nfft = int(self.nfft_text.get("1.0", "end"))
        alt_bytes = int(self.alt_msg_text.get("1.0", "end"))

        f_res = float((10*(10**6))/nfft)
        delta = f2-f1

        final_res = float(delta*(10**3)/f_res)
        num_bytes = (final_res * 4) + alt_bytes

        print(f1)
        print(f2)
        print(nfft)
        print(alt_bytes)

        self.num_bin_text.config(state='normal')
        self.num_bin_text.insert(tk.INSERT, final_res)
        self.num_bin_text.config(state='disabled')

        self.num_bytes_text.config(state='normal')
        self.num_bytes_text.insert(tk.INSERT, num_bytes)
        self.num_bytes_text.config(state='disabled')

    def cancel_is_clicked(self):
        self.bin_win.destroy()
    
    
