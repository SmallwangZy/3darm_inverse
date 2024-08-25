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
STEP = 0.2

x0,y0,height = (0,18,12.8)
a0,a1,a2 = CompleteInverse(x0,y0,height)
Command(a0,a1,a2,delay=1000)

def on_key_event(event):
    global x0,y0,a0,a1,a2,cnt,height
    if event.name == 'up':
        y0 = y0 + STEP
        a0,a1,a2 = CompleteInverse(x0,y0,height)
        print("Up arrow key pressed")
        Command(a0,a1,a2,delay=500)
    elif event.name == 'down':
        y0 = y0 - STEP
        a0,a1,a2 = CompleteInverse(x0,y0,height)
        print("Down arrow key pressed")
        Command(a0,a1,a2,delay=500)
    elif event.name == 'left':
        x0 = x0 - STEP
        a0,a1,a2 = CompleteInverse(x0,y0,height)
        print("Left arrow key pressed")
        Command(a0,a1,a2,delay=500)
    elif event.name == 'right':
        x0 = x0 + STEP
        a0,a1,a2 = CompleteInverse(x0,y0,height)
        print("Right arrow key pressed")
        Command(a0,a1,a2,delay=500)
    elif event.name == 'w':
        height = height + STEP
        print(height)
        a0,a1,a2 = CompleteInverse(x0,y0,height)
        print("W key pressed")
        Command(a0,a1,a2,delay=500)
    elif event.name == 's':
        height = height - STEP
        print(height)
        a0,a1,a2 = CompleteInverse(x0,y0,height)
        print("S key pressed")
        Command(a0,a1,a2,delay=500)
    elif event.name == 'space':
        cnt = cnt + 1
        cnt = cnt % 2
        print(cnt)
        if cnt == 0:
            ser.write("#005P1500T9999!".encode('utf-8'))
        else:
            ser.write("#005P2500T9999!".encode('utf-8'))
        print("Space key pressed")  
    print('x:{},y:{},z:{}'.format(x0,y0,height))

# 监听键盘事件
print('start')
keyboard.on_press(on_key_event)

# 保持程序运行
keyboard.wait('esc')  # 按下ESC键退出程序

ser.close()

