# Multimodal TPP Project

## 爬虫代码
1. 获取up的主页（2024全部百大up）：
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/video_author_details/catch_up_homePage.py'>catch_up_homePage.py</a>

2. 获取视频bv号（2024所有百大up，该年度的全部视频）：
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/video_author_details/collect_up_bv.py'>collect_up_bv.py</a>

3. 构建bilibili-多模态TTP数据集：
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/collect_blbl_ttp_data.py'>collect_blbl_ttp_data.py</a>

## Note
1. 直接运行第三步的代码即可：
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/collect_blbl_ttp_data.py'>collect_blbl_ttp_data.py</a>

2. 建议提前构建文件目录组织，创建Data-Save文件夹，格式如下：
   ```
    Multimodal-TPP/
    ├── Dataset-Construction/
    ├── Data-Save/
    │   ├── image/
    │   ├── danmaku/
    │   ├── analyze/
    │   ├── video/
    │   └── audio/
    └── ...
    ```

3. 本项目构建的 BILI-TPP 数据集：
https://huggingface.co/datasets/FRENKIE-CHIANG/BILI-TPP
    
