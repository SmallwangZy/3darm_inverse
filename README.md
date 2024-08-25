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

至此, $\theta_1$ 的逆运动学方程已经给出, 现在围绕 $\theta_2$ 进行求解。对 $\theta_2$ 的补角 $\pi-\theta_2$ 所在的三角形使用余弦定理:

$$
\cos \left(\pi-\theta_2\right)=\frac{L_1^2+L_2^2-\left(x^2+y^2\right)}{2 L_1 L_2}
$$
