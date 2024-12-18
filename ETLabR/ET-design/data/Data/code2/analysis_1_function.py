# analysis_1_function.py
# copyright@pifuyuini
# 仅供实验小组成员使用
# 封装用于数据处理的函数

# 导入必要的库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import os

# 绘图设置
# 风格
plt.style.use('seaborn-v0_8-whitegrid')
# 全局设置
config = {'font.family':'Times New Roman', 'figure.dpi':500, 'figure.figsize':(10,8), 'axes.labelsize':20}
plt.rcParams.update(config)

# 定义拟合函数（用来拟合平稳区域的高低电平值）
def flat_line(x, a):
    return a * np.ones_like(x)

# 交点的计算方法
def find_intersection(x, y, level):
    """找到信号 y 与水平线 level 的交点"""
    intersections = []
    for i in range(len(y) - 1):
        if (y[i] > level and y[i + 1] < level) or (y[i] < level and y[i + 1] > level):
            # 线性插值计算交点
            t = (level - y[i]) / (y[i + 1] - y[i])
            intersection_time = x[i] + t * (x[i + 1] - x[i])
            intersections.append(intersection_time)
    return intersections

# 数据处理主函数
def main_analysis(data):
    '''
    The main function for processing data returns the relevant data of a shutter at a certain voltage.

    Parameters:
    data: pandas.DataFrame

    Return:
    (rise_time, fall_time, rise_response_time, fall_response_time)
    '''
    # 加载数据
    time = data['Time(s)'].values
    ch1 = data['CH1(V)'].values
    ch2 = data['CH2(V)'].values
    # 滤波
    window_length = 1511  # 窗口长度，可以根据实际情况调整
    polyorder = 3       # 多项式阶数，一般为2或3
    CH1 = savgol_filter(ch1, window_length, polyorder)
    CH2 = savgol_filter(ch2, window_length, polyorder)
    # 找到 CH1 左右跃变点
    CH1_threshold = (np.max(CH1) + np.min(CH1)) / 2  # 动态阈值
    CH1_left_index = np.where((CH1[:-1] < CH1_threshold) & (CH1[1:] > CH1_threshold))[0][0]
    CH1_right_index = np.where((CH1[:-1] > CH1_threshold) & (CH1[1:] < CH1_threshold))[0][0]
    CH1_left_time = time[CH1_left_index]
    CH1_right_time = time[CH1_right_index]
    # 拟合 CH2 信号高低电平值
    high_indices = np.where(CH2 > (np.max(CH2) + np.min(CH2)) / 2)[0]
    low_indices = np.where(CH2 < (np.max(CH2) + np.min(CH2)) / 2)[0]
    # 高电平拟合
    popt_high, _ = curve_fit(flat_line, time[high_indices], CH2[high_indices])
    CH2_high_level = popt_high[0]
    # 低电平拟合
    popt_low, _ = curve_fit(flat_line, time[low_indices], CH2[low_indices])
    CH2_low_level = popt_low[0]
    # 找到 CH2 的下降开始时间
    CH2_fall_start_index = np.where((CH2[:-1] > CH2_high_level) & (CH2[1:] < CH2_high_level))[0][0]
    CH2_fall_start_time = time[CH2_fall_start_index]
    # 找到停止下降和开始上升时间点：通过低电平拟合直线与信号曲线交点
    # 找低电平交点
    low_intersections = find_intersection(time, CH2, CH2_low_level)
    # 确定停止下降和开始上升的时间点
    if len(low_intersections) >= 2:
        CH2_rise_start_time = low_intersections[0]  # 第一个交点为停止下降时间点
        CH2_fall_end_time = low_intersections[1]  # 第二个交点为开始上升时间点
    else:
        raise ValueError("未找到低电平的两个交点，请检查数据质量")
    # 计算下降时间和上升时间
    CH2_fall_duration = CH2_fall_end_time - CH2_fall_start_time
    # 找到 CH2 上升结束时间
    CH2_rise_end_index = np.where((CH2[:-1] < CH2_high_level) & (CH2[1:] > CH2_high_level))[0][0]
    CH2_rise_end_time = time[CH2_rise_end_index]
    CH2_rise_duration = CH2_rise_end_time - CH2_rise_start_time
    # 计算响应时间
    rise_response_time = CH2_rise_start_time - CH1_left_time
    fall_response_time = CH2_fall_start_time - CH1_right_time
    # 返回指定数据
    return (CH2_rise_duration, CH2_fall_duration, rise_response_time, fall_response_time)

def data_integration(file_path):
    '''
    Integration of all data analysis results of a single shutter.

    Parameters:
    file_path: string, corresponding to a shutter

    Return:
    (voltage_group, rise_time_group, fall_time_group, rise_response_time_group, fall_response_time_group)
    '''
    voltage_group = []
    rise_time_group = []
    fall_time_group = []
    rise_response_time_group = []
    fall_response_time_group = []
    # 遍历文件夹中的所有文件
    for file_name in os.listdir(file_path):
        # 检查是否是CSV文件
        if file_name.endswith(".csv"):
            try:
                # 提取文件名后两位的数字
                voltage = float(file_name.split()[-1].replace(".csv", ""))
                # 读取CSV文件为DataFrame
                file_full_path = os.path.join(file_path, file_name)
                data = pd.read_csv(file_full_path)
                voltage_group.append(voltage)
                outcome = main_analysis(data)
                rise_time_group.append(outcome[0])
                fall_time_group.append(outcome[1])
                rise_response_time_group.append(outcome[2])
                fall_response_time_group.append(outcome[3])
            except ValueError as e:
                print(f"Error processing file {file_name}: {e}")
    voltage_group = np.array(voltage_group)
    rise_time_group = np.array(rise_time_group)
    fall_time_group = np.array(fall_time_group)
    rise_response_time_group = np.array(rise_response_time_group)
    fall_response_time_group = np.array(fall_response_time_group)
    return (voltage_group, rise_time_group, fall_time_group, rise_response_time_group, fall_response_time_group)

def main_plot(outcome, name='Shutter'):
    '''
    The main drawing function draws the rising response time-voltage scatter plot and the falling response time-voltage scatter plot.

    Parameters:
    outcome: tuple (numpy.ndarray), the integrated data about a shutter given by the function data_integration

    Return:
    None
    '''
    # Load data
    voltage = outcome[0]
    rise_response_time_group = outcome[3]
    fall_response_time_group = outcome[4]
    # Plot rise
    plt.figure()
    plt.scatter(voltage, rise_response_time_group)
    plt.title('Scatter Plot of Rise Response Time vs. Voltage of ' + name, fontsize=20)
    plt.xlabel('Voltage [0.1V]')
    plt.ylabel('Response Time [s]')
    plt.show()
    # Plot fall
    plt.figure()
    plt.scatter(voltage, fall_response_time_group)
    plt.title('Scatter Plot of Fall Response Time vs. Voltage of ' + name, fontsize=20)
    plt.xlabel('Voltage [0.1V]')
    plt.ylabel('Response Time [s]')
    plt.show()
    return None