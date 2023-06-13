#######################################################
############ FOR OFFICIAL USE #########################
#######################################################

#######################################################
'''
THIS IS UGRA - .0 
THE FIRST VERSION TO BE OFFICIALLY USED. 
'''
#######################################################
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import * 
from tkinter import messagebox
from tkinter.ttk import *
import tkinter.font as font
import numpy as np
import threading
import time
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



### File Imports ###
from preprocess import *
from take_screenshot import *
from file_saving import *
from configuration import *
from health_check import *
from remove_by_index2 import remove
from start import startup
from calc_bin import *
from report_generation import *
# from cmd_response import *


#####################################################################################

# startup()

#####################################################################################

preprocess_obj = preprocessing()
save_file_obj = save_file()
screenshot_obj = screenshot_class()
config_obj = configuration_setting()
# health_obj = health_settings()
bin_obj = bin_calc()
report_obj = generate_report_directory()
# cmd_response_obj = cmd_report_directory()


data1 = np.array([])
data2 = np.array([])
report_data = np.array([])
msg_len = 0
gui_id_30 = 1
gui_id_f = 1
seq_id = 1
disp_counter_30 = 1
disp_counter_f = 1
cond = False
tx_on_full_flag = False 
report_flag = False
# response_report_flag = False
report_loc = ''
report_counter = 1

def plot_data():
    global cond, data1, data2, seq_id, gui_id_30, gui_id_f, disp_counter_30, disp_counter_f, msg_len, save_file_obj, report_flag, report_loc, config_obj, report_counter, report_data , response_obj

    test_msg = np.array([])
    msg = np.array([])
    msg_buff = np.array([])
    test_counter = 0
    counter = 0

    l1 = np.array([])
    l2 = np.array([])
    l3 = np.array([])

    try:
        if cond == True:
            config_obj.s.reset_input_buffer()

            while test_counter < 2:
                a = config_obj.s.read().hex()
                test_msg = np.append(test_msg, a)
                test_counter += 1

            print(test_msg)
            
            if test_msg[0] == '07' and test_msg[1] == 'e0': 
                print("Condition is True")
                msg = np.append(msg, test_msg[0]) 
                msg = np.append(msg, test_msg[1])

                if tx_on_full_flag == True:

                    msg_len = 7916

                    while counter < msg_len-2:  #ud
                        a = config_obj.s.read().hex()
                        msg = np.append(msg, a)
                        counter += 1
                    
                    l3 = msg[msg_len-40:msg_len]  #for 40
                    l3 = preprocess_obj.process_30(l3)

                    msg_buff = preprocess_obj.slicer2(msg)

                    # print("only plot msg")
                    # print(msg_buff)

                    #####################################

                    msg_buff = remove(msg_buff)
                  
                    # print("Remove msg")
                    # print(msg_buff)

                    #####################################

                    l1 = msg_buff[0:int(len(msg_buff)/2)]
                    l2 = msg_buff[int(len(msg_buff)/2):len(msg_buff)]

                    l1 = preprocess_obj.concat_plot_data(l1)
                    l2 = preprocess_obj.concat_plot_data(l2)

                    for i in range(len(l1)):
                        l1[i] = int(l1[i], 16)
                        l2[i] = int(l2[i], 16)

                    if report_flag == True:

                        if report_counter <= 10:

                            report_data = np.append(report_data, l3)
                            report_counter += 1

                        else:

                            report_thread = threading.Thread(target=generate_report,args=[report_data])
                            report_thread.start()
                            report_thread.join()   

                            print("Report data in def")
                            print(report_data)

                            report_data = np.array([]) 
                            report_counter = 1                      
                            report_flag = False

                    t3 = threading.Thread(target=save_file_obj.save_record, args=(l1, l2, l3, seq_id))
                    t3.start()
                    t3.join()
                    seq_id += 1

                    if disp_counter_f % 2 == 0:
                        if gui_id_f % 2 == 0:
                            display_table.insert(parent='',index='end',text='', values=(l3[0], l3[2], l3[3], l3[7], l3[8], l3[9], l3[10],time.strftime('%H:%M:%S')), tags=('even'))
                            display_table.yview_moveto(1)
                            gui_id_f += 1 
                        else:
                            display_table.insert(parent='',index='end',text='', values=(l3[0], l3[2], l3[3], l3[7], l3[8], l3[9], l3[10],time.strftime('%H:%M:%S')), tags=('odd'))
                            display_table.yview_moveto(1)
                            gui_id_f += 1 

                        if len(data1) < len(l1): #ud
                            data1 = np.append(data1, l1[0:len(l1)]) #ud

                        lines.set_xdata(np.arange(0,len(data1)))
                        lines.set_ydata(data1)
                        lines.set_color("#39e600")

                        if len(data2) < len(l2): #ud
                            data2 = np.append(data2, l2[0:len(l2)]) #ud

                        lines1.set_xdata(np.arange(0,len(data2)))
                        lines1.set_ydata(data2)
                        lines1.set_color("#39e600")

                        canvas.draw()
                        canvas.flush_events()

                        data1 = np.array([])
                        data2 = np.array([])        

                    disp_counter_f += 1   

                else:

                    msg_len = 30
                    
                    while counter < msg_len-2:  #ud
                        a = config_obj.s.read().hex()
                        msg = np.append(msg, a)
                        counter += 1
                
                    # msg_buff = preprocess_obj.slicer1(msg)
                    l3 = preprocess_obj.process_30(msg)

                #####################################################################################################
                ###################################### Table components #############################################
                #####################################################################################################

                # Displays one in every 2 messgae packets

                    if report_flag == True:

                        if report_counter <= 10:

                            report_data = np.append(report_data, l3)
                            report_counter += 1

                        else:

                            report_thread = threading.Thread(target=generate_report,args=[report_data])
                            report_thread.start()
                            report_thread.join()  

                            report_data = np.array([]) 
                            report_counter = 1                      
                            report_flag = False

                    t3 = threading.Thread(target=save_file_obj.save_record_30, args=(l3, seq_id))
                    t3.start()
                    t3.join()
                    seq_id += 1

                    if disp_counter_30 % 40 == 0:
                        if gui_id_30 % 2 == 0:
                            display_table.insert(parent='',index='end',text='', values=(l3[0], l3[2], l3[3], l3[7], l3[8], l3[9], l3[10],time.strftime('%H:%M:%S')), tags=('even'))
                            display_table.yview_moveto(1)
                            gui_id_30 += 1 
                        else:
                            display_table.insert(parent='',index='end',text='', values=(l3[0], l3[2], l3[3], l3[7], l3[8], l3[9], l3[10],time.strftime('%H:%M:%S')), tags=('odd'))
                            display_table.yview_moveto(1)    
                            gui_id_30 += 1         
                    
                    disp_counter_30 += 1
                    gui_id_30 += 1 

                test_msg = np.array([])

            else:
                print("Condition is False")
                config_obj.s.reset_input_buffer()
                test_msg = np.array([])

        root.after(1,plot_data)
    
    except KeyboardInterrupt:
        root.destroy()

#################################################################
###################### Button Functions #########################
#################################################################

def plot_start():
    
    global cond, config_obj, system_state_text
    cond = True
    if config_obj.port_baud_flag2 == False:
        messagebox.showerror("Error", "SYSTEM NOT CONFIGURED!")

    config_obj.s.reset_input_buffer()

    system_state_text.config(state='normal')              
    system_state_text.insert(tk.INSERT,"\nSession started at " +str(time.strftime('%H:%M:%S')))
    system_state_text.see('end')
    system_state_text.config(state='disabled')

    
def plot_stop():
    global cond
    cond = False

    system_state_text.config(state='normal')              
    system_state_text.insert(tk.INSERT,"\nSession ended at " +str(time.strftime('%H:%M:%S')))
    system_state_text.see('end')
    system_state_text.config(state='disabled')

def hide_window():
    t2 = threading.Thread(target=screenshot_obj.screenshot)
    t2.start()
    t2.join()

    system_state_text.config(state='normal')              
    system_state_text.insert(tk.INSERT,"\nScreenshot taken at " + time.strftime("%H:%M:%S"))
    system_state_text.see('end')
    system_state_text.config(state='disabled')    

def report_is_clicked():

    global report_flag
    report_flag = True

def generate_report(report_data):
    global config_obj, report_loc

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 8)

    try:
        
        pdf.cell(100, 8, txt = "Report generated on "+str(time.strftime('%d-%m-%Y')+" at "+str(time.strftime('%H:%M:%S'))), new_x="LMARGIN", new_y="NEXT", align = 'L')

        pdf_data_details1 = (
            ("Project", "UUT", "UUT Type", "Model No.", "Unit S.No.", "Test", "Place of Test"),
            (str(config_obj.project), str(config_obj.uut_text), str(config_obj.uut_type_text), 
             str(config_obj.model_input), str(config_obj.ra_unit_input), str(config_obj.test_name_text), str(config_obj.pot_text))
        )

        with pdf.table() as table:
            for data_row in pdf_data_details1:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

        pdf.cell(200, 8, txt = " ", new_x="LMARGIN", new_y="NEXT", align = 'L')

    except:

        print("Project detail(s) missing")


    pass_fail_list = []
    
    # indices_height = [3,18,33,48,63]
    sim_h = []
    indices_daf = [2, 17, 32,47, 62, 77 ,92, 107, 122, 137]



    for i in indices_daf:
        if report_data[i] == 9999 or report_data[i]== 99:
            pass_fail_list.append("PASS")
        else:
            pass_fail_list.append("FAIL")

    # sim_height = str(config_obj.height_input)
    # print(config_obj.height_input)
    # print(type(config_obj.height_input))
    # print(len(config_obj.height_input))

    if len(config_obj.height_input) == 0:
        config_obj.height_input = "Not Specified"
    else:
        pass

    # for i in indices_snr:
    #     if report_data[i] >= int(config_obj.snr_thresh_input):
    #         checklist.append("OK")
    #     else:
    #         checklist.append("NOT OK")
    # except:

    #     for i in indices_height:
    #         if report_data[i] <= 9000:
    #             checklist.append("OK")
    #         else:
    #             checklist.append("NOT OK")

    #     for i in indices_snr:
    #         if report_data[i] >= 18:
    #             checklist.append("OK")
    #         else:
    #             checklist.append("NOT OK")


    pdf_data = (
        ("Sim_H (m)", "Measure_H" , "SNR-U (dB)", "SNR-D (dB)", "fd", "T_Sys", "DA-Flag","Pass/Fail"),
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[8]), time.strftime('%H:%M:%S'), str(report_data[2]), str(pass_fail_list[0])) ,   
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[23]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[1])) ,
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[38]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[2])) ,
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[53]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[3])) ,
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[68]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[4])))
       

    with pdf.table() as table:
        for data_row in pdf_data:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    # pdf.output(str(report_loc) + "/Report at " + str(time.strftime('%H_%M_%S')) + ".pdf")

    # system_state_text.config(state='normal')              
    # system_state_text.insert(tk.INSERT,"Report generated at"+time.strftime('%H:%M:%S'))
    # system_state_text.see('end')
    # system_state_text.config(state='disabled')

########################################################################################################################
#########################################   HEALTH RESPONSE PDF   ######################################################

# def heal_cmd_is_clicked():

#     global response_report_flag
#     response_report_flag = True

# def heal_res_generate_report(response_report_data):
#     global  report_loc

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size = 8)

#     try:
        
#         pdf.cell(100, 8, txt = "Report generated on "+str(time.strftime('%d-%m-%Y')+" at "+str(time.strftime('%H:%M:%S'))), new_x="LMARGIN", new_y="NEXT", align = 'L')

#         pdf_data_details1 = (
#             ('Byte No.','Description','Type','Expected'),
#             (str('00-01','02','03','04','05','06-07','08-09','10','11','12','13','14-15'), 
#              str('Header','Message_ID','Sequence number','Length of Data','Health CMD ACK','Version','Revision','Health Status','TX ON/OFF Status','Reserved','Checksum','Footer'), 
#              str('Unsigned Short','Unsigned Char','Unsigned Char','Unsigned Char','Unsigned Char','Unsigned Short','Unsigned Short','Unsigned Char','Unsigned Char','Unsigned Char','Unsigned Char','Unsigned Short'),
#              str('07E0','A1','()','08','()','07E6','000A','()','()','0D','()','FFFF'))
#         )

#         with pdf.table() as table:
#             for data_row in pdf_data_details1:
#                 row = table.row()
#                 for datum in data_row:
#                     row.cell(datum)

#         pdf.cell(200, 8, txt = " ", new_x="LMARGIN", new_y="NEXT", align = 'L')

#     except:

#         print("Project Response detail(s) missing")


#     pass_fail_list = []

#     if health_tree('Expected') == received_tree('Received') :
#         pass_fail_list.append("PASS")
#     else:
#         pass_fail_list.append("FAIL")




#     pdf_data = (
#         ('Byte No.','Description','Type','Expected','T_sys', 'Received',"Pass/Fail"),
#         (str(response_report_data), str(response_report_data), str(response_report_data), str(response_report_data), time.strftime('%H:%M:%S'), str(response_report_data), str(pass_fail_list)) ,   
#         (str(response_report_data), str(response_report_data), str(response_report_data), str(response_report_data), time.strftime('%H:%M:%S'), str(response_report_data), str(pass_fail_list)) ,   
#         (str(response_report_data), str(response_report_data), str(response_report_data), str(response_report_data), time.strftime('%H:%M:%S'), str(response_report_data),  str(pass_fail_list)) ,
#         (str(response_report_data), str(response_report_data), str(response_report_data), str(response_report_data), time.strftime('%H:%M:%S'), str(response_report_data),  str(pass_fail_list)) ,
#         (str(response_report_data), str(response_report_data), str(response_report_data), str(response_report_data), time.strftime('%H:%M:%S'), str(response_report_data),  str(pass_fail_list)) ,
#         (str(response_report_data), str(response_report_data), str(response_report_data), str(response_report_data), time.strftime('%H:%M:%S'), str(response_report_data),  str(pass_fail_list)) 
#     )

#     with pdf.table() as table:
#         for data_row in pdf_data:
#             row = table.row()
#             for datum in data_row:
#                 row.cell(datum)

#     pdf.output(str(report_loc) + "/Report at " + str(time.strftime('%H_%M_%S')) + ".pdf")

###############################################################################################################################
###############################################################################################################################

def tx_on_full():
    global config_obj, tx_on_full_flag
    tx_on_full_flag = True
    tx_on_msg = b'\x07\xe0\x02\x01\x03\x77\x00\x00\x77\xff\xff'
    config_obj.s.write(tx_on_msg)
    system_state_text.config(state='normal')              
    system_state_text.insert(tk.INSERT,"\nTx ON!")
    system_state_text.see('end')
    system_state_text.config(state='disabled')

def tx_on_30():
    global config_obj, tx_on_full_flag
    tx_on_full_flag = False
    tx_on_msg = b'\x07\xe0\x02\x01\x03\xaa\x00\x00\xaa\xff\xff'
    config_obj.s.write(tx_on_msg)
    system_state_text.config(state='normal')              
    system_state_text.insert(tk.INSERT,"\nTx ON!")
    system_state_text.see('end')
    system_state_text.config(state='disabled')

def tx_off():
    global config_obj
    tx_off_msg = b'\x07\xe0\x02\x01\x03\x55\x00\x00\x55\xff\xff'
    config_obj.s.write(tx_off_msg)
    system_state_text.config(state='normal')              
    system_state_text.insert(tk.INSERT,"\nTx OFF!")
    system_state_text.see('end')
    system_state_text.config(state='disabled')

# def health_check(): #use sr.timeout() for read
#     global config_obj
#     health_seq_id = 0x02
#     chksum = 0x01 ^ health_seq_id ^ 0x03 ^ 0x00 ^ 0x00 ^ 0x00
#     print(chksum)
#     chksum = "{0:#0{1}x}".format(chksum,4)
#     chksum = bytes(chksum, 'utf-8')
#     print(chksum)
#     health_chk_msg = b'\x07\xe0\x01\x02\x03\x00\x00\x00' + chksum + b'\xff\xff'
#     print(health_chk_msg)
#     config_obj.s.write(health_chk_msg)
#     system_state_text.config(state='normal')              
#     system_state_text.insert(tk.INSERT,"\nHealth check command sent !")
#     system_state_text.see('end')
#     system_state_text.config(state='disabled')

def stat_update():

    global config_obj, system_state_text, model_text, ra_unit_text, ra_sr_text, project_text, save_file_obj, screenshot_obj, report_loc

    if config_obj.port_baud_flag == True:
        save_file_obj.setup_file()
        screenshot_obj.create_ss_folder()
        report_loc = report_obj.create_report_folder()

        model_text.config(state='normal')               
        model_text.insert(tk.INSERT, str('\n')+config_obj.model_input) 
        model_text.see('end') 
        model_text.config(state='disabled') 

        ra_unit_text.config(state='normal')               
        ra_unit_text.insert(tk.INSERT, str('\n')+config_obj.ra_unit_input)
        ra_unit_text.see('end') 
        ra_unit_text.config(state='disabled') 

        ra_sr_text.config(state='normal')              
        ra_sr_text.insert(tk.INSERT, str('\n')+config_obj.pot_text)
        ra_sr_text.see('end')
        ra_sr_text.config(state='disabled')
        
        project_text.config(state='normal')              
        project_text.insert(tk.INSERT, str('\n')+config_obj.project)
        project_text.see('end')
        project_text.config(state='disabled')

        system_state_text.config(state='normal')              
        system_state_text.insert(tk.INSERT,"\nCOM PORT: " + str(config_obj.port[0]) + "\t\tBAUDRATE: " + str(config_obj.bd_rate) + "\nSystem ready !\n")
        system_state_text.see('end')
        system_state_text.config(state='disabled')
        config_obj.port_baud_flag = False

    root.after(500, stat_update)

root = tk.Tk()
root.title("UGRA")
root.configure(background= 'white')
root.geometry("1920x1080")

tab_style = ttk.Style()
tab_style.configure('TNotebook.Tab', font=('Calibri','12'))

#Creating tabs
notebook = Notebook(root)
notebook.pack(expand=True)

frame1 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')
frame2 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')
frame3 = tk.Frame(notebook, width=1920, height=1080, bg='#0d0d0d')
frame4 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')
frame5 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')
frame6 = tk.Frame(notebook, width=1920, height=1080)
frame7 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)
frame5.pack(fill='both', expand=True)
frame6.pack(fill='both', expand=True)
frame7.pack(fill='both', expand=True)

notebook.add(frame1, text='Health_CMD_Response')
notebook.add(frame2, text='TX_CMD_Response')
notebook.add(frame3, text='Measurement Data')
notebook.add(frame4, text='Live Plot')
notebook.add(frame5, text= 'Transmit Command')
notebook.add(frame6, text= 'Alt_param_plot')
notebook.add(frame7, text= 'GT_msg_rendering')


#######################################################################################################
################################# HEALTH CHECK COMMAND ################################################
title_label = tk.Label(frame1, text='U G R A', fg='white', bg='#272727')
title_label.config(font=("Game Of Squids", 35, "bold"))
title_label.place(x=1640,y=22)

sub_title_label = tk.Label(frame1, text='UART         GUI    for    Radio    Altimeter', fg='white', bg='#272727')
sub_title_label.config(font=("Century-Gothic", 10))
sub_title_label.place(x=1640,y=75)

h_cmd_frame = tk.Frame(frame1)
h_cmd_frame.pack()
h_cmd_frame.config(background='#272727')
h_cmd_frame.place(x=200, y=350)

h_cmd_style = ttk.Style()
h_cmd_style.configure("Treeview.Heading", background='#272727', foreground='black', font=('Calibri', 40, 'bold'))
h_cmd_style.configure("Treeview", background='#272727', foreground='#33cc00', font=('Calibri', 20, 'bold'))



HEALTH_TREE_LABEL= tk.Label(frame1, text='HEALTH CHECK COMMAND RESPONSE', fg='#E6E6E6', bg='#272727')
HEALTH_TREE_LABEL.config(font=('Calibri', 30, 'bold'))
HEALTH_TREE_LABEL.place(x=650,y=70)

health_tree  = ttk.Treeview(h_cmd_frame ,column=('Byte No.','Description','Type','Expected'  ), show='headings', height=12)
health_tree.pack()

health_tree.column("# 1", anchor=CENTER, width=270)
health_tree.heading("# 1", text="Byte No.")
health_tree.column("# 2", anchor=CENTER, width=270)
health_tree.heading("# 2", text="Description")
health_tree.column("# 3", anchor=CENTER, width=270)
health_tree.heading("# 3", text="Type")
health_tree.column("# 4", anchor=CENTER, width=270)
health_tree.heading("# 4", text="Expected")

health_tree.place(x=200, y=350)
health_tree.insert('', 'end', text="1", values=('00-01','Header','Unsigned Short','07E0') ,tags=('even'))
health_tree.insert('', 'end', text="1", values=('02','Message_ID','Unsigned Char','A1'), tags=('odd'))
health_tree.insert('', 'end', text="1", values=('03','Sequence number','Unsigned Char','()'),tags=('even'))
health_tree.insert('', 'end', text="1", values=('04','Length of Data','Unsigned Char','08'), tags=('odd'))
health_tree.insert('', 'end', text="1", values=('05','Health CMD ACK','Unsigned Char','()'),tags=('even'))
health_tree.insert('', 'end', text="1", values=('06-07','Version','Unsigned Short','07E6'), tags=('odd'))
health_tree.insert('', 'end', text="1", values=('08-09','Revision','Unsigned Short','000A'),tags=('even'))
health_tree.insert('', 'end', text="1", values=('10','Health Status','Unsigned Char','()'), tags=('odd'))
health_tree.insert('', 'end', text="1", values=('11','TX ON/OFF Status','Unsigned Char','()'),tags=('even'))
health_tree.insert('', 'end', text="1", values=('12','Reserved','Unsigned Char','0D'), tags=('odd'))
health_tree.insert('', 'end', text="1", values=('13','Checksum','Unsigned Char','()'),tags=('even'))
health_tree.insert('', 'end', text="1", values=('14-15','Footer','Unsigned Short','FFFF'), tags=('odd'))
health_tree.pack()

health_tree.tag_configure('even', foreground='#33cc00', background='#272727')
health_tree.tag_configure('odd', foreground='#33cc00', background='#4d4d4d')

h_receive_tree = ttk.Treeview(frame1, column=('Received'), show='headings', height=12)
h_receive_tree.pack()

h_receive_tree.column("# 1", anchor=CENTER)
h_receive_tree.heading("# 1", text="Received")
h_receive_tree.place(x=1300, y=350)

for i in range(12):
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('even'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('odd'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('even'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('odd'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('even'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('odd'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('even'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('odd'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('even'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('odd'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('even'))
    h_receive_tree.insert(parent='',index='end',text='', values=("") , tags=('odd'))
    h_receive_tree.yview_moveto(1)


h_receive_tree.tag_configure('even', foreground='#33cc00', background='#272727')
h_receive_tree.tag_configure('odd', foreground='#33cc00', background='#4d4d4d')

def h_exit():
    frame1.destroy()
########################################################

model_label = tk.Label(frame1,text='Model', bg= '#272727', fg='#e6e6e6')
model_label.config(font=('Calibri', 18, 'bold'))
model_label.place(x = 520, y = 190)

model_text = tk.Text(frame1, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
model_text.config(font=('Courier New', 18, 'bold'), state='disabled')
model_text.place(x = 520, y = 230)

########################################################

ra_unit_label = tk.Label(frame1, text='Unit S.No.', bg= '#272727', fg='#e6e6e6')
ra_unit_label.config(font=('Calibri', 18, 'bold'))
ra_unit_label.place(x = 840, y = 190)

ra_unit_text = tk.Text(frame1, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
ra_unit_text.config(font=('Courier New', 18, 'bold'), state='disabled')
ra_unit_text.place(x = 840, y = 230)

########################################################

ra_sr_label = tk.Label(frame1, text='Place of Test', bg= '#272727', fg='#e6e6e6')
ra_sr_label.config(font=('Calibri', 18, 'bold'))
ra_sr_label.place(x = 1160, y = 190)

ra_sr_text = tk.Text(frame1, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
ra_sr_text.config(font=('Courier New', 18, 'bold'), state='disabled')
ra_sr_text.place(x = 1160, y = 230)

########################################################

project_label = tk.Label(frame1, text='Project', bg= '#272727', fg='#e6e6e6')
project_label.config(font=('Calibri', 18, 'bold'))
project_label.place(x = 200, y = 190)

project_text = tk.Text(frame1, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
project_text.config(font=('Courier New', 18, 'bold'), state='disabled')
project_text.place(x = 200, y = 230)

# root.after(500, stat_update)

# mypath = "C:/Users/DELL/Desktop/GUI_IIITNR/Response_Reports"
# def gen_pdf():
#     text = health_tree.get("1.0",END)
#     c=canvas.Canvas(mypath , pagesize='A4')
#     c.save(text)



######################## Display Table ######################################################################################
#############################################################################################################################

table_frame = tk.Frame(frame3)
table_frame.pack()
table_frame.config(background='#272727')
table_frame.place(x=10, y=400, width=1905)

############# Table #############################


tree_style = ttk.Style()
tree_style.configure("Treeview.Heading", background='#272727', foreground='black', font=('Calibri', 18, 'bold'))
tree_style.configure("Treeview", background='#272727', foreground='#33cc00', font=('Calibri', 14, 'bold'))

display_table = ttk.Treeview(table_frame, show='headings', height=20) 
display_table.pack()

############# Heading ###########################
# display_table['columns'] = ('Seq', 'H', 'DAF', 'HoB', 'Mode', 'fr', 'fd', 'fb_U', 'fb_D', 'SNR_U', 'SNR_D', 'N_U', 'N_D', 'T_sys', 'T/S')
display_table['columns'] = ('Seq', 'DAF', 'H', 'fr', 'fd', 'SNR_U', 'SNR_D', 'T_Sys')

display_table.column("#0", width=0, stretch=NO)
display_table.column("Seq",anchor=CENTER, width=250)
# display_table.column("Pkt_No",anchor=CENTER, width=90)
display_table.column("DAF",anchor=CENTER, width=230)
display_table.column("H",anchor=CENTER, width=250)
# display_table.column("HoB",anchor=CENTER, width=120)
# display_table.column("Mode",anchor=CENTER, width=90)
display_table.column("fr",anchor=CENTER, width=230)
display_table.column("fd",anchor=CENTER, width=210)
# display_table.column("fb_U",anchor=CENTER, width=120)
# display_table.column("fb_D",anchor=CENTER, width=120)
display_table.column("SNR_U",anchor=CENTER, width=230)
display_table.column("SNR_D",anchor=CENTER, width=230)
# display_table.column("N_U",anchor=CENTER, width=120)
# display_table.column("N_D",anchor=CENTER, width=120)
display_table.column("T_Sys",anchor=CENTER, width=230)
# display_table.column("T/S",anchor=CENTER, width=120)

display_table.heading("#0",text="",anchor=CENTER)
display_table.heading("Seq",text="Seq",anchor=CENTER)
# display_table.heading("Pkt_No",text="Pkt_No",anchor=CENTER)
display_table.heading("DAF",text="DAF",anchor=CENTER)
display_table.heading("H",text="H",anchor=CENTER)
display_table.heading("fr",text="fr",anchor=CENTER)
display_table.heading("fd",text="fd",anchor=CENTER)
# display_table.heading("HoB",text="HoB",anchor=CENTER)
# display_table.heading("Mode",text="Mode",anchor=CENTER)
# display_table.heading("fb_U",text="fb_U",anchor=CENTER)
# display_table.heading("fb_D",text="fb_D",anchor=CENTER)
display_table.heading("SNR_U",text="SNR_U",anchor=CENTER)
display_table.heading("SNR_D",text="SNR_D",anchor=CENTER)
# display_table.heading("N_U",text="N_U",anchor=CENTER)
# display_table.heading("N_D",text="N_D",anchor=CENTER)
display_table.heading("T_Sys",text="T_Sys",anchor=CENTER)
# display_table.heading("T/S",text="T/S",anchor=CENTER)

display_table.pack()

for i in range(20):
    display_table.insert(parent='',index='end',text='', values=("","","","","","","","","","","","","","",""))     
    display_table.yview_moveto(1)

display_table.tag_configure('even', foreground='#33cc00', background='#272727')
display_table.tag_configure('odd', foreground='#33cc00', background='#4d4d4d')

#############################################################################################################################
######################## GUI 2 ##############################################################################################
#############################################################################################################################

notebook2 = Notebook(frame5)
notebook2.pack(expand=True)

project_specs_tab = tk.Frame(notebook2, width=1920, height=1080, bg='#272727')
param_settings_tab = tk.Frame(notebook2, width=1920, height=1080, bg='#272727')

project_specs_tab.pack(fill='both', expand=True)
param_settings_tab.pack(fill='both', expand=True)

notebook2.add(project_specs_tab, text='Project Specifics')
notebook2.add(param_settings_tab, text='Parameter Settings')

###############################################################################################################
############# Project Version ##################################################################
###############################################################################################################

pro_version_label = tk.Label(project_specs_tab, text='Project Version')
pro_version_label.config(font=('Calibri', 22, 'bold'), bg= '#272727', fg='#e6e6e6')
pro_version_label.place(x=20, y=10)

version_label= tk.Label(project_specs_tab, text='Version')
version_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
version_label.place(x=50, y=60)

version_text = tk.Text(project_specs_tab, width = 20, height=1)
version_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
version_text.place(x = 180, y= 60)

revision_label= tk.Label(project_specs_tab, text='Revision')
revision_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
revision_label.place(x=50, y=110)

revision_text = tk.Text(project_specs_tab, width = 20, height=1)
revision_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
revision_text.place(x = 180, y= 110)

#################### Antenna Cable Calibration ##################################################

acc_label = tk.Label(project_specs_tab, text='Antenna Cable Calibration')
acc_label.config(font=('Calibri', 22, 'bold'), bg= '#272727', fg='#e6e6e6')
acc_label.place(x=20, y=160)

calibrate_label= tk.Label(project_specs_tab, text='Calibration')
calibrate_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
calibrate_label.place(x=50, y=210)

calibrate_text= tk.Text(project_specs_tab, width = 20, height=1)
calibrate_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
calibrate_text.place(x = 180, y= 210)

#################### HoB Condition ##############################################################

hob_cond_label = tk.Label(project_specs_tab, text='HoB Condition')
hob_cond_label.config(font=('Calibri', 22, 'bold'), bg= '#272727', fg='#e6e6e6')
hob_cond_label.place(x=20, y=260)

hob_threshold= tk.Label(project_specs_tab, text='HoB Threshold')
hob_threshold.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
hob_threshold.place(x=50, y=310)

hob_cond_text= tk.Text(project_specs_tab, width = 20, height=1)
hob_cond_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
hob_cond_text.place(x = 180, y= 310)

#################### DDS Setting ##############################################################

dds_setting_label = tk.Label(project_specs_tab, text='DDS Setting')
dds_setting_label.config(font=('Calibri', 22, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_setting_label.place(x=20, y=360)

dds_tone_label = tk.Label(project_specs_tab, text='DDS Single Tone Mode')
dds_tone_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_tone_label.place(x=50, y=410)

single_tone_label = tk.Label(project_specs_tab, text='Single Tone Frequency')
single_tone_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
single_tone_label.place(x=120, y=460)

single_tone_text = tk.Text(project_specs_tab, width = 20, height=1)
single_tone_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
single_tone_text.place(x = 310, y= 460)

#################### DDS Ramp ##################################################################

dds_ramp_label = tk.Label(project_specs_tab, text='DDS Ramp Mode')
dds_ramp_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_ramp_label.place(x=50, y=510)

enable_ramp_val = IntVar()
enable_ramp_btn = tk.Checkbutton(project_specs_tab,
                                 variable=enable_ramp_val,
                                 onvalue=1,
                                 offvalue=0,
                                 bg='#272727',
                                 activebackground='#272727')
enable_ramp_btn.place(x=120,y=560)

enable_ramp_label = tk.Label(project_specs_tab, text='Enable Ramp Mode')
enable_ramp_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
enable_ramp_label.place(x=135, y=557)

dds_freq_label = tk.Label(project_specs_tab, text='DDS Center Frequency')
dds_freq_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_freq_label.place(x=300, y=557)

dds_freq_text = tk.Text(project_specs_tab, width = 20, height=1)
dds_freq_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
dds_freq_text.place(x = 490, y= 557)

#################### Zone condition ##############################################################
zone_cond_label = tk.Label(project_specs_tab, text='Zone Condition')
zone_cond_label.config(font=('Calibri', 22, 'bold'), bg= '#272727', fg='#e6e6e6')
zone_cond_label.place(x=20, y=610)

multi_zone_val = IntVar()
multi_zone_btn = tk.Checkbutton(project_specs_tab,
                                 variable=multi_zone_val,
                                 onvalue=1,
                                 offvalue=0,
                                 bg='#272727',
                                 activebackground='#272727')
multi_zone_btn.place(x=50,y=660)

multi_zone_label = tk.Label(project_specs_tab, text='Multi Zone Enable')
multi_zone_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
multi_zone_label.place(x=75, y=657)

multi_zone_label2 = tk.Label(project_specs_tab, text='(Select to Enable Multiple Zones)')
multi_zone_label2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
multi_zone_label2.place(x=50, y=680)

###################################################################################################
co_zone_label = tk.Label(project_specs_tab, text='CO Zone Selection')
co_zone_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
co_zone_label.place(x=50, y=720)

co_zone_val = IntVar()
co_btn1 = tk.Radiobutton(project_specs_tab, variable=co_zone_val,
                         value=1, 
                         bg='#272727', 
                         activebackground='#272727')
co_btn1.place(x=50, y=750)

co_btn1_label = tk.Label(project_specs_tab, text='INTERNAL')
co_btn1_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
co_btn1_label.place(x=75, y=747)

co_btn2 = tk.Radiobutton(project_specs_tab, variable=co_zone_val, 
                         value=2, 
                         bg='#272727', 
                         activebackground='#272727')
co_btn2.place(x=180, y=750)

co_btn2_label = tk.Label(project_specs_tab, text='EXTERNAL')
co_btn2_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
co_btn2_label.place(x=205, y=747)

###################################################################################################
total_zone_label = tk.Label(project_specs_tab, text='Total Number of Zones')
total_zone_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
total_zone_label.place(x=50, y=790)

noco_val = tk.StringVar()
noco_val_choosen = ttk.Combobox(project_specs_tab, textvariable = noco_val)
noco_val_choosen['values'] = ('1', 
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8')
noco_val_choosen.place(x= 270, y=790, width = 250, height= 30)
noco_val_choosen.config(font=('Calibri', 14))
noco_val_choosen.current()

###################################################################################################
rs422_bd_label = tk.Label(project_specs_tab, text='RS422 Baudrate')
rs422_bd_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
rs422_bd_label.place(x=50, y=850)

rs422_bd_val = tk.StringVar()
rs422_bd_choosen = ttk.Combobox(project_specs_tab, textvariable = rs422_bd_val)
rs422_bd_choosen['values'] = ('110', 
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
rs422_bd_choosen.place(x= 270, y=850, width = 250, height= 30)
rs422_bd_choosen.config(font=('Calibri', 14))
rs422_bd_choosen.current()

###################### Project Specs Apply btn ################################################################ 
def create_zone_tabs():

    global noco_val, param_settings_tab

    noco_val = int(noco_val.get())

    notebook3 = Notebook(param_settings_tab)
    notebook3.pack(expand=True)
    notebook3.place(x=0,y=0)
    
    try:
        for i in range(noco_val):

            temp_label = tk.Frame(notebook3, width=2000, height=600, bg='#272727')
            temp_label.pack(fill='both', expand=1)
            notebook3.add(temp_label, text='Zone '+str(i+1))

            fft_pts_i_label = tk.Label(temp_label, text='FFT Points ' +str(i+1))
            fft_pts_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
            fft_pts_i_label.place(x=20, y=10)

            fft_pts_i__val = tk.StringVar()
            fft_pts_i__val = ttk.Combobox(temp_label, textvariable = fft_pts_i__val)
            fft_pts_i__val['values'] = ('110', 
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
            
            fft_pts_i__val.place(x= 50, y=60, width = 250, height= 30)
            fft_pts_i__val.config(font=('Calibri', 14))
            fft_pts_i__val.current()

            app_btn = Button(param_settings_tab, text='Submit', bg='#dddddd', command=lambda: create_zone_tabs())
            app_btn.place(x=1810, y=570)
            app_btn.config(font=('Calibri', 12), width=10)
########################################################################################################################            

            dds_pts_i_label = tk.Label(temp_label, text='DDS Parameters ' +str(i+1))
            dds_pts_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
            dds_pts_i_label.place(x=20, y=110)

            dds_sub_label1= tk.Label(temp_label, text='Bandwidth '+str(i+1))
            dds_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            dds_sub_label1.place(x=50, y=150)

            dds_sub_tx1 = tk.Text(temp_label, width = 20, height=1)
            dds_sub_tx1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            dds_sub_tx1.place(x = 200, y= 150)

            dds_sub_label1_unit= tk.Label(temp_label, text='MHz')
            dds_sub_label1_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            dds_sub_label1_unit.place(x=450, y=150)

            dds_sub_label2= tk.Label(temp_label, text='Sweep Period '+str(i+1))
            dds_sub_label2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            dds_sub_label2.place(x=570, y=150)

            dds_sub_tx2 = tk.Text(temp_label, width = 20, height=1)
            dds_sub_tx2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            dds_sub_tx2.place(x = 750, y= 150)

            dds_sub_label2_unit= tk.Label(temp_label, text='uSec')
            dds_sub_label2_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            dds_sub_label2_unit.place(x=1000, y=150)
               
########################################################################################################################         

            range_lim_i_label= tk.Label(temp_label, text='Range Limits ')
            range_lim_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
            range_lim_i_label.place(x=20, y=190)

            range_sub_label1= tk.Label(temp_label, text='Min Range ' +str(i+1))
            range_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            range_sub_label1.place(x=50, y=230)

            range_sub_tx1_1 = tk.Text(temp_label, width = 20, height=1)
            range_sub_tx1_1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            range_sub_tx1_1.place(x = 200, y= 230)

            range_sub_label1_unit1= tk.Label(temp_label, text='KHz')
            range_sub_label1_unit1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            range_sub_label1_unit1.place(x=450, y=230)

            range_sub_tx1_2 = tk.Text(temp_label, width = 20, height=1)
            range_sub_tx1_2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            range_sub_tx1_2.place(x = 550, y= 230)

            range_sub_label1_unit2= tk.Label(temp_label, text='m')
            range_sub_label1_unit2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            range_sub_label1_unit2.place(x=800, y=230)

            range_sub_label2= tk.Label(temp_label, text='Max Range ' +str(i+1))
            range_sub_label2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            range_sub_label2.place(x=1000, y=230)

            range_sub_tx2 = tk.Text(temp_label, width = 20, height=1)
            range_sub_tx2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            range_sub_tx2.place(x = 1150, y= 230)

            range_sub_label1_unit1= tk.Label(temp_label, text='KHz')
            range_sub_label1_unit1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            range_sub_label1_unit1.place(x=1400, y=230)

            range_sub_tx2_2 = tk.Text(temp_label, width = 20, height=1)
            range_sub_tx2_2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            range_sub_tx2_2.place(x = 1500, y= 230)

            range_sub_label1_unit2= tk.Label(temp_label, text='m')
            range_sub_label1_unit2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            range_sub_label1_unit2.place(x=1750, y=230)

########################################################################################################################            
  
            val_thresh_i_label= tk.Label(temp_label, text='Validity Thresholds ' +str(i+1))
            val_thresh_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
            val_thresh_i_label.place(x=20, y=270)

            val_sub_label1= tk.Label(temp_label, text='Snr Threshold ' +str(i+1))
            val_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            val_sub_label1.place(x=50, y=310)

            val_sub_tx1_1 = tk.Text(temp_label, width = 20, height=1)
            val_sub_tx1_1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            val_sub_tx1_1.place(x = 200, y= 310)

            val_sub_tx1_2 = tk.Text(temp_label, width = 20, height=1)
            val_sub_tx1_2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            val_sub_tx1_2.place(x = 550, y= 310)

            val_sub_tx1_2_unit= tk.Label(temp_label, text='dB')
            val_sub_tx1_2_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            val_sub_tx1_2_unit.place(x=800, y=310)

            val_sub_label2= tk.Label(temp_label, text='Doppler Range ' +str(i+1)+str('     + -'))
            val_sub_label2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            val_sub_label2.place(x=945, y=310)

            val_sub_tx2 = tk.Text(temp_label, width = 20, height=1)
            val_sub_tx2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            val_sub_tx2.place(x = 1150, y= 310)

            val_sub_tx2_unit= tk.Label(temp_label, text='KHz')
            val_sub_tx2_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            val_sub_tx2_unit.place(x=1400, y=310)

########################################################################################################################

            tx_rx_attn_i_label= tk.Label(temp_label, text='TX & RX Attenuations ' +str(i+1))
            tx_rx_attn_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
            tx_rx_attn_i_label.place(x=20, y=350)

            tx_rx_attn_sub_label1= tk.Label(temp_label, text='Tx Attenuation ' +str(i+1))
            tx_rx_attn_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            tx_rx_attn_sub_label1.place(x=50, y=390)

            tx_rx_attn_sub_txt1 = tk.Text(temp_label, width = 20, height=1)
            tx_rx_attn_sub_txt1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            tx_rx_attn_sub_txt1.place(x = 200, y= 390)

            tx_rx_attn_sub_txt1_unit= tk.Label(temp_label, text='dB')
            tx_rx_attn_sub_txt1_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            tx_rx_attn_sub_txt1_unit.place(x=450, y=390)

            tx_rx_attn_sub_label2= tk.Label(temp_label, text='Rx Attenuation '+str(i+1))
            tx_rx_attn_sub_label2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            tx_rx_attn_sub_label2.place(x=570, y=390)

            tx_rx_attn_sub_txt2 = tk.Text(temp_label, width = 20, height=1)
            tx_rx_attn_sub_txt2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            tx_rx_attn_sub_txt2.place(x = 750, y= 390)

            tx_rx_attn_sub_txt2_unit= tk.Label(temp_label, text='dB')
            tx_rx_attn_sub_txt2_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            tx_rx_attn_sub_txt2_unit.place(x=1000, y=390)

########################################################################################################################
            
            ad504_gain__i_label= tk.Label(temp_label, text='AD604 Gain Voltage ' +str(i+1))
            ad504_gain__i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
            ad504_gain__i_label.place(x=20, y=430)

            ad504_gain_sub_label1= tk.Label(temp_label, text='Dac Voltage ' +str(i+1))
            ad504_gain_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            ad504_gain_sub_label1.place(x=50, y=470)

            ad504_gain_sub_tx1 = tk.Text(temp_label, width = 20, height=1)
            ad504_gain_sub_tx1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
            ad504_gain_sub_tx1.place(x = 200, y= 470)

            ad504_gain_sub_tx1_unit= tk.Label(temp_label, text='V')
            ad504_gain_sub_tx1_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
            ad504_gain_sub_tx1_unit.place(x=450, y=470)

########################################################################################################################            
            
            if i == 0:

                changeover_setpts_i_label= tk.Label(temp_label, text='Changeover Set Point ' +str(i+1))
                changeover_setpts_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_i_label.place(x=20, y=510)

                changeover_setpts_sub_label1= tk.Label(temp_label, text='Higher Set Point ' +str(i+1))
                changeover_setpts_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_label1.place(x=50, y=550)

                changeover_setpts_sub_tx1 = tk.Text(temp_label, width = 20, height=1)
                changeover_setpts_sub_tx1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
                changeover_setpts_sub_tx1.place(x = 200, y= 550)

                changeover_setpts_sub_label2= tk.Label(temp_label, text='Set Point Threshold '+str(i+1))
                changeover_setpts_sub_label2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_label2.place(x=570, y=550)

                changeover_setpts_sub_tx2 = tk.Text(temp_label, width = 20, height=1)
                changeover_setpts_sub_tx2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
                changeover_setpts_sub_tx2.place(x = 750, y= 550)

                changeover_setpts_sub_tx2_unit= tk.Label(temp_label, text='::::::::::::::::::::::::: INPUT VALUE AFTER MULTIPLYING BY 10')
                changeover_setpts_sub_tx2_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_tx2_unit.place(x=1000, y=550)
            
            
            elif i == noco_val-1:

                changeover_setpts_i_label= tk.Label(temp_label, text='Change Set Point ' +str(i+1))
                changeover_setpts_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_i_label.place(x=20, y=510)

                changeover_setpts_sub_label1= tk.Label(temp_label, text='Lower Set Point ' +str(i+1))
                changeover_setpts_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_label1.place(x=50, y=550)

                changeover_setpts_sub_tx1 = tk.Text(temp_label, width = 20, height=1)
                changeover_setpts_sub_tx1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
                changeover_setpts_sub_tx1.place(x = 200, y= 550)

                changeover_setpts_sub_label3= tk.Label(temp_label, text='Set Point Threshold '+str(i+1))
                changeover_setpts_sub_label3.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_label3.place(x=570, y=550)

                changeover_setpts_sub_tx3 = tk.Text(temp_label, width = 20, height=1)
                changeover_setpts_sub_tx3.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
                changeover_setpts_sub_tx3.place(x = 760, y= 550)

                changeover_setpts_sub_tx3_unit= tk.Label(temp_label, text=':::::::::::::::::::::  INPUT VALUE AFTER MULTIPLYING BY 10')
                changeover_setpts_sub_tx3_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_tx3_unit.place(x=1010, y=550)

            else:

                changeover_setpts_i_label= tk.Label(temp_label, text='Change Set Point ' +str(i+1))
                changeover_setpts_i_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_i_label.place(x=20, y=510)

                changeover_setpts_sub_label1= tk.Label(temp_label, text='Lower Set Point ' +str(i+1))
                changeover_setpts_sub_label1.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_label1.place(x=50, y=550)

                changeover_setpts_sub_tx1 = tk.Text(temp_label, width = 20, height=1)
                changeover_setpts_sub_tx1.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
                changeover_setpts_sub_tx1.place(x = 200, y= 550)

                changeover_setpts_sub_label2= tk.Label(temp_label, text='Higher Set Point ' +str(i+1))
                changeover_setpts_sub_label2.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_label2.place(x=470, y=550)

                changeover_setpts_sub_tx2 = tk.Text(temp_label, width = 20, height=1)
                changeover_setpts_sub_tx2.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
                changeover_setpts_sub_tx2.place(x = 650, y= 550)

                changeover_setpts_sub_label3= tk.Label(temp_label, text='Set Point Threshold '+str(i+1))
                changeover_setpts_sub_label3.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_label3.place(x=910, y=550)

                changeover_setpts_sub_tx3 = tk.Text(temp_label, width = 20, height=1)
                changeover_setpts_sub_tx3.config(font=('Calibri', 16, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
                changeover_setpts_sub_tx3.place(x = 1100, y= 550)

                changeover_setpts_sub_tx3_unit= tk.Label(temp_label, text=':::::::::::::::::::::  INPUT VALUE AFTER MULTIPLYING BY 10')
                changeover_setpts_sub_tx3_unit.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
                changeover_setpts_sub_tx3_unit.place(x=1350, y=550)

    except:
        print("No. of zones not set")

def additional_zone_params():

    global param_settings_tab, param_settings_tab, noco_val

    summary_frame = tk.Frame(param_settings_tab, width=1895, height=500, bg='#272727')
    summary_frame.pack(fill='both', expand=1)
    summary_frame.place(x=0,y=630)

    param_settings_apply_btn = tk.Button(summary_frame, text='Apply')
    param_settings_apply_btn.place(x=1810, y=20)
    param_settings_apply_btn.config(font=('Calibri', 12), width=10)

    attn_bits_cond_label = tk.Label(summary_frame, text='Attenuation Bits Condition')
    attn_bits_cond_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
    attn_bits_cond_label.place(x=20, y=10)

    att_condition_val = IntVar()
    att_condition_btn = tk.Checkbutton(summary_frame,
                                    variable=att_condition_val,
                                    onvalue=1,
                                    offvalue=0,
                                    bg='#272727',
                                    activebackground='#272727')
    att_condition_btn.place(x=50,y=50)

    att_condition_label = tk.Label(summary_frame, text='Att Condition (Select to invert Attenuator Bits)')
    att_condition_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
    att_condition_label.place(x=75, y=48)

    att_fine_setting_label = tk.Label(summary_frame, text='Attenuator Fine Setting')
    att_fine_setting_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
    att_fine_setting_label.place(x=50, y=90)

    tx_fine_setting_val = IntVar()
    tx_fine_setting_btn = tk.Checkbutton(summary_frame,
                                    variable=tx_fine_setting_val,
                                    onvalue=1,
                                    offvalue=0,
                                    bg='#272727',
                                    activebackground='#272727')
    tx_fine_setting_btn.place(x=90,y=130)

    tx_fine_setting_label = tk.Label(summary_frame, text='Tx Attenuation 0.5')
    tx_fine_setting_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
    tx_fine_setting_label.place(x=115, y=128)

    rx_fine_setting_val = IntVar()
    rx_fine_setting_btn = tk.Checkbutton(summary_frame,
                                    variable=rx_fine_setting_val,
                                    onvalue=1,
                                    offvalue=0,
                                    bg='#272727',
                                    activebackground='#272727')
    rx_fine_setting_btn.place(x=325,y=130)

    rx_fine_setting_label = tk.Label(summary_frame, text='Rx Attenuation 0.5')
    rx_fine_setting_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
    rx_fine_setting_label.place(x=350, y=128)

    zonewise_range_label = tk.Label(summary_frame, text='TOTAL ZONEWISE RANGE')
    zonewise_range_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
    zonewise_range_label.place(x=20, y=170)

    min_range_label = tk.Label(summary_frame, text='MIN RANGE (Min Alt)')
    min_range_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
    min_range_label.place(x=50, y=220)

    max_range_label = tk.Label(summary_frame, text='MAX RANGE (Max Alt)')
    max_range_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
    max_range_label.place(x=50, y=260)

    for i in range(noco_val):

        zone_alt_label = tk.Label(summary_frame, text='Zone '+str(i+1))
        zone_alt_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
        zone_alt_label.place(x=350+(i*200), y=195)

        zone_min_alt_txt = tk.Text(summary_frame, width = 20, height=1)
        zone_min_alt_txt.config(font=('Calibri', 12, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
        zone_min_alt_txt.place(x=300+(i*200), y=225)

        zone_max_alt_txt = tk.Text(summary_frame, width = 20, height=1)
        zone_max_alt_txt.config(font=('Calibri', 12, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
        zone_max_alt_txt.place(x=300+(i*200), y=265)


project_specs_btn = tk.Button(project_specs_tab, text='Apply', bg='#dddddd', command=lambda: [create_zone_tabs(), additional_zone_params()])
project_specs_btn.place(x=800, y=900)
project_specs_btn.config(font=('Calibri', 12), width=10)

submit_btn = Button(project_specs_tab, text='Submit', bg='#dddddd', command=lambda:  additional_zone_params(),)
submit_btn.place(x=920, y=900)
submit_btn.config(font=('Calibri', 12), width=10)
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

title_label = tk.Label(frame3, text='U G R A', fg='white', bg='#272727')
title_label.config(font=("Game Of Squids", 35, "bold"))
title_label.place(x=1640,y=22)

sub_title_label = tk.Label(frame3, text='UART         GUI    for    Radio    Altimeter', fg='white', bg='#272727')
sub_title_label.config(font=("Century-Gothic", 10))
sub_title_label.place(x=1640,y=75)

#####################################################################################################
#####################################################################################################
#####################################################################################################

# Creating the 2 Subplots 

fig, (ax, ax1) = plt.subplots(2,1)
fig.patch.set_facecolor('#272727')
# FFT UP PLOT 
ax.set_title("FFT UP", color='white')
ax.set_xlabel("Sample", color='white')
ax.set_ylabel("values", color='white')
ax.set_xlim(0,3950) #ud
ax.set_ylim(0,10000)
ax.grid()
ax.set_facecolor("#000000")
ax.tick_params(color='white', labelcolor='white')
lines = ax.plot([],[])[0]

# FFT DOWN PLOT 
ax1.set_title("FFT DOWN", color='white')
ax1.set_xlabel("Sample", color='white')
ax1.set_ylabel("values", color='white')
ax1.set_xlim(0,3950) #ud
ax1.set_xlim(xmin=0)
ax1.set_ylim(0,10000)
ax1.grid()
ax1.set_facecolor("#000000")
ax1.tick_params(color='white', labelcolor='white')
lines1 = ax1.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=frame4)
canvas.get_tk_widget().place(x=0, y=0, width=1920, height=1000)
canvas.draw()

title_label = tk.Label(frame4, text='U G R A', fg='white', bg='#272727')
title_label.config(font=("Game Of Squids", 35, "bold"))
title_label.place(x=1640,y=22)

sub_title_label = tk.Label(frame4, text='UART         GUI    for    Radio    Altimeter', fg='white', bg='#272727')
sub_title_label.config(font=("Century-Gothic", 10))
sub_title_label.place(x=1640,y=75)

    

##############################################################
########################################################
##### STATE DISPLAY ##########################################

system_state_label = tk.Label(frame3, text='SYSTEM STATE', bg= '#272727', fg='#e6e6e6')
system_state_label.config(font=('Calibri', 18, 'bold'))
system_state_label.place(x = 20, y = 110)

system_state_text = tk.Text(frame3, width=38, height=5, border=0, bg="#4d4d4d", fg='#ffff33')
system_state_text.config(font=('Calibri', 16, 'bold'))
system_state_text.place(x = 20, y = 150)

system_state_text.config(state='normal')              
system_state_text.insert(tk.INSERT,"Project details not entered\nCOM PORT and BAUDRATE not configured !")
system_state_text.see('end')
system_state_text.config(state='disabled')

#######################################################################################################
#######################################################################################################

########################################################
##### DISPLAY PROJECT DETAILS ##########################

model_label = tk.Label(frame3, text='Model', bg= '#272727', fg='#e6e6e6')
model_label.config(font=('Calibri', 18, 'bold'))
model_label.place(x = 820, y = 190)

model_text = tk.Text(frame3, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
model_text.config(font=('Courier New', 18, 'bold'), state='disabled')
model_text.place(x = 820, y = 230)

########################################################

ra_unit_label = tk.Label(frame3, text='Unit S.No.', bg= '#272727', fg='#e6e6e6')
ra_unit_label.config(font=('Calibri', 18, 'bold'))
ra_unit_label.place(x = 1140, y = 190)

ra_unit_text = tk.Text(frame3, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
ra_unit_text.config(font=('Courier New', 18, 'bold'), state='disabled')
ra_unit_text.place(x = 1140, y = 230)

########################################################

ra_sr_label = tk.Label(frame3, text='Place of Test', bg= '#272727', fg='#e6e6e6')
ra_sr_label.config(font=('Calibri', 18, 'bold'))
ra_sr_label.place(x = 1460, y = 190)

ra_sr_text = tk.Text(frame3, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
ra_sr_text.config(font=('Courier New', 18, 'bold'), state='disabled')
ra_sr_text.place(x = 1460, y = 230)

########################################################

project_label = tk.Label(frame3, text='Project', bg= '#272727', fg='#e6e6e6')
project_label.config(font=('Calibri', 18, 'bold'))
project_label.place(x = 500, y = 190)

project_text = tk.Text(frame3, width=15, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
project_text.config(font=('Courier New', 18, 'bold'), state='disabled')
project_text.place(x = 500, y = 230)

#######################################################################################################
#######################################################################################################
#####################################  ALT_PARAM_PLOT TAB  ############################################

default_file_path = "D:/Santhosh/JTmsgRenderGUI/Alt_param/data_dec.txt"
# Function to handle file browse button event
def browse_file():
    ALT_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if ALT_file_path:
        ALT_file_path_entry.delete(0, tk.END)
        ALT_file_path_entry.insert(0, ALT_file_path)
        # Update the default file path
        global default_file_path
        default_file_path = ALT_file_path

def hide_window():
    t_alt = threading.Thread(target=screenshot_obj.screenshot)
    t_alt.start()
    t_alt.join()

# Function to plot selected columns
def plot_columns():
    ALT_file_path = ALT_file_path_entry.get()
    selected_columns = []
    for i, var in enumerate(checkbox_vars):
        if var.get():
            selected_columns.append(i)  # Append the index of the selected column

    data_format = data_format_var.get()
    if data_format == "Decimal":
        conversion_func = int
    elif data_format == "Hexadecimal":
        conversion_func = lambda x: int(x, 16)
    elif data_format == "Floating":
        conversion_func = float

    with open(ALT_file_path, 'r') as file:
        all_columns = [[] for _ in range(len(selected_columns))]  # Initialize empty lists for each selected column
        for line in file:
            columns = line.strip().split()  # Split the line by tab spacing or the appropriate delimiter
            filter_data = True

            # Check if filtering is enabled and if the filter column(s) and value(s) are provided
            if filter_checkbox_var.get():
                if filter_column_1.get() is not None and filter_value_1.get() != "":
                    try:
                        value_1 = conversion_func(columns[filter_column_1.get()])
                        if value_1 != int(filter_value_1.get(),16):
                            filter_data = False
                    except ValueError:
                        filter_data = False
                
                if use_filter_column_2_var.get() == 1 and filter_column_2.get() is not None and filter_value_2.get() != "":
                    try:
                        value_2 = conversion_func(columns[filter_column_2.get()])
                        if value_2 != int(filter_value_2.get()):
                            filter_data = False
                    except ValueError:
                        filter_data = False

            if not filter_data:
                continue

            for i, column_index in enumerate(selected_columns):
                value = conversion_func(columns[column_index])
                all_columns[i].append(value)  # Append the data point to the respective column

    # Create subplots based on the number of selected columns
    num_plots = len(selected_columns)
    fig, axs = plt.subplots(num_plots, 1, figsize=(8, 6*num_plots), squeeze=False)

    # Plot the selected columns
    for i, column_data in enumerate(all_columns):
        axs[i, 0].plot(range(len(column_data)), column_data)
        axs[i, 0].set_xlabel('Index')
        axs[i, 0].set_ylabel(f'Column {selected_columns[i]} Data')
        
        # Add title only if the checkbox is selected
        if title_checkbox_var.get():
            axs[i, 0].set_title(f'Column {selected_columns[i]} Data Points', pad=20)  # Adjust the title spacing

    # Adjust the spacing between subplots and labels
    plt.subplots_adjust(hspace=0.5)

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()


# Create the main window

# alt_frame = tk.Frame(frame6)
# alt_frame.pack()
# alt_frame.config(background='#e6e6e6')
# alt_frame.place(x=20, y=325, width=1875)

alt_frame = tk.Frame(frame6)
alt_frame.pack(side=tk.TOP, padx=10, pady=10)

# Create a label and entry for displaying the selected file path
ALT_file_path_label = tk.Label(frame6, text="Selected File:")
ALT_file_path_label.config(font=('Calibri', 18 ,'bold'))
ALT_file_path_label.pack()

ALT_file_path_entry = tk.Entry(frame6, width=50)
ALT_file_path_entry.config(font=('Calibri', 18))
ALT_file_path_entry.pack()

# Set the initial value of the file path entry
ALT_file_path_entry.insert(0, default_file_path)

# Create a button for browsing the file
browse_button = tk.Button(frame6, text="Browse", command=browse_file)
browse_button.config(font=('Calibri', 14))
browse_button.pack()

# Create checkboxes for column selection
checkbox_vars = []
checkboxes = []
columns_frame = tk.Frame(frame6)
columns_frame.pack()



# frame6.pack()

# Add checkboxes for columns
# Add checkboxes for columns
def add_checkbox(i):
    var = tk.IntVar()
    checkbox_vars.append(var)
    checkbox = tk.Checkbutton(columns_frame, text=f"Column {i}", variable=var)
    checkbox.config(font=('Calibri', 11))

    # var_2 = tk.IntVar()
    # checkbox_vars2.append(var_2)
    # checkbox2 = tk.Checkbutton(columns_frame4, text=f"Column {i}", variable=var_2)
    # checkbox2.config(font=('Calibri', 13))

    if   i <=20:
        checkbox.pack(side=tk.LEFT)
    # elif i>10 and i==19:
    #     checkbox2.pack(side=tk.LEFT)
    else:
        checkbox.pack()
    checkboxes.append(checkbox)

for i in range(20):
    add_checkbox(i)
    


# checkbox_vars2 = []
# checkboxes2=[]
# columns_frame4 = tk.Frame(frame6)
# columns_frame4.pack()

# def add_checkbox_2(x):
     
     
#     var_2 = tk.IntVar()
#     checkbox_vars2.append(var_2)
#     checkbox2 = tk.Checkbutton(columns_frame4, text=f"Column {i}", variable=var_2)
#     checkbox2.config(font=('Calibri', 13))

     
#     if  x >= 11:

#         checkbox_vars2.pack(side=tk.LEFT)
#     # elif i>10 and i==19:
#     #     checkbox2.pack(side=tk.LEFT)
#     else:
#         checkbox_vars2.pack()
#     checkboxes2.append(checkboxes2)



# # Assuming a maximum of 18 columns, you can adjust the range if needed


# for x in range(19):
#     add_checkbox_2(x)


# Create a checkbox for selecting the display of subplot titles
title_checkbox_var = tk.IntVar()
title_checkbox = tk.Checkbutton(frame6, text="Display Subplot Titles", variable=title_checkbox_var)
title_checkbox.config(font=('Calibri', 18))
title_checkbox.pack()

# Create a checkbox for enabling or disabling filtering
filter_checkbox_var = tk.IntVar()
filter_checkbox = tk.Checkbutton(frame6, text="Enable Filtering", variable=filter_checkbox_var)
filter_checkbox.config(font=('Calibri', 18))
filter_checkbox.pack()

# Create a label and entry for filter column 1 selection
filter_column_label_1 = tk.Label(frame6, text="Filter Column 1:")
filter_column_label_1.config(font=('Calibri', 18))
filter_column_label_1.pack()

filter_column_1 = tk.IntVar()
filter_column_entry_1 = tk.Entry(frame6, textvariable=filter_column_1)
filter_column_entry_1.config(font=('Calibri', 18))
filter_column_entry_1.pack()

# Create a label and entry for filter value 1
filter_value_label_1 = tk.Label(frame6, text="Filter Value 1:")
filter_value_label_1.config(font=('Calibri', 18))
filter_value_label_1.pack()

filter_value_1 = tk.StringVar()
filter_value_entry_1 = tk.Entry(frame6, textvariable=filter_value_1)
filter_value_entry_1.config(font=('Calibri', 18))
filter_value_entry_1.pack()
# filter_value_entry_1=str(filter_value_entry_1)
# filter_value_entry_1=bytes(filter_value_entry_1 ,'utf-16')


# Create a checkbox for selecting the second filter column
use_filter_column_2_var = tk.IntVar()
use_filter_column_2_checkbox = tk.Checkbutton(frame6, text="Use Filter Column 2", variable=use_filter_column_2_var)
use_filter_column_2_checkbox.config(font=('Calibri', 18))
use_filter_column_2_checkbox.pack()

# Create a label and entry for filter column 2 selection
filter_column_label_2 = tk.Label(frame6, text="Filter Column 2:")
filter_column_label_2.config(font=('Calibri', 18))
filter_column_label_2.pack()

filter_column_2 = tk.IntVar()
filter_column_entry_2 = tk.Entry(frame6, textvariable=filter_column_2, state=tk.DISABLED)
filter_column_entry_2.config(font=('Calibri', 18))
filter_column_entry_2.pack()

# Create a label and entry for filter value 2
filter_value_label_2 = tk.Label(frame6, text="Filter Value 2:")
filter_value_label_2.config(font=('Calibri', 18))
filter_value_label_2.pack()

filter_value_2 = tk.StringVar()
filter_value_entry_2 = tk.Entry(frame6, textvariable=filter_value_2, state=tk.DISABLED)
filter_value_entry_2.config(font=('Calibri', 18))
filter_value_entry_2.pack()

# Function to toggle the state of filter column 2 components
def toggle_filter_column_2():
    if use_filter_column_2_var.get() == 1:
        filter_column_entry_2.configure(state=tk.NORMAL)
        filter_value_entry_2.configure(state=tk.NORMAL)
    else:
        filter_column_entry_2.configure(state=tk.DISABLED)
        filter_value_entry_2.configure(state=tk.DISABLED)

# Associate the toggle function with the checkbox
use_filter_column_2_checkbox.configure(command=toggle_filter_column_2)

# Create a dropdown menu for selecting the data format
data_format_label = tk.Label(frame6, text="Data Format:")
data_format_label.config(font=('Calibri', 18))
data_format_label.pack()

data_format_var = tk.StringVar()
data_format_dropdown = tk.OptionMenu(frame6, data_format_var, "Decimal", "Hexadecimal", "Floating")
data_format_dropdown.config(font=('Calibri', 18))
data_format_dropdown.pack()

# Create a button for plotting the selected columns
plot_button = tk.Button(frame6, text="Plot", command=plot_columns)
plot_button.config(font=('Calibri', 18))
plot_button.pack()

title_label = tk.Label(frame6, text='U G R A', fg='black', bg='white')
title_label.config(font=("Game Of Squids", 35, "bold"))
title_label.place(x=1640,y=22)

sub_title_label = tk.Label(frame6, text='UART         GUI    for    Radio    Altimeter', fg='white', bg='#272727')
sub_title_label.config(font=("Century-Gothic", 10))
sub_title_label.place(x=1640,y=75)


#######################################################################################################
#######################################################################################################
################################## GT _ MSG RENDERING TAB ###########################################

# # Function to handle file browse button event
# def browse_file():
#     file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
#     file_entry.delete(0, END)
#     file_entry.insert(0, file_path)
#     

# def update_plot(i):
#     try:
#         if not file_path or file is None:
#             anim.event_source.stop()
#             return
        
#         line = file.readline()
        
#         if not line:
#             anim.event_source.stop()
#             return
        
#         data = line.split()
        
#         x = []
#         y = []
        
#         for i in range(2, len(data), 1):
#             x.append(i)
#             y.append(int(data[i], 16))
        
#         plt.cla()
#         plt.plot(x, y)
#         plt.xlabel('X-axis')
#         plt.ylabel('Y-axis')
#         plt.title('Real-time Data Plot')
#         plt.tight_layout()
#         canvas.draw()

#     except Exception as e:
#         print(f"Error: {e}")

# def plot_data():
#     try:
#         global file
#         global file_path

#         file_path = file_entry.get()
#         file = open(file_path, 'r')

#         # Start the animation
#         anim.event_source.start()

#     except Exception as e:
#         print(f"Error: {e}")

# def pause_plot():
#     anim.event_source.stop()

# def continue_plot():
#     if not file_path or file is None:
#         return

#     anim.event_source.start()

# # window = tk.Tk()
# # window.title('Real-time Data Plot')
# # window.geometry('1000x1000')



# file_frame = Frame(frame7)
# file_frame.pack(side=TOP, padx=10, pady=10)

# file_button = Button(file_frame, text="Browse", command=browse_file)
# file_button.pack(side=LEFT)

# file_entry = Entry(file_frame, width=50)
# file_entry.pack(side=LEFT)

# button_frame = Frame(frame7)
# button_frame.pack(side=TOP, padx=10, pady=10)

# plot_button = Button(button_frame, text="Plot", command=plot_data)
# plot_button.pack(side=LEFT, padx=10)

# pause_button = Button(button_frame, text="Pause", command=pause_plot)
# pause_button.pack(side=LEFT, padx=10)

# continue_button = Button(button_frame, text="Continue", command=continue_plot)
# continue_button.pack(side=LEFT, padx=10)

# # Create a matplotlib Figure and Axes for the plot
# fig, ax_gt = plt.subplots()

# # Create a Tkinter Canvas for embedding the plot
# canvas = FigureCanvasTkAgg(fig, master=frame7)
# canvas.draw()
# canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

# toolbar = NavigationToolbar2Tk(canvas, frame7)
# toolbar.update()
# canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

# # Open the file for reading
# file = None


# # Initialize the animation
# anim = FuncAnimation(fig, update_plot, interval=1000)  # Update every second  #update_plot,


#######################################################################################################
################################# HEALTH CHECK COMMAND ################################################



# HEALTH_TREE_LABEL= tk.Label(frame1, text='HEALTH CHECK COMMAND RESPONSE', fg='#E6E6E6', bg='#272727')
# HEALTH_TREE_LABEL.config(font=('Calibri', 20, 'bold'))
# HEALTH_TREE_LABEL.place(x=150,y=590)

# health_tree = ttk.Treeview(frame1, column=('Byte No.','Description','Type','Expected'), show='headings', height=12)
# health_tree.pack()

# health_tree.column("# 1", anchor=CENTER, width=160)
# health_tree.column("# 2", anchor=CENTER,width=160)
# health_tree.column("# 3", anchor=CENTER, width=160)
# health_tree.column("# 4", anchor=CENTER, width=160)

# health_tree.heading("# 1", text="Byte No.")
# health_tree.heading("# 2", text="Description")
# health_tree.heading("# 3", text="Type")
# health_tree.heading("# 4", text="Expected")
# health_tree.pack()


# health_tree.place(x=30, y=670)

# health_tree.insert('', 'end', text="1", values=('00-01','Header','Unsigned Short','07E0'))
# health_tree.insert('', 'end', text="1", values=('02','Message_ID','Unsigned Char','A1'))
# health_tree.insert('', 'end', text="1", values=('03','Sequence number','Unsigned Char','()'))
# health_tree.insert('', 'end', text="1", values=('04','Length of Data','Unsigned Char','08'))
# health_tree.insert('', 'end', text="1", values=('05','Health CMD ACK','Unsigned Char','()'))
# health_tree.insert('', 'end', text="1", values=('06-07','Version','Unsigned Short','07E6'))
# health_tree.insert('', 'end', text="1", values=('08-09','Revision','Unsigned Short','000A'))
# health_tree.insert('', 'end', text="1", values=('10','Health Status','Unsigned Char','()'))
# health_tree.insert('', 'end', text="1", values=('11','TX ON/OFF Status','Unsigned Char','()'))
# health_tree.insert('', 'end', text="1", values=('12','Reserved','Unsigned Char','0D'))
# health_tree.insert('', 'end', text="1", values=('13','Checksum','Unsigned Char','()'))
# health_tree.insert('', 'end', text="1", values=('14-15','Footer','Unsigned Short','FFFF'))

# received_tree = ttk.Treeview(frame1, column=('Received'), show='headings', height=12)
# received_tree.pack()

# received_tree.column("# 1", anchor=CENTER)

# received_tree.heading("# 1", text="Received")

# received_tree.place(x=680, y=670)

# for i in range(12):
#     received_tree.insert(parent='',index='end',text='', values=(""))
#     received_tree.yview_moveto(1)

# lst = ['ABC', 'DEF']

# received_tree.insert(parent='',index='end',text='', values=(lst[1]+lst[0]))

#######################################################################################################
#################################################  TX_RESPONSE  #######################################
title_label = tk.Label(frame2, text='U G R A', fg='white', bg='#272727')
title_label.config(font=("Game Of Squids", 35, "bold"))
title_label.place(x=1640,y=22)

sub_title_label = tk.Label(frame2, text='UART         GUI    for    Radio    Altimeter', fg='white', bg='#272727')
sub_title_label.config(font=("Century-Gothic", 10))
sub_title_label.place(x=1640,y=75)
    
TX_Tree_label=tk.Label(frame2, text='TX COMMAND RESPONSE', fg='#E6E6E6', bg='#272727')
TX_Tree_label.config(font=('Calibri', 30, 'bold'))
TX_Tree_label.place(x=700,y=90)

TX_tree = ttk.Treeview(frame2, column=('Byte No.','Description','Type','Expected'), show='headings', height=9)
TX_tree.pack()

TX_tree.column("# 1", anchor=CENTER, width=270)
TX_tree.column("# 2", anchor=CENTER,width=270)
TX_tree.column("# 3", anchor=CENTER, width=270)
TX_tree.column("# 4", anchor=CENTER, width=270)

TX_tree.heading("# 1", text="Byte No.")
TX_tree.heading("# 2", text="Description")
TX_tree.heading("# 3", text="Type")
TX_tree.heading("# 4", text="Expected")
TX_tree.pack()


TX_tree.place(x=200, y=470)
# TX_tree.insert('', 'end', text='', values=(""),tags = ('even'))
TX_tree.insert('', 'end', text="1", values=('00-01','Header','Unsigned Short','07E0'),tags = ('odd'))
TX_tree.insert('', 'end', text="1", values=('02','Message_ID','Char','A2'),tags = ('even'))
TX_tree.insert('', 'end', text="1", values=('03','Sequence_ID','Char','()'),tags = ('odd'))
TX_tree.insert('', 'end', text="1", values=('04','Length of Data','Char','05'),tags = ('even'))
TX_tree.insert('', 'end', text="1", values=('05','TX On/Off AND ACK','Char','()'),tags = ('odd'))
TX_tree.insert('', 'end', text="1", values=('06-07','TX ON/OFF Status','Unsigned Short','()'),tags = ('even'))
TX_tree.insert('', 'end', text="1", values=('08-09','Preset HOB Read-back','Unsigned Short','()'),tags = ('odd'))
TX_tree.insert('', 'end', text="1", values=('10-11','Checksum','Unsigned Short','()'),tags = ('even'))
TX_tree.insert('', 'end', text="1", values=('12-13','Footer','Unsigned Short','FFFF'),tags = ('odd'))
# TX_tree.insert('', 'end', text='', values=(""),tags = ('even'))
# TX_tree.insert('', 'end', text='', values=(""),tags = ('odd'))

TX_tree.tag_configure('even', foreground='#33cc00', background='#272727')
TX_tree.tag_configure('odd', foreground='#33cc00', background='#4d4d4d')

TX_RECEIVE_tree = ttk.Treeview(frame2, column=('Received'), show='headings', height=9)
TX_RECEIVE_tree.pack()

TX_RECEIVE_tree.column("# 1", anchor=CENTER)

TX_RECEIVE_tree.heading("# 1", text="Received")

TX_RECEIVE_tree.place(x=1300, y=470)

for i in range(9):
    # TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('even'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('odd'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('even'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('odd'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('even'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('odd'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('even'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('odd'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('even'))
    TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('odd'))
    # TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('even'))
    # TX_RECEIVE_tree.insert(parent='',index='end',text='', values=(""),tags = ('odd'))
    TX_RECEIVE_tree.yview_moveto(1)

TX_RECEIVE_tree.tag_configure('even', foreground='#33cc00', background='#272727')
TX_RECEIVE_tree.tag_configure('odd', foreground='#33cc00', background='#4d4d4d')


def tx_exit():
    frame2.destroy()


#######################################################################################################
#######################################################################################################
#######################################################################################################

#Scrrenshot button

ss_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/camera.png')

root.update()
take_ss = tk.Button(frame3, height=32, width=32, command=hide_window, bg='#272727')
take_ss.config(image=ss_icon)
take_ss["border"] = "0"
take_ss.place(x = 180, y = 40)

root.update()
take_ss = tk.Button(frame4, height=32, width=32, command=hide_window, bg='#272727')
take_ss.config(image=ss_icon)
take_ss["border"] = "0"
take_ss.place(x = 180, y = 40)

#Start/Stop buttons

start_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/play.png')
stop_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/stop.png')
configuration_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/settings.png')
health_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/heart.png')
pdf_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/pdf.png')
# mypdf_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/mypdf.png')
myFont = font.Font(size=12, weight='bold')

root.update()
start = tk.Button(frame3, height=32, width=32,command=lambda: plot_start(), bg='#272727')
start.config(image=start_icon)
start["border"] = "0"
start.place(x=20, y=40)

root.update()
stop = tk.Button(frame3, height=24, width=24, command=lambda: plot_stop(), bg='#272727')
stop.config(image=stop_icon)
stop["border"] = "0"
stop.place(x=70, y=44)

root.update()
configure = Button(frame3, height=32, width=32, command=lambda: config_obj.config_window(), bg='#272727')
configure.config(image=configuration_icon)
configure["border"] = "0"
configure.place(x=120, y=40)

root.update()
report_btn= tk.Button(frame3, height=32, width=32, bg='#272727', command=lambda: report_is_clicked())
report_btn.config(image=pdf_icon)
report_btn["border"] = "0"
report_btn.place(x=490, y=870)

root.update()
tx_on_full_btn = tk.Button(frame3, text="TX - ON_F", bg = 'light green', fg='black', height = 1, width=10, command=lambda: tx_on_full())
tx_on_full_btn.place(x=100, y=870)
tx_on_full_btn['font'] = myFont

root.update()
tx_on_30_btn = tk.Button(frame3, text="TX - ON_30", bg = 'light green', fg='black', height = 1, width=10, command=lambda: tx_on_30())
tx_on_30_btn.place(x=230, y=870)
tx_on_30_btn['font'] = myFont

root.update()
tx_off_btn = tk.Button(frame3, text="TX - OFF", bg = 'red', fg='white', height = 1, width=10, command=lambda: tx_off())
tx_off_btn.place(x=360, y=870)
tx_off_btn['font'] = myFont

# root.update()
# health_chk_btn = tk.Button(frame3, height = 32, width=32, bg='#272727', command=lambda: health_obj.health_window())
# health_chk_btn.config(image=health_icon)
# health_chk_btn["border"] = "0"
# health_chk_btn.place(x=140, y=40)

root.update()
bin_calc_btn = tk.Button(frame3, text="CALCULATE BIN", bg = 'yellow', fg='black', height = 1, width=14, command=lambda: bin_obj.bin_window())
bin_calc_btn.place(x=230, y=42)
bin_calc_btn['font'] = myFont

# root.update()
# h_cmd_res_btn = Button(frame1, height=32, width=32, command=lambda:heal_cmd_is_clicked())
# h_cmd_res_btn.config(image= mypdf_icon)
# h_cmd_res_btn["border"] = "0"
# h_cmd_res_btn.place(x=500, y=120)
root.update()
h_exit_btn = Button(frame1 , text="EXIT", bg = 'white', fg='black', height = 1, width=10, command=lambda: h_exit() )
h_exit_btn.place(x=200, y=770)
h_exit_btn['font'] = myFont

# root.update()
# res_tx_on_full_btn = tk.Button(frame2, text="TX - ON_F", bg = 'light green', fg='black', height = 1, width=10, command=lambda: tx_on_full())
# res_tx_on_full_btn.place(x=200, y=900)
# res_tx_on_full_btn['font'] = myFont

# root.update()
# res_tx_on_30_btn = tk.Button(frame2, text="TX - ON_30", bg = 'light green', fg='black', height = 1, width=10, command=lambda: tx_on_30())
# res_tx_on_30_btn.place(x=320, y=900)
# res_tx_on_30_btn['font'] = myFont

# root.update()
# res_tx_off_btn = tk.Button(frame2, text="TX - OFF", bg = 'red', fg='white', height = 1, width=10, command=lambda: tx_off())
# res_tx_off_btn.place(x=440, y=900)
# res_tx_off_btn['font'] = myFont

root.update()
res_tx_exit_btn = Button(frame2 , text="EXIT", bg = 'white', fg='black', height = 1, width=10, command=lambda: tx_exit() )
res_tx_exit_btn.place(x=1390, y=900)
res_tx_exit_btn['font'] = myFont

# root.update()
# res_h_configure = Button(frame1, height=32, width=32, command=lambda: config_obj.config_window(), bg='#272727')
# res_h_configure.config(image=configuration_icon)
# res_h_configure["border"] = "0"
# res_h_configure.place(x=550, y=85)

# root.update()
# res_tx_configure = Button(frame2, height=32, width=32, command=lambda: config_obj.config_window(), bg='#272727')
# res_tx_configure.config(image=configuration_icon)
# res_tx_configure["border"] = "0"
# res_tx_configure.place(x=600, y=100)

# root.update()
# tx_cmd_res_btn = Button(frame2, height=32, width=32, command=lambda:heal_cmd_is_clicked())
# tx_cmd_res_btn.config(image= mypdf_icon)
# tx_cmd_res_btn["border"] = "0"
# tx_cmd_res_btn.place(x=550, y=120)

t1 = threading.Thread(target=plot_data)
t1.start()

t4 = threading.Thread(target=stat_update)
t4.start()

root.mainloop()