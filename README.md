# Multimodal TTP Project

## 爬虫代码
1. 获取up的主页（2024全部百大up）：
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/video_author_details/catch_up_homePage.py'>catch_up_homePage.py</a>

2. 获取视频bv号（2024所有百大up，该年度的全部视频）：
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/video_author_details/collect_up_bv.py'>collect_up_bv.py</a>

3. 构建bilibili-多模态TTP数据集：
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/collect_blbl_ttp_data.py'>collect_blbl_ttp_data.py</a>

## Note
1. 直接运行第三步的代码即可：
<a href='/Dataset3/jy_data/Github/MM-TTP/Dataset-Construction/collect_blbl_ttp_data.py'>collect_blbl_ttp_data.py</a>

2. 需要提前下载对应Chrome版本的 chromedriver.exe，存放路径： MM-TTP/Dataset-Construction/chromedriver.exe

    下载链接：
    
    1）ChromeDriver官方仓库：https://chromedriver.storage.googleapis.com/index.html

    2）新版Chrome for Testing（适用于Chrome 114+）：https://googlechromelabs.github.io/chrome-for-testing/

