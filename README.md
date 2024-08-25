# 3darm_inverse
a simulation program for inverse motion of 3darm using Python, aiming to play chess with machine arm

# 逆运动学

逆运动学是指输入通过已知位姿得到控制量参数的过程, 具体来说就是：

$$
\theta_1=f(x, y), \theta_2=g(x, y)
$$


设足尖顶点为 P 点, 坐标为 $(x, y)$, 设直线 OB 与 x 轴形成的夹角为 $\angle B$, 则有:

$$
\cos \angle P=\frac{x}{\sqrt{x^2+y^2}}, \angle P=\arccos \frac{x}{\sqrt{x^2+y^2}}
$$

而在由两杆 $L_1, L_2$ 和边 OP 构成的三角形中, 可以构造出余弦定理公式:

$$
\cos \left(\angle P-\theta_1\right)=\frac{L_1^2+x^2+y^2-L_2^2}{2 L_1 \sqrt{x^2+y^2}}
$$

因此可以得出：

$$
\begin{aligned}
\theta_1 & =\angle P-\arccos \frac{L_1^2+x^2+y^2-L_2^2}{2 L_1 \sqrt{x^2+y^2}} \\
& =\arccos \frac{x}{\sqrt{x^2+y^2}}-\arccos \frac{L_1^2+x^2+y^2-L_2^2}{2 L_1 \sqrt{x^2+y^2}}
\end{aligned}
$$

公式6中只含有θ2和x, y参数，因此可以由该方程唯一确定出关于θ2的逆运动学方程：

$$
\theta_2=\pi-\arccos\frac{L_1^2+L_2^2-(x^2+y^2}{2L_1L_2}
$$


至此, $\theta_1$ 的逆运动学方程已经给出, 现在围绕 $\theta_2$ 进行求解。对 $\theta_2$ 的补角 $\pi-\theta_2$ 所在的三角形使用余弦定理:

$$
\cos \left(\pi-\theta_2\right)=\frac{L_1^2+L_2^2-\left(x^2+y^2\right)}{2 L_1 L_2}
$$

![image-20240825130858611](https://wang-250-notes-1320145649.cos.ap-nanjing.myqcloud.com/Markdown/image-20240825130858611.png?imageSlim)

因此逆运动学方程解的公式为:

$$
\left\{\begin{array}{l}
\theta_1=\arccos \frac{x}{\sqrt{x^2+y^2}}-\arccos \frac{L_1^2+x^2+y^2-L_2^2}{2 L_1 \sqrt{x^2+y^2}} \\
\theta_2=\pi-\arccos \frac{L_1^2+L_2^2-\left(x^2+y^2\right)}{2 L_1 L_2}
\end{array}\right.
$$


若要使足尖 $P$ 点轨迹为直线运动，且沿着 $x$ 轴的方向， $P$ 点纵坐标 $y$ 需要恒定为一个常数。在此约束条件下，求解出所有满足限制的x。这里还需要注意使用到了 $\arccos$ 函数， arccos函数是有定义域限制的，满足 $[-1,1]$ 之间，程序需要判断是否处于定义域内。否则程序将出错。在程序中累加x或者累减x，根据公式 8 求解即可。

因为题目要求的是往复运动，因此到达足尖到达一个边界点后应该从该边界点反方向出发，而不是重新回到起点。整个系统的程序流程图如下：

![image-20240825131014131](https://wang-250-notes-1320145649.cos.ap-nanjing.myqcloud.com/Markdown/image-20240825131014131.png?imageSlim)

# 正运动学及仿真

正运动学与逆运动学相反, 正运动学的过程是给定控制量 $\theta_1$ 和 $\theta_2$, 推算出位姿, 即足尖的坐标。可以基于解三角形的方法实现, 但使用齐次变换矩阵的方式更容易理解, 并且在高自由度的时候,解三角形方法就难以分析了。首先介绍什么是齐次坐标, 对于二维空间中的一个点 $(x, y)$, 其齐次坐标是一个三维向量 $(x, y, 1)$ :

$$
\boldsymbol{x}=[\begin{array}{l}
x \\
y
\end{array}] \Rightarrow \overline{\boldsymbol{x}}=[\begin{array}{l}
x \\
y \\
1
\end{array}]
$$


通俗易懂的讲, 坐标可以拉伸, 这意味着可以用相同的向量表示不同的坐标, 只要这些坐标是线性相关的, 而针对坐标还有旋转的操作, 旋转和拉伸构成了空间中所有的操作。齐次的本质就是增加了一个维度, 因此二维坐标下的引出齐次变换矩阵:

$$
\operatorname{Rot}(z, \theta)=\left[\begin{array}{ccc}
\cos \theta & -\sin \theta & t_x \\
\sin \theta & \cos \theta & t_y \\
0 & 0 & 1
\end{array}\right]
$$


坐标系变换涉及到了齐次变换矩阵, 参考图7, 假设 P 点是第一个关节点, 向量 $\overrightarrow{O P}$ 与 $x$ 轴形成的夹角为 $\theta$, 坐标为 $\left(t_x, t_y\right.$ )。点 E 是足尖, 其在由 $\vec{O}_0 Y_0, O_0 X_0$ 两个正交基底构成的绝对坐标系（以原始坐标系为参考）下的坐标为 $\left(E_x, E_y\right)$, 齐次坐标记为 $\vec{E}$, 而在以 $\vec{O}_2 Y_2, O_2 \overrightarrow{X_2}$ 两基底构成的坐标系下的坐标为 $\left(E_x^{\prime}, E_y^{\prime}\right)$, 齐次坐标记为 $\vec{E}^{\prime}$ 则:

$$
\begin{aligned}
\vec{E} & =\operatorname{Rot}(\varphi) \cdot T(\vec{P}) \cdot \operatorname{Rot}(\theta) \cdot \vec{E} \\
& =\left[\begin{array}{ccc}
\cos \varphi & -\sin \varphi & 0 \\
\sin \varphi & \cos \varphi & 0 \\
0 & 0 & 1
\end{array}\right] \cdot\left[\begin{array}{ccc}
1 & 0 & P_x \\
0 & 1 & P_y \\
0 & 0 & 1
\end{array}\right] \cdot\left[\begin{array}{ccc}
\cos \theta & -\sin \theta & 0 \\
\sin \theta & \cos \theta & 0 \\
0 & 0 & 1
\end{array}\right] \cdot \vec{E}^{\prime}
\end{aligned}
$$


其实可以将旋转和平移 (缩放) 归为一类, 不必要如此麻烦, 只使用一次齐次变换矩阵。我们接着采用如图10中的模型, 第一个关节的坐标 $P_1$ 可以利用 $\theta_1$ 来表示, 第二个关节的坐标 $P_2$ 可以利用 $\theta_2$ 来表示:

$$
\left[\begin{array}{c}
P_{2 x} \\
P_{2 y} \\
1
\end{array}\right]=\left[\begin{array}{ccc}
\cos \theta_1 & -\sin \theta_1 & L_1 \cos \theta_1 \\
\sin \theta_1 & \cos \theta_1 & L_1 \sin \theta_1 \\
0 & 0 & 1
\end{array}\right] \cdot\left[\begin{array}{c}
L_2 \cos \theta_2 \\
L_2 \sin \theta_2 \\
1
\end{array}\right]
$$

求解得到, 绝对的世界坐标系下的 $P_2$ 坐标为:

$$
\begin{cases}P_{2 x} & =L_2 * \cos \left(\theta_1+\theta_2\right)+L_1 * \cos \theta_1 \\ P_{2 y} & =L_2 * \sin \left(\theta_1+\theta_2\right)+L_1 * \sin \theta_1\end{cases}
$$


利用正运动学方程（13）可以帮助我们进行python仿真，它并不是毫无意义的。通过python代码仿真, 我们可以描绘出模拟机械臂的轨迹, 近似等于一条直线。
