# Multimodal TPP Project

[中文版](README_cn.md)

## Web Scraping Code
1. Get Uploader's Homepage (All 2024 Top 100 Uploaders):
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/video_author_details/catch_up_homePage.py'>catch_up_homePage.py</a>

2. Get Video BV Numbers (All videos from 2024 Top 100 Uploaders):
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/video_author_details/collect_up_bv.py'>collect_up_bv.py</a>

3. Build Bilibili Multimodal TTP Dataset:
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/collect_blbl_ttp_data.py'>collect_blbl_ttp_data.py</a>

## Note
1. You can directly run the code in step 3:
<a href='https://github.com/FRENKIE-CHIANG/Multimodal-TTP/blob/main/Dataset-Construction/collect_blbl_ttp_data.py'>collect_blbl_ttp_data.py</a>

2. It's recommended to set up the directory structure beforehand. Create a Data-Save folder with the following format:
3. The BILI-TPP dataset constructed in this project:
   https://huggingface.co/datasets/FRENKIE-CHIANG/BILI-TPP

## Citation
If you find this dataset helpful in your research, please consider citing:
```bibtex
@misc{BILI-TPP,
  author = {Yue Jiang and Quyu Kong and Feng Zhou},
  title = {Multimodal-TPP: A Multimodal Temporal Point Process Dataset},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/FRENKIE-CHIANG/Multimodal-TPP}
}
```
