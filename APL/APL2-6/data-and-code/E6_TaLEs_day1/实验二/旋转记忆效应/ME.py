import cv2
import numpy as np
from skimage import io, color, restoration, img_as_ubyte
import matplotlib.pyplot as plt

# 图像读取与预处理
R = io.imread('大角度旋转\参考物.png')
R_D = io.imread('大角度旋转\参考散斑.png')
U_D = io.imread('大角度旋转\未知物散斑.png')


# 转换为灰度图并归一化
R = color.rgb2gray(R)
R_D = color.rgb2gray(R_D)
U_D = color.rgb2gray(U_D)

# 数据类型转换（关键修改点）
R_D_np = img_as_ubyte(R_D)  # 转换为uint8
U_np = img_as_ubyte(U_D)      # 转换为uint8

# 点扩散函数（PSF）计算 [1,2,3](@ref)
PSF, _ = restoration.unsupervised_wiener(R_D, R)
plt.figure()
plt.imshow(np.abs(PSF), cmap='hot')
plt.axis('off')
plt.savefig('大角度旋转\点扩散函数_PSF2.png')  # 保存图像
# plt.show()

# 维纳滤波恢复 [2](@ref)
U_restored, _ = restoration.unsupervised_wiener(U_D, PSF)
plt.figure()
plt.imshow(U_restored)
plt.axis('equal')
plt.savefig('大角度旋转\恢复图像_维纳滤波2.png')  # 保存图像
# plt.show()

# 阈值分割优化 [2](@ref)
threshold = 0.25
U_th = np.clip(U_restored, 0, 1)
U_th[U_th > threshold] = 1
plt.figure()
plt.imshow(U_th, cmap='hot')
plt.axis('equal')
plt.savefig('大角度旋转\阈值分割图像2.png')  # 保存图像
# plt.show()

# 互相关系数计算 [4,5](@ref)
cross_corr = cv2.matchTemplate(R_D_np, U_np, cv2.TM_CCOEFF_NORMED)
plt.figure()
plt.imshow(cross_corr, cmap='hot', vmin=-1, vmax=1)
plt.axis('off')
plt.savefig('大角度旋转\互相关系数图2.png')  # 保存图像
# plt.show()

