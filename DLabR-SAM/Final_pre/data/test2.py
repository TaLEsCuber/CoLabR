import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# 尝试作连续曲线的误差分析


df1 = pd.read_excel('S.A.M.Data1 (2).xlsx', sheet_name='工作表3')
x1 = np.array(df1['R (Ω)']) * 1000
y1 = np.array(df1['P(mW)'])

from sklearn.gaussian_process import GaussianProcessRegressor

# 计算高斯过程回归，使其符合 fit 数据点
gp = GaussianProcessRegressor()
gp.fit(x1[:, np.newaxis], y1)

xfit = np.linspace(0, max(x1), 1000)
yfit, std = gp.predict(xfit[:, np.newaxis], return_std=True)
dyfit = 2 * std  # 两倍sigma: 95%确定区域

# 可视化结果
plt.figure()
plt.plot(x1, y1, 'o', color='#e26e1b',label='Original Data')
plt.plot(xfit, yfit, '-', color='#3e324a', label='Fit Curve')

plt.fill_between(xfit, yfit - dyfit, yfit + dyfit,
                 color='#475d7b', alpha=0.2, label='Error')
plt.title('Gaussion Error')
plt.xlabel('$R_L$[ohm]')
plt.ylabel('Power[mW]')
plt.legend()
plt.grid(True)
plt.show()