import pandas as pd
import matplotlib.pyplot as plt

# 从 Excel 文件中读取数据
excel_file = '负反馈放大电路.xlsx'  # 替换为你的 Excel 文件名
sheet_name = '幅频特性测量--闭环'  # 替换为你的工作表名称

# 使用 pandas 读取 Excel 数据
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# 假设数据列名为 'f/kHz' 和 'Uo/mV'，根据实际数据调整列名
x = df['f/kHz'] * 1000
y = df['Uo/mV']

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

# 添加峰值的横纵坐标
peak_x = x[y.idxmax()]
peak_y = y.max()
plt.plot(peak_x, peak_y, 'bo')  # 在峰值处标记一个蓝色圆点，并添加图例
plt.annotate(f'Peak ({peak_x:.2f}, {peak_y:.2f})', xy=(peak_x, peak_y), xytext=(peak_x, peak_y - 3),
             arrowprops=dict(facecolor='blue', shrink=0.05), color='blue', ha='center', fontsize=12)

plt.show()
