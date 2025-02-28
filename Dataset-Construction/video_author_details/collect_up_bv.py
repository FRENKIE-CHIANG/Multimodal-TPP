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

# 获取百大up的主页
up_urls_path = 'MM-TTP/Dataset-Construction/video_author_details/up_homePages.txt'
with open(up_urls_path, "r", encoding="utf-8") as file:
    lines = file.readlines()
up_urls = [line.strip() for line in lines]


chromedriver_path = "MM-TTP/Dataset-Construction/chromedriver.exe"
service = Service(chromedriver_path)
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()  # 使窗口最大化

i = 0
for url in up_urls:
    i += 1
    data_save = []

    url = url + '/upload/video'

    browser.get('https://notegpt.io/workspace/create')
    # 等待页面加载（可以根据需要调整）
    # time.sleep(7000)
    try:
        # 找到账号输入框并输入账号
        username_input = browser.find_element(By.XPATH, "//input[@placeholder='请输入账号']")
        username_input.send_keys('####【替换为b站账号】####')
        # 找到密码输入框并输入密码
        password_input = browser.find_element(By.XPATH, "//input[@placeholder='请输入密码']")
        password_input.send_keys('####【替换为b站密码】####')
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
    # time.sleep(4000)

    up_name = browser.find_element(By.CLASS_NAME, 'h-user').find_element(By.CLASS_NAME, 'h-basic').find_element(By.ID, 'h-name').text
    print(f"正在爬取第 {i} 个up主: {up_name}")
    data_save = []
    page = 0
    video_sum = 0

    flag_2024 = True # 判断爬取的视频是否是2024年的

    while True:
        page += 1

        video_box = browser.find_element(By.CLASS_NAME, 'main-content').find_element(By.ID,'submit-video').find_element(By.CSS_SELECTOR, '.clearfix.cube-list')
        video_list = video_box.find_elements(By.TAG_NAME, 'li')
        time.sleep(2)

        bv_list = []
        count = 0

        # 当前一页
        for video in video_list:
            bv = video.get_attribute("data-aid")
            creat_time = video.find_element(By.CLASS_NAME, 'meta').find_element(By.CLASS_NAME, 'time').text
            creat_time = creat_time.strip()

            #### 【判断逻辑】只爬取2024的视频
            if "2023" in creat_time:
                flag_2024 = False
                break
            elif "2024" not in creat_time:
                continue
            ############################

            if bv is None or bv in bv_list:
                continue
            bv_list.append(bv)
            # print(f'BV: {bv}, time:{creat_time}')
            # print("1: ", bv)
            link = video.find_element(By.TAG_NAME, 'a').get_attribute("href")
            # print("2: ", link)
            title = video.find_element(By.CLASS_NAME, 'title').text
            title = clean_name(title)
            # print("3: ", title)
            d = {
                    "bv": bv,
                    "title": title,
                    "url": link,
                    "creat_time": creat_time
                }
            data_save.append(d)
            count += 1
            video_sum += 1
            print(f"已爬取第 {page} 页，第 {count} 个视频: {bv}, 总计共: {video_sum} 个视频")

        # 如果2024的视频已经爬完，退出
        if not flag_2024:
            print("2024视频爬取完毕")
            break

        next_box = browser.find_element(By.CLASS_NAME, 'main-content').find_element(By.ID, 'submit-video').find_element(By.CLASS_NAME, 'be-pager')
        next_page_button = next_box.find_element(By.CLASS_NAME, "be-pager-next")

        # 判断按钮是否禁用，检查是否包含 'be-pager-disabled' 类
        if 'be-pager-disabled' in next_page_button.get_attribute("class"):
            print("所有页面爬取完毕")
            break

        else:
            time.sleep(0.5)
            # 如果有下一页，点击下一页按钮
            next_page_button.click()
            print("正在加载下一页...")
            time.sleep(2)

    time.sleep(1.5)
    save_path = f'MM-TTP/Dataset-Construction/video_author_details/up_2024百大_2024视频bv号\{up_name}_bv号.json'
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data_save, f, ensure_ascii=False, indent=2)
    time.sleep(1)
    # browser.close()

