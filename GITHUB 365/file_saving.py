#############################################################################################
################################ Features included ##########################################
# 1.  File saving feature with format enabled  
#############################################################################################

import time
import os

class save_file():

    def setup_file(self):

        try:
            location = 'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Records'
            inner_location = location + '/' + time.strftime("%Y-%m-%d")
            actual_location = inner_location + '/' + time.strftime("%H-%M-%S")

            if(os.path.exists(location)):
                pass
            else:
                os.makedirs(location)

            if(os.path.exists(inner_location)):
                pass
            else:
                os.makedirs(inner_location)

            if(os.path.exists(actual_location)):
                pass
            else:
                os.makedirs(actual_location)

            # self.fft_up.write('     '+"SEQUENCE".ljust(20,' ')+"  SNR UP".ljust(20,' ')+"  SNR DOWN".ljust(20,' ')+"  FB UP".ljust(20,' ')+"  FB DOWN".ljust(20,' ')+"  FD".ljust(20,' ')+"  ALTITUDE".ljust(20,' ')+"FR".ljust(20,' ')+"TIME".ljust(20,' ')+"VALIDITY".ljust(20,' ')+"LATITUDE".ljust(20,' ')+"LONGITUDE".ljust(20,' ')+"GPS_ALTITUDE".ljust(20,' ')+"GPS_TIME".ljust(20,' ')+"\n")
            
            #Save FFT UP message
            self.fft_up = actual_location + "/fft_up.txt"
            self.fft_up = open(self.fft_up, mode='a')
            self.fft_up.write('\n'+"**********RS-422*****session started*****"+time.strftime(" %d-%m-%Y ")+"***** at ***** "+time.strftime(" %H:%M **********")+'\n')
            self.fft_up.write(' Sr.No.'.ljust(10,' ')+'\n')
            self.fft_up.flush()

            #Save FFT DOWN message
            self.fft_down = actual_location + "/fft_down.txt"
            self.fft_down = open(self.fft_down, mode='a')
            self.fft_down.write('\n'+"**********RS-422*****session started*****"+time.strftime(" %d-%m-%Y ")+"***** at ***** "+time.strftime(" %H:%M **********")+'\n')
            self.fft_down.write(' Sr.No.'.ljust(10,' ')+'\n')
            self.fft_down.flush()

            #Save Params message
            self.params = actual_location + "/params.txt"
            self.params = open(self.params, mode='a')
            self.params.write('\n'+"**********RS-422*****session started*****"+time.strftime(" %d-%m-%Y ")+"***** at ***** "+time.strftime(" %H:%M **********")+'\n')
            self.params.write(' Sr.No.'.ljust(10,' ')+'\n')
            self.params.flush()

        except:
            print('Error setting file')

    def save_record(self, l1, l2, l3, seq_id):  #l2, l3, 
        
        try:
            
            line1 = ' '+str(seq_id).ljust(10,' ')
            for i in l1:
                line1 = line1 + str(i).ljust(10,' ')
            self.fft_up.write(line1+'\n')
            self.fft_up.flush()

            line2 = ' '+str(seq_id).ljust(10,' ')
            for i in l2:
                line2 = line2 + str(i).ljust(10,' ')
            self.fft_down.write(line2+'\n')
            self.fft_down.flush()

            line3 = ' '+str(seq_id).ljust(10,' ')
            for i in l3:
                line3 = line3 + str(i).ljust(10,' ')
            self.params.write(line3+'\n')
            self.params.flush()

        except:
            print("Error writing to file")

    def save_record_30(self, l3, seq_id):
        
        try:

            line3 = ' '+str(seq_id).ljust(10,' ')
            for i in l3:
                line3 = line3 + str(i).ljust(10,' ')
            self.params.write(line3+'\n')
            self.params.flush()

        except:
            print("Error writing to file")


