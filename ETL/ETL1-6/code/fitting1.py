import math
import cmath


import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 设置全局字号大小和图像尺寸
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 20,
    'axes.labelsize': 24,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'legend.fontsize': 20,
    'figure.figsize': (8.27, 11.69)
})

# 读取Excel文件中的数据
df = pd.read_excel('ET1_6data_else.xlsx', sheet_name='RL相频')

# 提取需要拟合的数据列
# 将x_data和y_data转换为numpy数组
x_data = np.array(df['f'])
y_data = np.array(df['Δφ（示波器自动测定）'])


# 定义要拟合的函数模型
def func(w,R,L,C):
    return  np.angle((R+1j*w*L)/(-w**2*C*L+1j*w*C*R+1))


initial_guess = [1, 0.001, 0.1]
# 使用curve_fit进行拟合
popt, pcov = curve_fit(func, x_data, y_data, p0=initial_guess)

# 计算相关系数
residuals = y_data - func(x_data, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r_squared = 1 - (ss_res / ss_tot)

# 输出拟合参数
print("拟合参数:", popt)
print("相关系数:", r_squared)
x_plot = np.linspace(10, 100000, num=1000)

# 绘制拟合结果
plt.figure()
plt.scatter(x_data, y_data, label='$DataPoint$')

# plt.plot(x_plot, func(x_plot, *popt), 'r-', label='$Fitting$:  bias_1=%5.3f mV, bias_2=%5.3f mV,bias_3=%5.3f mV, $R^2$=%.6f ' % (*popt, r_squared))
plt.plot(x_plot, func(x_plot, *popt), 'r-')

# plt.xlabel('T/K', fontsize=20)
plt.xlabel('f')
# plt.ylabel('U/mV', fontsize=20)
plt.ylabel('$\\phi$')

# plt.legend(fontsize='large')
plt.legend()
plt.show()
