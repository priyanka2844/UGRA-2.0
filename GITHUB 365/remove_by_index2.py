def remove(list):

    msg_len = 7916

    new_msg_len = msg_len-40
    new_msg_len = int(new_msg_len/2)
    full_length = int(new_msg_len*2)

    indices = [0,1,2,3,4,new_msg_len-3,new_msg_len-2,new_msg_len-1,
               new_msg_len,new_msg_len+1,new_msg_len+2,new_msg_len+3,new_msg_len+4,full_length-3,full_length-2,full_length-1]
    
    # print(indices)


    # indices = [0,1,2,3,4,3935,3936,3937,3938,3939,3940,3941,3942,7873,7874,7875]

    list = [i for j, i in enumerate(list) if j not in indices]
    return list

# for 1020: 0,1,2,493,494,495,496,497,988,989
# for 1023: 0,1,2,339,340,341,342,343,680,681,682,683,684,1021,1022
# for 6604: 0,1,2,3,4,3281,3280,3279,3282,3283,3284,3285,3286,
# for 7916: 0,1,2,3,4,3935,3936,3937,3938,3939,3940,3941,3942,7873,7874,7875
# for 9228: 0,1,2,3,4592,4593,4594,4595,4596,4597,9186,9187,9188,9189,9226,9227