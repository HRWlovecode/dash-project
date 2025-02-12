import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置中文字体
font = font_manager.FontProperties(fname="C:/Windows/Fonts/msyh.ttc")
plt.rcParams['font.family'] = font.get_name()

# 参数设置
lambda_rate = 40  # 总顾客到达率（顾客/小时）
p_self = 0.7  # 70% 顾客选择自助收银台
p_artificial = 1 - p_self  # 30% 选择人工收银台
mu_artificial = 10  # 每个人工收银员的服务率（顾客/小时）
mu_self = 8  # 每个自助收银台的服务率（顾客/小时）

# 顾客流量分配
lambda_self = p_self * lambda_rate  # 自助收银顾客流量
lambda_artificial = p_artificial * lambda_rate  # 人工收银顾客流量


# 计算P(Wq > 0)的公式
def P_wq(c, lambda_rate, mu):
    rho = lambda_rate / (c * mu)  # 系统利用率
    if rho >= 1:
        return float('inf')  # 避免ρ >= 1时的无穷大情况

    sum_terms = sum([(lambda_rate / mu) ** k / math.factorial(k) for k in range(c)])

    # 检查分母是否为零，避免除零错误
    denominator = sum_terms + ((lambda_rate / mu) ** c / math.factorial(c)) * (1 / (1 - rho))
    if denominator == 0:
        return 0  # 如果分母为0，直接返回0
    P_0 = 1 / denominator
    return (lambda_rate / mu) ** c / (math.factorial(c)) * P_0


# 计算平均等待时间 Wq
def average_waiting_time(c, lambda_rate, mu):
    P_wq_value = P_wq(c, lambda_rate, mu)
    denominator = (c * mu - lambda_rate)
    if denominator <= 0:
        return float('inf')  # 避免无效计算
    return P_wq_value / denominator


# 计算系统中顾客数 Lq
def average_customers_in_system(c, lambda_rate, mu):
    P_wq_value = P_wq(c, lambda_rate, mu)
    denominator = (c * mu - lambda_rate)
    if denominator <= 0:
        return float('inf')  # 避免无效计算
    return P_wq_value * lambda_rate / denominator


# 固定人工收银台数量，测试不同自助收银台数量
c_artificial = 5  # 设定人工收银台数量为5
c_values = np.arange(1, 11)  # 自助收银台数量从1到10
wait_times = []
customers_in_system = []

for c_self in c_values:
    # 计算人工收银台的等待时间和系统顾客数
    wait_time_artificial = average_waiting_time(c_artificial, lambda_artificial, mu_artificial)
    customers_artificial = average_customers_in_system(c_artificial, lambda_artificial, mu_artificial)

    # 计算自助收银台的等待时间和系统顾客数
    wait_time_self = average_waiting_time(c_self, lambda_self, mu_self)
    customers_self = average_customers_in_system(c_self, lambda_self, mu_self)

    # 总系统的平均等待时间（加权平均）
    total_wait_time = (p_self * wait_time_self) + (p_artificial * wait_time_artificial)
    total_customers = customers_artificial + customers_self  # 系统中的总顾客数

    # 存储结果
    wait_times.append(total_wait_time)
    customers_in_system.append(total_customers)

# 创建图像
fig, ax1 = plt.subplots(figsize=(10, 6))  # 调整图像大小，避免标题溢出

# 平均等待时间
ax1.set_xlabel('自助收银台数量', fontsize=14)
ax1.set_ylabel('平均等待时间（小时）', color='tab:blue', fontsize=14)
ax1.plot(c_values, wait_times, color='tab:blue', label='平均等待时间', linewidth=2)
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 创建第二个坐标轴，用于显示系统中的顾客数
ax2 = ax1.twinx()
ax2.set_ylabel('系统中的顾客数', color='tab:red', fontsize=14)
ax2.plot(c_values, customers_in_system, color='tab:red', label='系统中的顾客数', linewidth=2)
ax2.tick_params(axis='y', labelcolor='tab:red')

# 添加网格和美化背景
ax1.grid(True, linestyle='--', alpha=0.7)  # 添加网格线
fig.patch.set_facecolor('#f5f5f5')  # 设置背景颜色

# 设置标题
plt.title('自助收银台引入后的优化（顾客到达率: 40 每个收银员的服务率：10）', fontsize=16, fontweight='bold')

# 调整图表布局，避免标题溢出
fig.tight_layout(pad=3.0)

# 显示图表
plt.show()
