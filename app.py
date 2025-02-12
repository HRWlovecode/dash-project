import math
import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# 初始化 Dash 应用
app = dash.Dash(__name__)

# 初始参数
lambda_default = 20  # 顾客到达率
mu_artificial_default = 10  # 人工收银台服务率
mu_self_default = 8  # 自助收银台服务率
c_artificial_range = list(range(0, 21))  # 人工收银台 0-20
c_self_range = list(range(0, 21))  # 自助收银台 0-20
p_self_default = 0.7  # 选择自助收银台的比例


# 计算排队论公式
def P_wq(c, lambda_rate, mu):
    if c == 0 or lambda_rate == 0:
        return 0  # 没有收银台时，不存在排队
    rho = lambda_rate / (c * mu)
    if rho >= 1:
        return float('inf')
    sum_terms = sum([(lambda_rate / mu) ** k / math.factorial(k) for k in range(c)])
    denominator = sum_terms + ((lambda_rate / mu) ** c / math.factorial(c)) * (1 / (1 - rho))
    if denominator == 0:
        return 0
    P_0 = 1 / denominator
    return (lambda_rate / mu) ** c / (math.factorial(c)) * P_0


def average_waiting_time(c, lambda_rate, mu):
    if c == 0 or lambda_rate == 0:
        return 0  # 没有收银台时，不存在等待时间
    P_wq_value = P_wq(c, lambda_rate, mu)
    denominator = (c * mu - lambda_rate)
    if denominator <= 0:
        return float('inf')
    return P_wq_value / denominator


def average_customers_in_system(c, lambda_rate, mu):
    if c == 0 or lambda_rate == 0:
        return 0  # 没有收银台时，系统中没有顾客
    P_wq_value = P_wq(c, lambda_rate, mu)
    denominator = (c * mu - lambda_rate)
    if denominator <= 0:
        return float('inf')
    return P_wq_value * lambda_rate / denominator


# Dash 组件布局
app.layout = html.Div([
    html.H1("超市收银台优化模拟", style={'textAlign': 'center'}),

    html.Label("顾客到达率 (λ)"),
    dcc.Slider(5, 50, 1, value=lambda_default, id='lambda-slider', marks={i: str(i) for i in range(5, 51, 5)}),

    html.Label("人工收银台数量"),
    dcc.Slider(0, 20, 1, value=5, id='c-artificial-slider', marks={i: str(i) for i in range(0, 21, 2)}),

    html.Label("人工收银台服务率 (μ)"),
    dcc.Slider(5, 20, 1, value=mu_artificial_default, id='mu-artificial-slider',
               marks={i: str(i) for i in range(5, 21, 5)}),

    html.Label("自助收银台数量"),
    dcc.Slider(0, 20, 1, value=5, id='c-self-slider', marks={i: str(i) for i in range(0, 21, 2)}),

    html.Label("自助收银台服务率 (μ)"),
    dcc.Slider(5, 20, 1, value=mu_self_default, id='mu-self-slider', marks={i: str(i) for i in range(5, 21, 5)}),

    html.Label("选择自助收银台的顾客比例 (%)"),
    dcc.Slider(0, 1, 0.1, value=p_self_default, id='p-self-slider', marks={i / 10: f"{i * 10}%" for i in range(0, 11)}),

    dcc.Graph(id='queue-graph')
])


# 回调函数
@app.callback(
    Output('queue-graph', 'figure'),
    [Input('lambda-slider', 'value'),
     Input('c-artificial-slider', 'value'),
     Input('mu-artificial-slider', 'value'),
     Input('c-self-slider', 'value'),
     Input('mu-self-slider', 'value'),
     Input('p-self-slider', 'value')]
)
def update_graph(lambda_rate, c_artificial, mu_artificial, c_self, mu_self, p_self):
    p_artificial = 1 - p_self
    lambda_self = p_self * lambda_rate
    lambda_artificial = p_artificial * lambda_rate

    wait_times = []
    customers_in_system = []

    for c_self_test in c_self_range:
        wait_time_artificial = average_waiting_time(c_artificial, lambda_artificial, mu_artificial)
        customers_artificial = average_customers_in_system(c_artificial, lambda_artificial, mu_artificial)
        wait_time_self = average_waiting_time(c_self_test, lambda_self, mu_self)
        customers_self = average_customers_in_system(c_self_test, lambda_self, mu_self)

        total_wait_time = (p_self * wait_time_self) + (p_artificial * wait_time_artificial)
        total_customers = customers_artificial + customers_self

        wait_times.append(total_wait_time)
        customers_in_system.append(total_customers)

    # 创建动态图表
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=c_self_range, y=wait_times, mode='lines+markers', name='平均等待时间', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=c_self_range, y=customers_in_system, mode='lines+markers', name='系统中的顾客数',
                             line=dict(color='red'), yaxis="y2"))

    # 设置双 Y 轴
    fig.update_layout(
        title="自助收银台优化分析",
        xaxis_title="自助收银台数量",
        yaxis=dict(title="平均等待时间（小时）", titlefont=dict(color="blue"), tickfont=dict(color="blue")),
        yaxis2=dict(title="系统中的顾客数", titlefont=dict(color="red"), tickfont=dict(color="red"), overlaying="y",
                    side="right"),
        template="plotly_white"
    )

    return fig


# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
