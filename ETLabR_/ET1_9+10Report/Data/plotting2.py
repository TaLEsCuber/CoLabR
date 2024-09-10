import pandas as pd
import matplotlib.pyplot as plt

# 从 Excel 文件中读取数据
excel_file = '负反馈放大电路.xlsx'  # 替换为你的 Excel 文件名
sheet_name = '幅频特性测量--开环'  # 替换为你的工作表名称

# 使用 pandas 读取 Excel 数据
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# 假设数据列名为 'f/Hz' 和 'Uo/mV'，根据实际数据调整列名
x = df['f/Hz']
y = df['Uo/V'] * 1000

# 计算峰值的 0.707 倍
peak_value = y.max() * 0.707

# 创建连线图，横坐标使用对数坐标
plt.figure()
plt.plot(x, y, marker='o', label='Original Data')  # 使用 'plot' 函数绘制连线图，并添加标记点和图例
plt.axhline(y=peak_value, color='r', linestyle='--', label='0.707 Peak Value')  # 添加水平虚线
plt.xscale('log')  # 设置横坐标为对数坐标
plt.xlabel('Frequency (Hz)', fontsize=24)
plt.ylabel('$U_{0}$ (mV)', fontsize=24)
plt.title('Relationship Curve Between Output Voltage and Frequency', fontsize=24)
plt.grid(True, which="both", ls="--")
plt.legend(fontsize=12)  # 显示图例

# 找到水平虚线与图像交点的索引
idx_peak = (y - peak_value).abs().idxmin()

# 标出两个交点
plt.plot(x[idx_peak], y[idx_peak], 'ro')  # 在第一个交点处标记一个红色圆点，并添加图例
plt.text(x[idx_peak] + 15, y[idx_peak] - 0.03, f'({x[idx_peak]:.2f}, {y[idx_peak]:.2f})', color='r', ha='center', fontsize=12)
y_second_peak = y[y < peak_value].idxmax()
plt.plot(x[y_second_peak], y[y_second_peak], 'ro')  # 在第二个交点处标记一个红色圆点
plt.text(x[y_second_peak] - 1500, y[y_second_peak] - 0.03, f'({x[y_second_peak]:.2f}, {y[y_second_peak]:.2f})', color='r', ha='center', fontsize=12)

# 添加峰值的横纵坐标
peak_x = x[y.idxmax()]
peak_y = y.max()
plt.plot(peak_x, peak_y, 'bo')  # 在峰值处标记一个蓝色圆点，并添加图例
plt.annotate(f'Peak ({peak_x:.2f}, {peak_y:.2f})', xy=(peak_x, peak_y), xytext=(peak_x, peak_y - 0.08),
             arrowprops=dict(facecolor='blue', shrink=0.05), color='blue', ha='center', fontsize=12)

plt.show()
