# -*- coding: utf-8 -*-

import time
import os
import re
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service

# 将字符串中的非法字符替换成下划线，以防写文件时文件名非法
def clean_name(name):
    return re.sub(r'[\\/:*?"<>|\[\]]+', '_', name)

# 创建 ChromeOptions 对象设置启动参数
options = Options()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
# options.add_argument('headless') # 不打开浏览器
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument('--no-sandbox')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("blink-settings=imagesEnabled=false")
# options.page_load_strategy = "eager"

# 设置 chromedriver 路径（修改为你的实际路径）
chromedriver_path = r"D:\File\实习\CVTE\cvte_py\bilibili\chromedriver.exe"
# 创建 Service 对象，传入 chromedriver 路径
service = Service(chromedriver_path)
# 创建浏览器对象,并以设置的启动参数启动浏览器
browser = webdriver.Chrome(service=service, options=options)

browser.maximize_window()  # 使窗口最大化
data_save = []

url = 'https://www.bilibili.com/blackboard/era/afKE7dek7iNaaSKv.html'
time.sleep(1)
browser.get(url)
# time.sleep(1000)

# 等待页面加载（可以根据需要调整）
time.sleep(5)
try:
    # 找到账号输入框并输入账号
    username_input = browser.find_element(By.XPATH, "//input[@placeholder='请输入账号']")
    username_input.send_keys('18701748423')
    # 找到密码输入框并输入密码
    password_input = browser.find_element(By.XPATH, "//input[@placeholder='请输入密码']")
    password_input.send_keys('12450612jy')
    # 找到登录按钮（先去掉 `disabled` 属性）
    login_button = browser.find_element(By.XPATH, "//div[contains(@class, 'btn_primary')]")
    # 如果按钮有 `disabled` 类，则先去掉
    browser.execute_script("arguments[0].classList.remove('disabled');", login_button)
    # 点击登录按钮
    login_button.click()
    # 等待几秒，确保页面跳转
    time.sleep(10)
except:
    pass
time.sleep(2)
# time.sleep(2000)
# 定位到包含 "关注" 按钮的 div 元素
up_list = browser.find_element(By.CLASS_NAME, "up-list").find_element(By.CLASS_NAME, "list").find_elements(By.CLASS_NAME, "up-item-detail-pc")
print(len(up_list))
up_urls = []

count = 0
for up in up_list:
    up_image = up.find_element(By.CLASS_NAME, "info")
    up_image.click()
    time.sleep(2)
    windows = browser.window_handles  # 以列表的形式返回当前所有的窗口
    browser.switch_to.window(windows[1])  # 切换窗口
    current_url = browser.current_url
    up_urls.append(current_url)
    count += 1
    print(f"已完成: {count}")
    browser.close()
    browser.switch_to.window(windows[0])  # 切换窗口
    time.sleep(2)

print(len(set(up_urls)))

with open('D:\File\实习\CVTE\cvte_py\\bilibili\\up_homePages.txt', 'w', encoding='utf-8') as f:
    for item in up_urls:
        f.write(str(item) + '\n')
