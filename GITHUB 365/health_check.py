import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import serial as sr
import serial.tools.list_ports

class health_settings():
    
    # def __init__(self):
        # self.health_port_baud_flag = False      # for raising error if apply btn of config window is pressed without configuring port and baudrate
        # self.health_port_baud_flag2 = False     # for raising error if play btn is pressed without configuring port and baudrate
        # self.health_port_baud_flag3 = False     # to prevent opening the errorbox if port and baudrate are already configured
        

    def xor_calculator():
        pass    
    
    def health_window(self):
            
        self.health_win = tk.Toplevel()
        self.health_win.grab_set()
        self.health_win.bind("<FocusOut>")
        self.health_win.geometry('700x700')
        self.health_win.title('Health Check')

        ################################################################

        hlt_chk_command_label = tk.Label(self.health_win, text='Enter Health Chk Command: ')
        hlt_chk_command_label.place(x=25, y=20)
        hlt_chk_command_label.config(font=('Calibri', 20))

        self.hlt_chk_command_text = tk.Text(self.health_win, width=35)
        self.hlt_chk_command_text.place(x=25, y=70, height=32)
        self.hlt_chk_command_text.config(font=('Calibri', 18))

        ################################################################

        calc_chksum_label = tk.Label(self.health_win, text='Enter the bytes:')
        calc_chksum_label.place(x=25, y=120)
        calc_chksum_label.config(font=('Calibri', 20))

        self.calc_chksum_text = tk.Text(self.health_win, width=35)
        self.calc_chksum_text.place(x=25, y=170, height=32)
        self.calc_chksum_text.config(font=('Calibri', 18))

        calc_xor = tk.Button(self.health_win, text='Calculate XOR', bg='#dddddd', command=self.xor_calculator)
        calc_xor.place(x=465, y=720)
        calc_xor.config(font=('Calibri', 12), width=10)

        ################################################################

        
        health_com_label = tk.Label(self.health_win, text='COM Port: ')
        health_com_label.place(x=25, y=220)
        health_com_label.config(font=('Calibri', 25))

        health_list_of_ports = serial.tools.list_ports.comports()

        self.health_com_port = tk.StringVar()

        self.health_port_choosen = ttk.Combobox(self.health_win, width = 41, textvariable = self.health_com_port)

        self.health_port_choosen['values'] = health_list_of_ports

        self.health_port_choosen.place(x= 25, y=270, height= 30)
        self.health_port_choosen.config(font=('Calibri', 15))
        self.health_port_choosen.current()     

        ######################################################################

        health_baud_rate_label = tk.Label(self.health_win, text='Baudrate: ')
        health_baud_rate_label.place(x=25, y=320)
        health_baud_rate_label.config(font=('Calibri', 25))

        self.health_bd_rate = tk.StringVar()
        self.health_bd_choosen = ttk.Combobox(self.health_win, width = 41, textvariable = self.health_bd_rate)
        self.health_bd_choosen['values'] = ('110', 
                        '300',
                        '600',
                        '1200',
                        '2400',
                        '4800',
                        '9600',
                        '14400',
                        '19200',
                        '28800',
                        '38400',
                        '56000',
                        '57600',
                        '115200',
                        '230400',
                        '460800')
        self.health_bd_choosen.place(x= 25, y=370, height= 30)
        self.health_bd_choosen.config(font=('Calibri', 15))
        self.health_bd_choosen.current()

        ######################################################################

        health_apply_btn = tk.Button(self.health_win, text='Apply', bg='#dddddd', command=self.health_apply_is_clicked)
        health_apply_btn.place(x=465, y=520)
        health_apply_btn.config(font=('Calibri', 12), width=10)

        ################################################################

        health_cancel_btn = tk.Button(self.health_win, text='Cancel', bg='#dddddd', command=self.health_win.destroy)
        health_cancel_btn.place(x=565, y=520)
        health_cancel_btn.config(font=('Calibri', 12), width=10)

        ################################################################

    # def create_port(self):

    #     self.health_bd_rate=int(self.health_bd_choosen.get())
    #     s = sr.Serial(self.health_port[0],self.health_bd_rate)
    #     return s
    

    def health_apply_is_clicked(self):
        

        # print(self.health_command_list)
        # print(type(self.health_command_list))
        

        # try:
            
        self.health_command_list=[" "]
        
        self.health_command_list.append(str(self.hlt_chk_command_text.get("1.0", "end-1c")))
        
        if len(self.health_command_list) > 1:
            self.health_command_list = bytes(self.health_command_list,'utf-16')
        print(self.health_command_list)
        
        self.health_bd_rate = int(self.health_bd_rate.get())
        self.health_com_port = str(self.health_com_port.get())
        self.health_port = self.health_com_port.split()

        self.s = sr.Serial(self.health_port[0], self.health_bd_rate)
        self.s.write(self.health_command_list[1])
        # self.health_port_baud_flag = True
        # self.health_port_baud_flag2 = True
        # self.health_port_baud_flag3 = True


        # self.s.write(self.health_command_list)
        self.health_command_list   = []
        self.health_com_port = []
        self.health_port = []
        self.health_bd_rate = []
        self.health_win.destroy()

        # except:
        
            # try:
            #     self.s.close()
            #     self.health_win.destroy()
            #     messagebox.showerror("Error", "COM Port and/or Baudrate not set!")
            #     self.health_window()
            # except:
            #     self.health_win.destroy()
            #     messagebox.showerror("Error", "COM Port and/or Baudrate not set!")
            #     self.health_window()