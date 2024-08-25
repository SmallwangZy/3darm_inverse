import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from matplotlib.animation import ArtistAnimation

L1 = 10.25
L2 = 12.2
L3 = 12.5











def Inverse(x,y):
    if((x**2 + y**2) > (L1**2 + L2**2)):
        return -1
    tem1 = (L1**2 + L2**2 - ( x **2 + y **2 )) / (2*L1*L2)
    tem2 = (L1**2 + (x**2 + y**2) - L2**2) / (2*L1*np.sqrt(x**2 + y**2))
    tem3 = (L2**2 + (x**2 + y**2) - L1**2) / (2*L2*np.sqrt(x**2 + y**2))
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
        return theta1, theta2, theta3
    else:
        print('arccos函数越界,已返回')
        return -1
    
STEP = 0.01

x = 25
y = 15

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

origin = [0,0,0]
target = [1,1,1]

# 创建一个点集，用于绘制直线
points = np.array([origin, target])

# 绘制原点和目标点
ax.scatter(points[:, 0], points[:, 1], points[:, 2], color=['r', 'b'])

# 绘制连接原点和目标点的直线
ax.plot(points[:, 0], points[:, 1], points[:, 2], color='k')

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 显示图形
plt.show()



# # 动画部分
# arts =[]
# fig = plt.figure (2)
# ax = fig.subplots()
# ax.grid ( True , linestyle ='--', which ='both', color ='gray', alpha =0.5) 
# ax.set_title (" Robotic arm trajectory description ")
# points = []





# for xi in x :
#     if(np.abs(xi/np.sqrt( xi **2 + y **2)) > 1) or (np.abs(( xi **2 + y **2 + L1 **2 -L2 **2) /(2*( L1 * np . sqrt ( xi **2 + y **2) ) ) ) > 1) :
#         print ('invaild x:{} '.format ( xi ))
#         break
#     else:
#         angle = np.arccos ( xi / np . sqrt ( xi **2 + y **2) )
#         angle1 = np.arccos (
#             ( xi **2 + y **2 + L1 **2 - L2 **2) /
#             (2*( L1 * np . sqrt ( xi **2 + y **2) ) )
#             )
#         phi2 = np . pi - np . arccos (
#             ( L1 **2 + L2 **2 - ( xi **2 + y **2) ) /
#             2 * L1 * L2
#             )
#         if angle1 < angle :
#             phi1 = angle - angle1
#         else :
#             phi1 = angle + angle1
#             phi2 = - phi2
#         Ax = L1 * np . cos (phi1) 
#         Ay = L1 * np . sin (phi1)

#         Bx = L2 *np.cos(phi1 + phi2) + Ax 
#         By = L2 * np.sin( phi1 + phi2 ) + Ay
#         points.append(( Ax , Ay )) 
#         points.append (( Bx , By ) )
#         lines = ax . plot ([0 , Ax , Bx ] , [0 , Ay , By ] , 'r') 
#         arts.append(lines)
# ax.plot (* zip(* points ) , 'bo ')
# ani = ArtistAnimation ( fig , arts , interval =200) 
# plt . show ()