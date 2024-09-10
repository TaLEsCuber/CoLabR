import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 从 Excel 文件中读取数据
excel_file = '负反馈放大电路.xlsx'  # 替换为你的 Excel 文件名

# 读取第一个工作表的数据
sheet_name1 = '幅频特性测量--开环'  # 替换为你的第一个工作表名称
df1 = pd.read_excel(excel_file, sheet_name=sheet_name1)
x1 = df1['f/Hz']
y1 = df1['Uo/V'] * 1000

# 读取第二个工作表的数据
sheet_name2 = '幅频特性测量--闭环3'  # 替换为你的第二个工作表名称
df2 = pd.read_excel(excel_file, sheet_name=sheet_name2)
x2 = df2['f/Hz']
y2 = df2['Uo/mV']

# 找到第一个数据集的峰值
peak_index1 = y1.idxmax()
peak_x1 = x1[peak_index1]
peak_y1 = y1[peak_index1]

# 找到第二个数据集的峰值
peak_index2 = y2.idxmax()
peak_x2 = x2[peak_index2]
peak_y2 = y2[peak_index2]

# 计算0.707倍峰值
threshold1 = 0.707 * peak_y1
threshold2 = 0.707 * peak_y2

# 函数：找到交点
def find_intersections(x, y, threshold):
    indices = np.where(np.diff(np.sign(y - threshold)))[0]
    intersections = [(np.interp(threshold, [y[i], y[i+1]], [x[i], x[i+1]]), threshold) for i in indices]
    return intersections

# 找到第一个数据集的0.707倍峰值的交点
intersections1 = find_intersections(x1, y1, threshold1)

# 找到第二个数据集的0.707倍峰值的交点
intersections2 = find_intersections(x2, y2, threshold2)

# 绘制第一个数据集的图表
plt.figure()
plt.plot(x1, y1, marker='o', label='Open Loop Data')

# 标注第一个数据集的峰值
plt.annotate(f'Peak\n({peak_x1:.2f}, {peak_y1:.2f})',
             xy=(peak_x1, peak_y1),
             xytext=(peak_x1, peak_y1 - 0.05 * peak_y1),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=12, color='red')

# 添加水平虚线
plt.axhline(y=threshold1, color='blue', linestyle='--', label='0.707 Peak')

# 标注第一个数据集的所有交点
for (ix, iy) in intersections1:
    plt.annotate(f'({ix:.2f}, {iy:.2f})',
                 xy=(ix, iy),
                 xytext=(ix, iy + 0.05 * iy),
                 arrowprops=dict(facecolor='blue', shrink=0.05),
                 fontsize=12, color='blue')

plt.xscale('log')  # 设置横坐标为对数坐标
plt.xlabel('Frequency (Hz)', fontsize=24)
plt.ylabel('$U_{0}$ (mV)', fontsize=24)
plt.title('Open Loop Output Voltage vs Frequency', fontsize=24)
plt.grid(True, which="both", ls="--")
plt.legend(fontsize=12)

# 保存或显示第一个图表
plt.show()

# 绘制第二个数据集的图表
plt.figure()
plt.plot(x2, y2, marker='o', label='Closed Loop Data')

# 标注第二个数据集的峰值
plt.annotate(f'Peak\n({peak_x2:.2f}, {peak_y2:.2f})',
             xy=(peak_x2, peak_y2),
             xytext=(peak_x2, peak_y2 - 0.05 * peak_y2),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=12, color='red')

# 添加水平虚线
plt.axhline(y=threshold2, color='blue', linestyle='--', label='0.707 Peak')

# 标注第二个数据集的所有交点
for (ix, iy) in intersections2:
    plt.annotate(f'({ix:.2f}, {iy:.2f})',
                 xy=(ix, iy),
                 xytext=(ix, iy + 0.05 * iy),
                 arrowprops=dict(facecolor='blue', shrink=0.05),
                 fontsize=12, color='blue')

plt.xscale('log')  # 设置横坐标为对数坐标
plt.xlabel('Frequency (Hz)', fontsize=24)
plt.ylabel('$U_{0}$ (mV)', fontsize=24)
plt.title('Closed Loop Output Voltage vs Frequency', fontsize=24)
plt.grid(True, which="both", ls="--")
plt.legend(fontsize=12)

# 保存或显示第二个图表
plt.show()
