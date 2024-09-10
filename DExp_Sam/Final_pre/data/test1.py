import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 设置全局字体大小
plt.rcParams.update({'font.size': 20})

# 从Excel文件中读取数据
file_path = 'S.A.M.Data1.xlsx'
data = pd.read_excel(file_path)

# 假设数据在列 'RL/ohm' 和 'P/mW' 中
x_data = data['RL/ohm'].values
y_data = data['P/mW'].values * 0.001

# 定义拟合函数
def quadratic_function(R_L, E, R_s):
    return (E / (R_L + R_s))**2 * R_L

# 使用curve_fit进行拟合
initial_guess = [1, 1]  # 初始猜测参数
params, covariance = curve_fit(quadratic_function, x_data, y_data, p0=initial_guess)

# 获取拟合参数
E_fit, R_s_fit = params

# 输出拟合结果
print(f"拟合参数: E = {E_fit}, R_s = {R_s_fit}")

# 生成拟合曲线
y_fit = quadratic_function(x_data, *params)

# 找到拟合曲线的最大值及其对应的 x 值
max_y_fit = np.max(y_fit)
max_x_fit = x_data[np.argmax(y_fit)]

# 输出拟合曲线的最大值
print(f"拟合曲线的最大值: P_max = {max_y_fit:.4f} W 对应的 RL = {max_x_fit:.4f} ohm")

# 创建绘图
fig, ax = plt.subplots(figsize=(10, 6))  # 控制图像大小，例如 10x6 英寸

# 绘制数据点和拟合曲线
ax.scatter(x_data, y_data, label='Data Point')
ax.plot(x_data, y_fit , color='red', label=f' E = {E_fit:.4f}\n R_s = {R_s_fit:.4f}')
ax.set_xlabel('$R_L / \Omega$')
ax.set_ylabel('$P / W$')
ax.legend()

# 添加网格线
ax.grid(True)

# 显示图像
plt.show()
