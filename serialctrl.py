# 调用串口
import serial
import numpy as np
from matplotlib import pyplot as plt


     




device = "COM5"

# ser = serial.Serial(device, 115200)    # 打开COM17，将波特率配置为115200，其余参数使用默认值
# if ser.isOpen():                        # 判断串口是否成功打开
#     print("打开串口成功。")
#     print(ser.name)    # 输出串口号
# else:
#     print("打开串口失败。")

# test_data = "#000P1700T1000!"

# 串口发送 ABCDEFG，并输出发送的字节数。


# test_data = make_command
# write_len = ser.write(test_data.encode('utf-8'))  # 发送数据，返回发送的字节数
# print("串口发出{}个字节。".format(write_len)) 
# ser.close()

