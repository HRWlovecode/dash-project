from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# 配置 Selenium 和浏览器驱动路径
driver_path = 'C:/path/to/chromedriver.exe'  # ChromeDriver 路径
url = 'file:///C:/path/to/cyber_security_bubble_map_red_for_high_gci.html'  # 地图文件路径

# 配置无头浏览器（headless）模式
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')  # 设置分辨率

# 使用 Service 来指定 ChromeDriver 路径
service = Service(driver_path)

# 启动浏览器
driver = webdriver.Chrome(service=service, options=options)

# 打开地图文件
driver.get(url)

# 等待地图加载完成
time.sleep(3)

# 截图并保存
driver.save_screenshot('high_res_map.png')

# 关闭浏览器
driver.quit()
