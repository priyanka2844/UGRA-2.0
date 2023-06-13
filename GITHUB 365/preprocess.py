import numpy as np
import math

class preprocessing():

    def slicer1(self, msg):
        temp = np.array([])
        for i in range(3, len(msg)-2):
            temp = np.append(temp, msg[i])
        return temp

    def slicer2(self, msg):
        temp = np.array([])
        for i in range(0, len(msg)-40):
            temp = np.append(temp, msg[i])
        return temp
    
    def process_30(self, msg):

        concat_list = self.slicer1(msg)

        concat_list = [msg[0]+msg[1], msg[2], msg[3], msg[4] + msg[5], msg[6] + msg[7], msg[8], msg[9], 
                    msg[10] + msg[11], msg[12] + msg[13], msg[14] + msg[15], msg[16] + msg[17], 
                    msg[18] + msg[19], msg[20] + msg[21], msg[22], msg[23] + msg[24]]
        
        for i in range(len(concat_list)):
            concat_list[i] = int(concat_list[i], 16)

        concat_list[9] =  float(20*math.log10(concat_list[9]))
        concat_list[9] = float("{:.3f}".format(concat_list[9]))
            
        concat_list[10] =  float(20*math.log10(concat_list[10]))
        concat_list[10] = float("{:.3f}".format(concat_list[10]))

        return concat_list

    def concat_plot_data(self, msg):

        concat_msg = [''.join(x) for x in zip(msg[0::2], msg[1::2])]
        return concat_msg

# import numpy as np
# import math

# class preprocessing():

#     def slicer1(self, msg):
#         temp = np.array([])
#         for i in range(3, len(msg)-2):
#             temp = np.append(temp, msg[i])
#         return temp

#     def slicer2(self, msg):   
#         temp = np.array([])
#         for i in range(0, len(msg)-30):
#             temp = np.append(temp, msg[i])
#         return temp
    
#     def process_30(self, msg):

#         temp = self.slicer1(msg)

#         concat_list = [temp[0]+temp[1], temp[2], temp[3], temp[4] + temp[5], temp[6] + temp[7], temp[8], temp[9], 
#                     temp[10] + temp[11], temp[12] + temp[13], temp[14] + temp[15], temp[16] + temp[17], 
#                     temp[18] + temp[19], temp[20] + temp[21], temp[22], temp[23] + temp[24]]
             
#         return concat_list
    
#     def convert_to_int(self, msg):

#         for i in range(len(msg)):
#             msg[i] = int(msg[i], 16)

#         msg[3] = msg[3]/10
#         msg[7] = msg[7]/10
#         msg[8] = msg[8]/10
#         msg[11] = msg[11]/10
#         msg[12] = msg[12]/10

#         msg[9] = 20 * (math.log10(msg[9]))
#         msg[10] = 20 * (math.log10(msg[10]))

#         msg[3] = "{:.3f}".format(msg[3])
#         msg[7] = "{:.3f}".format(msg[7])
#         msg[8] = "{:.3f}".format(msg[8])
#         msg[9] = "{:.3f}".format(msg[9])
#         msg[10] = "{:.3f}".format(msg[10])
#         msg[11] = "{:.3f}".format(msg[11])
#         msg[12] = "{:.3f}".format(msg[12])

#         return msg

#     def concat_plot_data(self, msg):

#         concat_msg = [''.join(x) for x in zip(msg[0::2], msg[1::2])]
#         return concat_msg