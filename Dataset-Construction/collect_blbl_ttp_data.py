import os
from tqdm import tqdm
import re
import cv2
import requests
import json
from lxml import etree

from bs4 import BeautifulSoup
from pyecharts.charts import Line

header = {
    "referer": "https://www.bilibili.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
}
 
# 提取视频和音频的播放地址
def get_play_url(url):
    r = requests.get(url, headers=header)
    # print(r.text)
    info = re.findall('window.__playinfo__=(.*?)</script>', r.text)[0]
    # print(info)
    video_url = json.loads(info)["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = json.loads(info)["data"]["dash"]["audio"][0]["baseUrl"]
    
    info2 = re.findall('window.__INITIAL_STATE__=(.*?)</script>', r.text)[0]
    match = re.search(r'"cidMap":\{.*?"cids":\{.*?"(\d+)":(\d+)\}.*?\}', info2)
    if match:
        cid_key = match.group(1)
        cid_value = match.group(2)
        cid = cid_value
        print(f"Found cid key: {cid_key}, cid value: {cid_value}")
        danmaku_url = f"https://comment.bilibili.com/{cid}.xml"
    else:
        print("######## No [cid] found ###########")

    html = etree.HTML(r.text)
    filename = html.xpath('//h1/text()')[0]
    return video_url, audio_url, danmaku_url, filename
 
# 下载并保存视频和音频
def download_files(video_url, audio_url, filename, video_path,audio_path):
    video_content = requests.get(video_url, headers=header).content
    audio_content = requests.get(audio_url, headers=header).content
    
    with open(f'{video_path}/{filename}.mp4', 'wb') as f:
        f.write(video_content)
        
    # with open(f'{audio_path}/{filename}.mp3', 'wb') as f:
    #     f.write(audio_content)
 
 
# 合并视频和音频,使用ffmpeg模块
def combin_video_audio(filename, video_path, audio_path):
    cmd = fr"ffmpeg -i {video_path}/{filename}.mp4 -i {audio_path}/{filename}.mp3 -c:v copy -c:a aac -strict experimental -map 0:v -map 1:a {video_path}/output-{filename}.mp4"
    os.system(cmd)
    print("音频视频合并完毕")
    print("--"*10)

    os.remove(f'{video_path}/{filename}.mp4')
    os.remove(f'{audio_path}/{filename}.mp3')
    print('已删除多余的文件')
    
def danmaku_frame_to_image(video_path, second, output_image_path):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频文件")
        return
    
    # 获取视频的帧率 (fps)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # print(f"视频帧率：{fps} FPS")

    # 计算目标帧的位置
    frame_number = int(fps * second)

    # 设置视频读取的位置到目标帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # 读取指定帧
    ret, frame = cap.read()

    if ret:
        # 保存该帧为图像
        cv2.imwrite(output_image_path, frame)
        # print(f"帧图像已保存为 {output_image_path}")
    else:
        # 无法读取，找下一秒的帧
        frame_number = int(fps * (second+1))
        # 设置视频读取的位置到目标帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        # 读取指定帧
        ret2, frame2 = cap.read()
        if ret2:
            # 保存该帧为图像
            cv2.imwrite(output_image_path, frame2)
            # print(f"帧图像已保存为 {output_image_path}")
        else:
            # 仍然无法读取，跳过
            print("无法读取指定帧")

    # 释放视频捕获对象
    cap.release()
    
def get_danmaku(danmaku_url, danmaku_save_path, video_path, frame_image_folder, filename):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    
    response = requests.get(danmaku_url, headers=headers)
    response.encoding = response.apparent_encoding
    xml = response.text
    soup = BeautifulSoup(xml,"lxml")
    
    content_all = soup.find_all(name = "d")
    
    timeList = []
    result_save = []
    for content in tqdm(content_all):
    
        data = content.attrs["p"]
    
        time = data.split(",")[0]
        int_time = int(float(time)) # 秒数向下取整
        
        # 秒数0.0~0.5，向下取整
        # 秒数0.5~1.0，向上取整
        if float(time) - int_time  > 0.5:
            int_time += 1
        
        # 将time转换成浮点数，添加进列表timeList中
        timeList.append(float(time))
        
        #######################################
        #### 捕获当前弹幕对应的这一秒的视频帧画面
        #######################################
        image_path = f'{frame_image_folder}/frame_{int_time}.jpg'
        danmaku_frame_to_image(video_path, int_time, image_path)

        text = content.get_text()
        result_save.append(
            {
                "time": float(time), 
                "int_time": int_time,
                "text": text,
                "image_path": image_path
            }
        )

    # 按时间排序
    result_save = sorted(result_save, key=lambda x: float(x["time"]))

    subtitlesDict = {}
    for x in range(22):
        start = 60*x+1
        end = 60*(x+1)
        segment_range = f"{start}-{end}"
        subtitlesDict[segment_range] = 0
    
    for subtitle in subtitlesDict.keys():
        start_key = subtitle.split("-")[0]
        end_key = subtitle.split("-")[1]
        for item in timeList:
            if int(start_key)<= item <= int(end_key):
                subtitlesDict[subtitle] = subtitlesDict[subtitle] + 1
    
    line = Line()
    
    # 使用list()将字典subtitlesDict所有键转换成列表，传入add_xaxis()中
    line.add_xaxis(list(subtitlesDict.keys()))
    # 使用add_yaxis()函数，将数据统称设置为"弹幕数"
    # 将字典subtitlesDict所有值转换成列表，作为参数添加进函数中
    line.add_yaxis("弹幕数", list(subtitlesDict.values()))
    
    # 使用render()函数存储文件，设置文件名为弹幕统计.html
    line.render(f"{danmaku_save_path}/analyze/弹幕统计_{filename}.html")
    
    danmaku_result = f'{danmaku_save_path}/danmaku/result_{filename}.json'
    with open(danmaku_result, 'w', encoding='utf-8') as f:
        json.dump(result_save, f, ensure_ascii=False, indent=2)
    # print(f"共爬取弹幕数量: {len(result_save)}")
 
# 将字符串中的非法字符替换成下划线，以防写文件时文件名非法
def clean_name(name):
    return re.sub(r'[\\/:*?"<>|\[\]]+', '_', name)

 
if __name__ == '__main__':
    video_save_path = r'MM-TTP/Data-Save/video'
    audio_save_path = r'MM-TTP/Data-Save/audio'
    danmaku_save_path = r'MM-TTP/Data-Save'
    
    error_videos = []
    
    directory_path = 'MM-TTP/Dataset-Construction/video_author_details/up_2024百大_2024视频bv号'
    
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    print(f"总共有 {len(json_files)} 个UP主")


    # 读取每个up
    up_num = 0
    for json_file in json_files:

        up_num += 1
        file_path = os.path.join(directory_path, json_file)
        up_name = json_file.replace('_bv号.json', '')
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        url_list = [d['url'] for d in data]
        
        count = len(url_list)
        print(f'当前up主共有: {count} 条视频')
        

        # 读取一个up的每一条视频的url
        video_num = 0
        for url in url_list:
            video_num += 1
            print(f'————正在处理第 {up_num} 个up主: {up_name} --第 {video_num} 个视频————')
            try:
                video_url, audio_url, danmaku_url, filename = get_play_url(url)
                filename = clean_name(filename)
            except:
                # 付费视频，跳过 & 记录该条
                error_videos.append(url)
                print(f'————已跳过：第 {up_num} 个up主 {up_name} --第 {video_num} 个视频————')
                continue
            
            # 下载视频音频
            download_files(video_url, audio_url, filename, video_save_path, audio_save_path)
            
            ## 合并视频音频
            # combin_video_audio(filename, video_save_path, audio_save_path)
            
            video_path = f'{video_save_path}/{filename}.mp4'  # 视频文件路径
            
            frame_image_folder = f'MM-TTP/Data-Save/image/{filename}'
            os.makedirs(frame_image_folder, exist_ok=True)
            get_danmaku(danmaku_url, danmaku_save_path, video_path, frame_image_folder, filename)
            
            
            # 删除视频文件
            if os.path.exists(video_path):  # 确保文件存在
                os.remove(video_path)  # 删除视频文件
                # print(f"视频文件已删除")
            else:
                print(f"视频文件不存在，无法删除")
            
            
            print(f'————已完成：第 {up_num} 个up主 {up_name} --第 {video_num} / {count} 个视频————')