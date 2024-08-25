import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import serial
import time

start0 = 1500
start1 = 1500
start2 = 1500

table = np.array([
    [1617,1252,1945],
    [0,0,1],
    [0,1,0],
    [0,1,1],
    [1474,0,0],
    [1,0,1],
    [1,1,0],
    [1,1,1]
])

def CalculateTime(pwm,ref):
    std = np.abs(pwm - ref)
    if std < 100:
        return 1000
    elif std < 300:
        return 1200
    elif std < 500:
        return 1500
    else:
        return 2000

def WriteCommand(data):
    ser.write(data.encode('utf-8'))

def PwmCommand(pwm0,pwm1,pwm2):
    time0 = CalculateTime(pwm0,ref=start0)
    time1 = CalculateTime(pwm1,ref=start1)
    time2 = CalculateTime(pwm2,ref=start2)
    test_data = "#000P{}T{}!#001P{}T{}!#002P{}T{}!".format(
        pwm0,'1000',
        pwm1,'1000',
        pwm2,'1000'
    )
    data = '{' + test_data + '}'
    print(data)
    ser.write(data.encode('utf-8'))


device = "COM5"
ser = serial.Serial(device, 115200)    # 打开COM17，将波特率配置为115200，其余参数使用默认值
if ser.isOpen():                        # 判断串口是否成功打开
    print("打开串口成功。")
    print(ser.name)    # 输出串口号
else:
    print("打开串口失败。")
    exit

PwmCommand(1705,1359,1570)

# WriteCommand("#000P{}T{}!".format(1659,'1000'))
# time.sleep(2)
# WriteCommand("#001P{}T{}!".format(1352,'1000'))
# WriteCommand("#002P{}T{}!".format(1663,'1000'))
