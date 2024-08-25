import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import serial
import time

# 参数
L1 = 15.1
L2 = 16.5

distance =  15
flag = 1
delay = 2500
height = 6
index = 0

# 单位: cm
table = np.array([
    [-4,21],
    [0,21],
    [3,21],
    [-4,18],
    [0,18],
    [3,18],
    [-4,15],
    [0,15],
    [3,15]
])

fig1 = plt.figure()

def Convert0(angle):
    return int(((2400 - 500) / 180) * np.rad2deg(angle) + 500)

def Convert1(angle):
    return  2500 - int(((2500 - 500) / 180.0) * np.rad2deg(angle)) 

def Convert2(angle):
    return int(((2500 - 500) / 180) * np.rad2deg(angle) + 1500)

def Polar2xy(r,theta):
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return x,y

def XY2polar(x,y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y,x)
    return r,theta

def InverseG(x,y):
    atanxy = np.arctan2(y,x)
    comptheta1 = (x**2 + y**2 + L1**2 - L2**2)/(2*np.sqrt(x**2 + y**2)*L1)
    comptheta2 = (L1**2 + L2**2 - x**2 - y**2)/(2*L1*L2)
    if (np.abs(comptheta1) > 1) or (np.abs(comptheta2) > 1):
        print('out of range')
        exit
    else:
        theta1 = np.pi - (atanxy + np.arccos(comptheta1))
        theta2 = theta1 - np.arccos(comptheta2)
        return theta1,theta2

def Forward(theta1,theta2):
    ax = L1*np.cos(theta1)
    ay = L1*np.sin(theta1)
    bx = ax + L2*np.cos(theta2 + np.pi)
    by = ay + L2*np.sin(theta2 + np.pi)
    return ax,ay,bx,by

def CompleteInverse(x,y,z,height=6):
    r,a0 = XY2polar(x,y)
    a1,a2 = InverseG(r,height)
    print('角度0:{},角度1:{},角度2:{}'.format(np.rad2deg(a0),np.rad2deg(a1),np.rad2deg(a2)))
    return a0,a1,a2



def Command(a0,a1,a2,delay=3000,pdelay=9999):
    test_data = "#000P{}T{}!#001P{}T{}!#002P{}T{}!#005P{}T{}!".format(
            Convert0(a0),delay,
            Convert1(a1),delay,
            Convert2(a2),delay,
            1500,pdelay
        )
    print('PWM0:{},PWM1:{},PWM2:{}'.format(Convert0(a0),Convert1(a1),Convert2(a2)))
    data = '{' + test_data + '}'
    ser.write(data.encode('utf-8'))  # 发送数据，返回发送的字节数
    


device = "COM5"
ser = serial.Serial(device, 115200)    # 打开COM17，将波特率配置为115200，其余参数使用默认值
if ser.isOpen():                        # 判断串口是否成功打开
    print("打开串口成功。")
    print(ser.name)    # 输出串口号
else:
    print("打开串口失败。")
    exit


while True:
    time.sleep(5)
    index = index % 9
    print('\n当前遍历方格:{}'.format(index))
    a0,a1,a2 = CompleteInverse(table[index][0],table[index][1],height)
    Command(a0,a1,a2,delay=3500)
    index = index + 1    

    
    

ser.close()

