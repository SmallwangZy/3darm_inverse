import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import serial
import time
import keyboard

# 参数
L1 = 15.1
L2 = 16.5

distance =  15
flag = 1
delay = 2500
height = 1
index = 0

refpos = [0.0,18.6,11.99999999999999993]
onepos = [-8.0999999999999999993,18,12.599999999999]

w3pos = [6.800000000000003,18.999999999999996,12.800000000000008]
_9pos = [3.2000000000000006,16.200000000000006,12.800000000000008]




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

def CompleteInverse(x,y,height):
    r,a0 = XY2polar(x,y)
    a1,a2 = InverseG(r,height)
    print('角度0:{},角度1:{},角度2:{}'.format(np.rad2deg(a0),np.rad2deg(a1),np.rad2deg(a2)))
    return a0,a1,a2



def Command(a0,a1,a2,delay=3000):
    if delay < 1000:
        test_data = "#000P{}T0{}!#001P{}T0{}!#002P{}T0{}!".format(
                    Convert0(a0),delay,
                    Convert1(a1),delay,
                    Convert2(a2),delay,
                )
    else:
        test_data = "#000P{}T{}!#001P{}T{}!#002P{}T{}!".format(
                Convert0(a0),delay,
                Convert1(a1),delay,
                Convert2(a2),delay,
            )
    print('PWM0:{},PWM1:{},PWM2:{}'.format(Convert0(a0),Convert1(a1),Convert2(a2)))
    data = '{' + test_data + '}'
    ser.write(data.encode('utf-8'))  # 发送数据，返回发送的字节数

def Direct(x,y,z,dely):
    a0,a1,a2 = CompleteInverse(x,y,z)
    Command(a0,a1,a2,delay=dely)
    

device = "COM5"
ser = serial.Serial(device, 115200)    # 打开COM17，将波特率配置为115200，其余参数使用默认值
if ser.isOpen():                        # 判断串口是否成功打开
    print("打开串口成功。")
    print(ser.name)    # 输出串口号
else:
    print("打开串口失败。")
    exit

x0 = 0
y0 = 18
a1,a2,a3 =0,0,0
cnt = 0
height = 15
STEP = 0.3

temp_height = 15


# 先指定在中心点
Direct(refpos[0],refpos[1],refpos[2],1000)
time.sleep(2)

# 移动到目标点
Direct(w3pos[0],w3pos[1],w3pos[2],1000)
time.sleep(2)

# 向下吸附
Direct(w3pos[0],w3pos[1],10.4,1000)
time.sleep(2)

# 开始抽气
ser.write("#005P2500T9999!".encode('utf-8'))
time.sleep(1)

# 回到中心点
Direct(refpos[0],refpos[1],temp_height ,1000)
time.sleep(3)

# 放到目标点
Direct(_9pos[0],_9pos[1],_9pos[2],1000)
time.sleep(2)

ser.write("#005P1500T9999!".encode('utf-8'))