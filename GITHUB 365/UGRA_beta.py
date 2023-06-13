#######################################################
############ FOR OFFICIAL USE #########################
#######################################################

#######################################################
'''
THIS IS UGRA - 1.0 
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
report_loc = ''
report_counter = 1

def plot_data():
    global cond, data1, data2, seq_id, gui_id_30, gui_id_f, disp_counter_30, disp_counter_f, msg_len, save_file_obj, report_flag, report_loc, config_obj, report_counter, report_data

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

                        if report_counter <= 5:

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

                        if report_counter <= 5:

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
    indices_daf = [2, 17, 32,47, 62]



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


    # pdf_data = (
    #     ("H (m)", "Check H", "DAF", "SNR-U (dB)", "Check SNR-U", "SNR-D (dB)", "Check SNR-D", "Time"),
    #     (str(report_data[3]), checklist[0], str(report_data[2]), str(report_data[9]), checklist[5], str(report_data[10]), checklist[10], time.strftime('%H:%M:%S')),    
    #     (str(report_data[18]), checklist[1], str(report_data[17]), str(report_data[24]), checklist[5], str(report_data[25]), checklist[11], time.strftime('%H:%M:%S')),
    #     (str(report_data[33]), checklist[2], str(report_data[32]), str(report_data[39]), checklist[5], str(report_data[40]), checklist[12], time.strftime('%H:%M:%S')),
    #     (str(report_data[48]), checklist[3], str(report_data[47]), str(report_data[54]), checklist[5], str(report_data[55]), checklist[13], time.strftime('%H:%M:%S')),
    #     (str(report_data[63]), checklist[4], str(report_data[62]), str(report_data[69]), checklist[5], str(report_data[70]), checklist[14], time.strftime('%H:%M:%S'))
    # )

    pdf_data = (
        ("Sim_H (m)", "Measure_H" , "SNR-U (dB)", "SNR-D (dB)", "fd", "T_sys", "DA-Flag","Pass/Fail"),
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[8]), time.strftime('%H:%M:%S'), str(report_data[2]), str(pass_fail_list[0])) ,   
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[23]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[1])) ,
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[38]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[2])) ,
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[53]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[3])) ,
        (str(config_obj.height_input),str(report_data[3]), str(report_data[9]), str(report_data[10]), str(report_data[68]), time.strftime('%H:%M:%S'), str(report_data[2]),  str(pass_fail_list[4])) 
    )

    with pdf.table() as table:
        for data_row in pdf_data:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    pdf.output(str(report_loc) + "/Report at " + str(time.strftime('%H_%M_%S')) + ".pdf")

    system_state_text.config(state='normal')              
    system_state_text.insert(tk.INSERT,"Report generated at"+time.strftime('%H:%M:%S'))
    system_state_text.see('end')
    system_state_text.config(state='disabled')

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
#     # config_obj.s.write(health_chk_msg)
#     # system_state_text.config(state='normal')              
#     # system_state_text.insert(tk.INSERT,"\nHealth check command sent !")
#     # system_state_text.see('end')
#     # system_state_text.config(state='disabled')

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
frame2 = tk.Frame(notebook, width=1920, height=1080, bg='#0d0d0d')
frame3 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')
frame4 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')
frame5 = tk.Frame(notebook, width=1920, height=1080, bg='#272727')


frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)
frame5.pack(fill='both', expand=True)


notebook.add(frame1, text='Tabulated Data')
notebook.add(frame2, text='Live Plot')
notebook.add(frame3, text= 'Transmit Command')
notebook.add(frame4, text= 'Alt_param_plot')
notebook.add(frame5, text= 'GT_msg_rendering')


#############################################################################################################################
######################## Display Table ######################################################################################
#############################################################################################################################

table_frame = tk.Frame(frame1)
table_frame.pack()
table_frame.config(background='#272727')
table_frame.place(x=20, y=325, width=1875)

############# Table #########################

tree_style = ttk.Style()
tree_style.configure("Treeview.Heading", background='#272727', foreground='black', font=('Calibri', 18, 'bold'))
tree_style.configure("Treeview", background='#272727', foreground='#33cc00', font=('Calibri', 14, 'bold'))

display_table = ttk.Treeview(table_frame) 
display_table.pack()

############# Heading ###########################
# display_table['columns'] = ('Seq', 'H', 'DAF', 'HoB', 'Mode', 'fr', 'fd', 'fb_U', 'fb_D', 'SNR_U', 'SNR_D', 'N_U', 'N_D', 'T_sys', 'T/S')
display_table['columns'] = ('Seq', 'DAF', 'H', 'fr', 'fd', 'SNR_U', 'SNR_D', 'T_sys')

display_table.column("#0", width=0, stretch=NO)
display_table.column("Seq",anchor=CENTER, width=90)
# display_table.column("Pkt_No",anchor=CENTER, width=90)
display_table.column("DAF",anchor=CENTER, width=100)
display_table.column("H",anchor=CENTER, width=110)
# display_table.column("HoB",anchor=CENTER, width=120)
# display_table.column("Mode",anchor=CENTER, width=90)
display_table.column("fr",anchor=CENTER, width=100)
display_table.column("fd",anchor=CENTER, width=110)
# display_table.column("fb_U",anchor=CENTER, width=120)
# display_table.column("fb_D",anchor=CENTER, width=120)
display_table.column("SNR_U",anchor=CENTER, width=120)
display_table.column("SNR_D",anchor=CENTER, width=120)
# display_table.column("N_U",anchor=CENTER, width=120)
# display_table.column("N_D",anchor=CENTER, width=120)
display_table.column("T_sys",anchor=CENTER, width=120)
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
display_table.heading("T_sys",text="T_sys",anchor=CENTER)
# display_table.heading("T/S",text="T/S",anchor=CENTER)

display_table.pack()

for i in range(10):
    display_table.insert(parent='',index='end',text='', values=("","","","","","","","","","","","","","",""))     
    display_table.yview_moveto(1)

display_table.tag_configure('even', foreground='#33cc00', background='#272727')
display_table.tag_configure('odd', foreground='#33cc00', background='#4d4d4d')

#############################################################################################################################
######################## GUI 2 ##############################################################################################
#############################################################################################################################

notebook2 = Notebook(frame3)
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
pro_version_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
pro_version_label.place(x=20, y=10)

version_label= tk.Label(project_specs_tab, text='Version')
version_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
version_label.place(x=20, y=60)

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
acc_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
acc_label.place(x=20, y=160)

calibrate_label= tk.Label(project_specs_tab, text='Calibration')
calibrate_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
calibrate_label.place(x=50, y=210)

calibrate_text= tk.Text(project_specs_tab, width = 20, height=1)
calibrate_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
calibrate_text.place(x = 180, y= 210)

#################### HoB Condition ##############################################################

hob_cond_label = tk.Label(project_specs_tab, text='HoB Condition')
hob_cond_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
hob_cond_label.place(x=20, y=260)

hob_threshold= tk.Label(project_specs_tab, text='HoB Threshold')
hob_threshold.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
hob_threshold.place(x=50, y=310)

hob_cond_text= tk.Text(project_specs_tab, width = 20, height=1)
hob_cond_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
hob_cond_text.place(x = 180, y= 310)

#################### DDS Setting ##############################################################

dds_setting_label = tk.Label(project_specs_tab, text='DDS Setting')
dds_setting_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_setting_label.place(x=20, y=360)

dds_tone_label = tk.Label(project_specs_tab, text='DDS Single Tone Mode')
dds_tone_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_tone_label.place(x=50, y=410)

single_tone_label = tk.Label(project_specs_tab, text='Single Tone Frequency')
single_tone_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
single_tone_label.place(x=80, y=460)

single_tone_text = tk.Text(project_specs_tab, width = 20, height=1)
single_tone_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
single_tone_text.place(x = 270, y= 460)

#################### DDS Ramp ##################################################################

dds_ramp_label = tk.Label(project_specs_tab, text='DDS Ramp Mode')
dds_ramp_label.config(font=('Calibri', 16, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_ramp_label.place(x=50, y=510)

enable_ramp_val = IntVar()
enable_ramp_btn = tk.Checkbutton(project_specs_tab,
                                 variable=enable_ramp_val,
                                 onvalue=1,
                                 offvalue=0,
                                 bg='#272727',
                                 activebackground='#272727')
enable_ramp_btn.place(x=80,y=560)

enable_ramp_label = tk.Label(project_specs_tab, text='Enable Ramp Mode')
enable_ramp_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
enable_ramp_label.place(x=105, y=557)

dds_freq_label = tk.Label(project_specs_tab, text='DDS Center Frequency')
dds_freq_label.config(font=('Calibri', 14, 'bold'), bg= '#272727', fg='#e6e6e6')
dds_freq_label.place(x=280, y=557)

dds_freq_text = tk.Text(project_specs_tab, width = 20, height=1)
dds_freq_text.config(font=('Calibri', 18, 'bold'), bg= '#4d4d4d', fg='#e6e6e6', border=0)
dds_freq_text.place(x = 470, y= 557)

#################### Zone condition ##############################################################
zone_cond_label = tk.Label(project_specs_tab, text='Zone Condition')
zone_cond_label.config(font=('Calibri', 18, 'bold'), bg= '#272727', fg='#e6e6e6')
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
rs422_bd_label.place(x=20, y=850)

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

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

title_label = tk.Label(frame1, text='U G R A', fg='white', bg='#272727')
title_label.config(font=("Game Of Squids", 35, "bold"))
title_label.place(x=1640,y=22)

sub_title_label = tk.Label(frame1, text='UART         GUI    for    Radio    Altimeter', fg='white', bg='#272727')
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

canvas = FigureCanvasTkAgg(fig, master=frame2)
canvas.get_tk_widget().place(x=0, y=0, width=1920, height=1000)
canvas.draw()
##############################################################
########################################################
##### STATE DISPLAY ##########################################

system_state_label = tk.Label(frame1, text='SYSTEM STATE', bg= '#272727', fg='#e6e6e6')
system_state_label.config(font=('Calibri', 18, 'bold'))
system_state_label.place(x = 20, y = 110)

system_state_text = tk.Text(frame1, width=38, height=5, border=0, bg="#4d4d4d", fg='#ffff33')
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

model_label = tk.Label(frame1, text='Model', bg= '#272727', fg='#e6e6e6')
model_label.config(font=('Calibri', 18, 'bold'))
model_label.place(x = 470, y = 190)

model_text = tk.Text(frame1, width=25, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
model_text.config(font=('Courier New', 18, 'bold'), state='disabled')
model_text.place(x = 470, y = 230)

########################################################

ra_unit_label = tk.Label(frame1, text='Unit S.No.', bg= '#272727', fg='#e6e6e6')
ra_unit_label.config(font=('Calibri', 18, 'bold'))
ra_unit_label.place(x = 860, y = 190)

ra_unit_text = tk.Text(frame1, width=25, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
ra_unit_text.config(font=('Courier New', 18, 'bold'), state='disabled')
ra_unit_text.place(x = 860, y = 230)

########################################################

ra_sr_label = tk.Label(frame1, text='Place of Test', bg= '#272727', fg='#e6e6e6')
ra_sr_label.config(font=('Calibri', 18, 'bold'))
ra_sr_label.place(x = 1250, y = 190)

ra_sr_text = tk.Text(frame1, width=25, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
ra_sr_text.config(font=('Courier New', 18, 'bold'), state='disabled')
ra_sr_text.place(x = 1250, y = 230)

########################################################

project_label = tk.Label(frame1, text='Project', bg= '#272727', fg='#e6e6e6')
project_label.config(font=('Calibri', 18, 'bold'))
project_label.place(x = 470, y = 110)

project_text = tk.Text(frame1, width=25, height=1, border=0, bg="#4d4d4d", fg='#c4ff4d')
project_text.config(font=('Courier New', 18, 'bold'), state='disabled')
project_text.place(x = 470, y = 150)

#######################################################################################################
#######################################################################################################
################################# HEALTH CHECK COMMAND ################################################

health_tree = ttk.Treeview(frame1, column=('Byte No.','Description','Type','Expected'), show='headings', height=12)
health_tree.pack()

health_tree.column("# 1", anchor=CENTER)
health_tree.column("# 2", anchor=CENTER)
health_tree.column("# 3", anchor=CENTER)
health_tree.column("# 4", anchor=CENTER)

health_tree.heading("# 1", text="Byte No.")
health_tree.heading("# 2", text="Description")
health_tree.heading("# 3", text="Type")
health_tree.heading("# 4", text="Expected")

health_tree.place(x=25, y=600)

health_tree.insert('', 'end', text="1", values=('00-01','Header','Unsigned short','07E0'))
health_tree.insert('', 'end', text="1", values=('02','Message_ID','Unsigned char','A1'))
health_tree.insert('', 'end', text="1", values=('03','Sequence number','Unsigned char','()'))
health_tree.insert('', 'end', text="1", values=('04','Length of Data','Unsigned char','08'))
health_tree.insert('', 'end', text="1", values=('05','Health CMD ACK','Unsigned char','()'))
health_tree.insert('', 'end', text="1", values=('06-07','Version','Unsigned short','07E6'))
health_tree.insert('', 'end', text="1", values=('08-09','Revision','Unsigned short','000A'))
health_tree.insert('', 'end', text="1", values=('10','Health Status','Unsigned char','()'))
health_tree.insert('', 'end', text="1", values=('11','TX ON/OFF Status','Unsigned char','()'))
health_tree.insert('', 'end', text="1", values=('12','Reserved','Unsigned char','0D'))
health_tree.insert('', 'end', text="1", values=('13','Checksum','Unsigned char','()'))
health_tree.insert('', 'end', text="1", values=('14-15','Footer','Unsigned short','FFFF'))

received_tree = ttk.Treeview(frame1, column=('Received'), show='headings', height=12)
received_tree.pack()

received_tree.column("# 1", anchor=CENTER)

received_tree.heading("# 1", text="Received")

received_tree.place(x=850, y=600)

for i in range(12):
    received_tree.insert(parent='',index='end',text='', values=(""))
    received_tree.yview_moveto(1)

lst = ['ABC', 'DEF']

# received_tree.insert(parent='',index='end',text='', values=(lst[1]+lst[0]))

#######################################################################################################
#######################################################################################################
#######################################################################################################

#Scrrenshot button

ss_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/camera.png')

root.update()
take_ss = tk.Button(frame1, height=32, width=32, command=hide_window, bg='#272727')
take_ss.config(image=ss_icon)
take_ss["border"] = "0"
take_ss.place(x = 180, y = 40)

root.update()
take_ss = tk.Button(frame2, height=32, width=32, command=hide_window, bg='#272727')
take_ss.config(image=ss_icon)
take_ss["border"] = "0"
take_ss.place(x = 180, y = 40)

#Start/Stop buttons

start_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/play.png')
stop_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/stop.png')
configuration_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/settings.png')
health_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/heart.png')
pdf_icon = tk.PhotoImage(file=r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/pdf.png')

myFont = font.Font(size=12, weight='bold')

root.update()
start = tk.Button(frame1, height=32, width=32,command=lambda: plot_start(), bg='#272727')
start.config(image=start_icon)
start["border"] = "0"
start.place(x=20, y=40)

root.update()
stop = tk.Button(frame1, height=24, width=24, command=lambda: plot_stop(), bg='#272727')
stop.config(image=stop_icon)
stop["border"] = "0"
stop.place(x=60, y=44)

root.update()
configure = Button(frame1, height=32, width=32, command=lambda: config_obj.config_window(), bg='#272727')
configure.config(image=configuration_icon)
configure["border"] = "0"
configure.place(x=100, y=40)

root.update()
report_btn= tk.Button(frame1, height=32, width=32, bg='#272727', command=lambda: report_is_clicked())
report_btn.config(image=pdf_icon)
report_btn["border"] = "0"
report_btn.place(x=230, y=40)

root.update()
tx_on_full_btn = tk.Button(frame1, text="TX - ON_F", bg = 'green', fg='white', height = 1, width=10, command=lambda: tx_on_full())
tx_on_full_btn.place(x=280, y=42)
tx_on_full_btn['font'] = myFont

root.update()
tx_on_30_btn = tk.Button(frame1, text="TX - ON_30", bg = 'green', fg='white', height = 1, width=10, command=lambda: tx_on_30())
tx_on_30_btn.place(x=400, y=42)
tx_on_30_btn['font'] = myFont

root.update()
tx_off_btn = tk.Button(frame1, text="TX - OFF", bg = 'red', fg='yellow', height = 1, width=10, command=lambda: tx_off())
tx_off_btn.place(x=520, y=42)
tx_off_btn['font'] = myFont

# root.update()
# health_chk_btn = tk.Button(frame1, height = 32, width=32, bg='#272727', command=lambda: health_obj.health_window())
# health_chk_btn.config(image=health_icon)
# health_chk_btn["border"] = "0"
# health_chk_btn.place(x=140, y=40)

root.update()
bin_calc_btn = tk.Button(frame1, text="CALCULATE BIN", bg = 'yellow', fg='black', height = 1, width=14, command=lambda: bin_obj.bin_window())
bin_calc_btn.place(x=640, y=42)
bin_calc_btn['font'] = myFont

t1 = threading.Thread(target=plot_data)
t1.start()

t4 = threading.Thread(target=stat_update)
t4.start()

root.mainloop()