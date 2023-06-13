from tkinter import messagebox
from tkinter import ttk
import serial as sr
import serial.tools.list_ports
from tkinter import * 
import tkinter.ttk as ttk

# root=Tk()
# root.title("CONFIG")

     # comment these when importing into original file


class configuration_setting():
    
    def __init__(self):
        self.port_baud_flag = False      # for raising error if apply btn of config window is pressed without configuring port and baudrate
        self.port_baud_flag2 = False     # for raising error if play btn is pressed without configuring port and baudrate
        self.port_baud_flag3 = False     # to prevent opening the errorbox if port and baudrate are already configured
        # self.mylist=[]

    def config_window(self):
            
        self.child_win = Toplevel()
        self.child_win.grab_set()
        self.child_win.bind("<FocusOut>")
        self.child_win.geometry('700x800')
        self.child_win.title('Configuration')
        
        ################################################################

        proj_label = Label(self.child_win, text='Project: ')
        proj_label.place(x=25, y=20)
        proj_label.config(font=('Calibri', 25))
        
        self.project = StringVar()
        proj_choosen = ttk.Combobox(self.child_win, width = 41, textvariable = self.project)
        proj_choosen['values'] = ('BRAHMOS', 
                        'GARUDA',
                        'PRALAY',
                        'LRGB',
                        'SMART')
        proj_choosen.place(x= 230, y=25, height= 30)
        proj_choosen.config(font=('Calibri', 15))
        proj_choosen.current()

        ################################################################

        test_name_label = Label(self.child_win, text='Test ')
        test_name_label.place(x=25, y=80)
        test_name_label.config(font=('Calibri', 25))

        self.test_name_text = Text(self.child_win, width=35)
        self.test_name_text.place(x=230, y=85, height=32)
        self.test_name_text.config(font=('Calibri', 18))

        ################################################################

        uut_label = Label(self.child_win, text='UUT: ')
        uut_label.place(x=25, y=140)
        uut_label.config(font=('Calibri', 25))

        self.uut_text = Text(self.child_win, width=35)
        self.uut_text.place(x=230, y=145, height=32)
        self.uut_text.config(font=('Calibri', 18))

        ################################################################

        uut_type_label = Label(self.child_win, text='UUT Type: ')
        uut_type_label.place(x=25, y=200)
        uut_type_label.config(font=('Calibri', 25))

        self.uut_type_text = Text(self.child_win, width=35)
        self.uut_type_text.place(x=230, y=205, height=32)
        self.uut_type_text.config(font=('Calibri', 18))
        
        ################################################################
        
        model_label = Label(self.child_win, text='Model: ')
        model_label.place(x=25, y=260)
        model_label.config(font=('Calibri', 25))

        self.model_input = Text(self.child_win, width=35)
        self.model_input.place(x=230, y=265, height=32)
        self.model_input.config(font=('Calibri', 18))

        ################################################################

        ra_unit_label = Label(self.child_win, text='RA Serial No: ')
        ra_unit_label.place(x=25, y=320)
        ra_unit_label.config(font=('Calibri', 25))

        self.ra_unit_input = Text(self.child_win, width=35)
        self.ra_unit_input.place(x=230, y=325, height=32)
        self.ra_unit_input.config(font=('Calibri', 18))

        ################################################################

        pot_label = Label(self.child_win, text='Place of Test: ')
        pot_label.place(x=25, y=380)
        pot_label.config(font=('Calibri', 25))

        self.pot_text = Text(self.child_win, width=35)
        self.pot_text.place(x=230, y=385, height=32)
        self.pot_text.config(font=('Calibri', 18))

        ################################################################

        height_thresh_label = Label(self.child_win, text='Sim_H: ')
        height_thresh_label.place(x=25, y=440)
        height_thresh_label.config(font=('Calibri', 25))

        self.height_thresh_input = Text(self.child_win, width=35)
        self.height_thresh_input.place(x=230, y=445, height=32)
        self.height_thresh_input.config(font=('Calibri', 18))

        ################################################################

        # snr_thresh_label = tk.Label(self.child_win, text='SNR Thresh: ')
        # snr_thresh_label.place(x=25, y=500)
        # snr_thresh_label.config(font=('Calibri', 25))

        # self.snr_thresh_input = tk.Text(self.child_win, width=35)
        # self.snr_thresh_input.place(x=230, y=505, height=32)
        # self.snr_thresh_input.config(font=('Calibri', 18))

        ################################################################

        com_label = Label(self.child_win, text='COM Port: ')
        com_label.place(x=25, y=560)
        com_label.config(font=('Calibri', 25))

        list_of_ports = serial.tools.list_ports.comports()

        self.com_port =StringVar()

        self.port_choosen = ttk.Combobox(self.child_win, width = 41, textvariable = self.com_port)

        self.port_choosen['values'] = list_of_ports

        self.port_choosen.place(x= 230, y=565, height= 30)
        self.port_choosen.config(font=('Calibri', 15))
        self.port_choosen.current()        

        ################################################################

        baud_rate_label = Label(self.child_win, text='Baudrate: ')
        baud_rate_label.place(x=25, y=620)
        baud_rate_label.config(font=('Calibri', 25))

        self.bd_rate = StringVar()
        self.bd_choosen = ttk.Combobox(self.child_win, width = 41, textvariable = self.bd_rate)
        self.bd_choosen['values'] = ('110', 
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
        self.bd_choosen.place(x= 230, y=625, height= 30)
        self.bd_choosen.config(font=('Calibri', 15))
        self.bd_choosen.current()

        ################################################################

        apply_btn = Button(self.child_win, text='Apply', bg='#dddddd', command=self.apply_is_clicked)
        apply_btn.place(x=465, y=720)
        apply_btn.config(font=('Calibri', 12), width=10)

        ################################################################

        cancel_btn = Button(self.child_win, text='Cancel', bg='#dddddd', command=self.child_win.destroy)
        cancel_btn.place(x=565, y=720)
        cancel_btn.config(font=('Calibri', 12), width=10)

        # ################################################################

        # submit_btn= Button(self.child_win, bg='#dddddd',bd=3,text = "SUBMIT",command=lambda:self.get_data())
        # submit_btn.place(x=365,y=720)
        # submit_btn.config(font=('Calibri', 12),width=10)

    # def create_port(self):

    #     self.bd_rate=int(self.bd_choosen.get())
    #     s = sr.Serial(self.port[0],self.bd_rate)
    #     return s
    
    # def get_data(self):
    #     self.com_port = str(self.com_port.get())
    #     self.port = self.com_port.split()
    #     print(self.port)

    #     self.mylist.append(str(self.project.get()))
    #     self.mylist.append(self.test_name_text.get("1.0", "end-1c"))
    #     self.mylist.append( self.uut_text.get("1.0", "end-1c"))
    #     self.mylist.append(self.uut_type_text.get("1.0", "end-1c"))
    #     self.mylist.append( self.model_input.get("1.0", "end-1c"))
    #     self.mylist.append(self.ra_unit_input.get("1.0", "end-1c"))
    #     self.mylist.append(self.pot_text.get("1.0", "end-1c"))
    #     self.mylist.append(self.height_thresh_input.get("1.0", "end-1c"))
    #     # self.mylist.append('  ')
    #     self.mylist.append(str(self.port[0]))
    #     self.mylist.append(int(self.bd_choosen.get()))
    #     print(self.mylist)

    #     self.mylist = str(self.mylist)
    #     print(self.mylist)
    #     print(type(self.mylist))


    #     self.mylist = bytes(self.mylist,'utf-16')
    #     print(self.mylist)
    #     print(type(self.mylist))

    #     self.s = self.create_port()
    #     self.s.write(self.mylist)
    #     self.mylist = []

        

    def apply_is_clicked(self):

        self.uut_text = str(self.uut_text.get("1.0", "end-1c"))
        self.uut_type_text = str(self.uut_type_text.get("1.0", "end-1c"))
        self.model_input = str(self.model_input.get("1.0", "end-1c"))
        self.ra_unit_input = str(self.ra_unit_input.get("1.0", "end-1c"))
        self.pot_text = str(self.pot_text.get("1.0", "end-1c"))
        self.project = str(self.project.get())
        self.test_name_text = str(self.test_name_text.get("1.0", "end-1c"))
        self.height_input = str(self.height_thresh_input.get("1.0", "end-1c"))
        # self.snr_thresh_input = str(self.snr_thresh_input.get("1.0", "end-1c"))

        try:

            self.bd_rate = int(self.bd_rate.get())
            self.com_port = str(self.com_port.get())
            self.port = self.com_port.split()
            self.s = sr.Serial(self.port[0], self.bd_rate)
            self.port_baud_flag = True
            self.port_baud_flag2 = True
            self.port_baud_flag3 = True
            self.child_win.destroy()

        except:
            try:
                self.s.close()
                self.child_win.destroy()
                messagebox.showerror("Error", "COM Port and/or Baudrate not set!")
                self.config_window()
            except:
                self.child_win.destroy()
                messagebox.showerror("Error", "COM Port and/or Baudrate not set!")
                self.config_window()


# configure = Button(root, command=lambda: config_obj.config_window(), bg='white',text="Config")
# configure.place(x=25, y=25)
# configure.config(font=('Calibri', 16))

# config_obj = configuration_setting()


# root.mainloop()