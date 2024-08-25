import numpy as np

class myarm:
    def __init__(self,l1=10.25,l2=12.2,l3=12.5):
        self.L1 = l1
        self.L2 = l2
        self.L3 = l3

    def angle2pwm(self,index,angle):
        if(index == 0):
            return ((2500-500) / 180) * angle + 500
        elif(index == 1):
            return -1
        elif(index == 2):
            return ((2500-1500) / 90) * angle + 1500
        else:
            return ((900 - 1500) / 90) * angle + 2100
        
    def Inverse(self,x,y):
        tem1 = (self.L1**2 + self.L2**2 - ( x **2 + y **2 )) / (2*self.L1*self.L2)
        tem2 = (self.L1**2 + (x**2 + y**2) - self.L2**2) / (2*self.L1*np.sqrt(x**2 + y**2))
        tem3 = (self.L2**2 + (x**2 + y**2) - self.L1**2) / (2*self.L2*np.sqrt(x**2 + y**2))
        if (np.abs(tem1) <= 1) and (np.abs(tem2) <= 1) and (np.abs(tem3) <= 1): 
            # 余弦定理计算夹角thetaT
            thetaT = np.arccos(tem1)
            # 求出补角theta2
            theta2 = np.pi - thetaT
            # 求出角theta1
            a = np.arctan(y/x)
            theta1 = a + np.arccos(tem2)
            # 计算第三个轴
            theta3 = np.arctan(x/y) + np.arccos(tem3)
            if (np.rad2deg(theta1) > 0 and np.rad2deg(theta1) < 90) and (np.rad2deg(theta2) > 0 and np.rad2deg(theta2) < 90) and (np.rad2deg(theta3) > 0 and np.rad2deg(theta3) < 180):
                return theta1, theta2, theta3
            else:
                # print('角度越界,已返回')
                return -1
        else:
            # print('arccos函数越界,已返回')
            return -1
        
    def Forward(self,theta1,theta2,theta3):
        ax = self.L1*np.cos(theta1)
        ay = self.L1*np.sin(theta1)

        bx = ax + self.L2*np.cos(theta1 - theta2)
        by = ay + self.L2*np.sin(theta1 - theta2)

        cx = bx
        cy = by - self.L3
        return ax,ay,bx,by,cx,cy


    def make_command(self,theta1, time1,theta2,time2, theta3,time3,Draw,time4):
        return "{#000P{}T{}!#001P{}T{}!#002P{}T{}!#003P{}T{}!#004P{}T{}!}".format(
            self.angle2pwm(0,theta1), time1, 
            self.angle2pwm(1,theta2), time2,
            self.angle2pwm(2,theta3), time3,
            Draw, time4)