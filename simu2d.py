import numpy as np
from matplotlib import pyplot as plt
import myarm as mine
from tqdm import tqdm

arm = mine.myarm()

fig1 = plt.figure()

a1,a2,a3 = arm.Inverse(18,12)
print(np.rad2deg(a1),np.rad2deg(a2),np.rad2deg(a3))

ax,ay,bx,by,cx,cy = arm.Forward(a1,a2,a3)

# 创建一个包含2个子图的图形

plt.plot([0, ax, bx, cx], [0, ay, by, cy], 'o-')
plt.title('Random Point State')


# fig2 = plt.figure()

# x = np.arange(-50,50,0.01)
# y = np.arange(-50,50,0.01)
# xsolve = []
# ysolve = []
# for xi in tqdm(x):
#     for yi in y:
#         if arm.Inverse(xi,yi) == -1:
#             continue
#         else:
#             xsolve.append(xi)
#             ysolve.append(yi)

# plt.plot(xsolve,ysolve,'o')
plt.show()

