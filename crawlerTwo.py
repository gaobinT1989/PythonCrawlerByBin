import requests
import re
import json
from tqdm import tqdm
import shutil
from urllib.parse import urlparse

def get_page_title(url):
    response = requests.get(url)
    if response.status_code == 200:
        match = re.search(r'<title>(.*?)</title>', response.text)
        if match:
            return match.group(1)
    return "video"
def download_m3u8_video(url):
        response = requests.get(url)
        html = response.text
        pattern = r'([^"]+index\.m3u8)'
        match = re.search(pattern, html)
        decoded_url = json.loads('"' + match.group(1) + '"')
        m3u8_response = requests.get(decoded_url)
        m3u8_data = m3u8_response.text
        match = re.search(r".*\.m3u8.*", m3u8_data)
        if match:#多层m3u8
         lines = m3u8_data.split("\n")
         s=lines[2]
         decoded_url=decoded_url.replace("index.m3u8",s)
         print("第二层链接：",decoded_url)
         m3u8_response = requests.get(decoded_url)
         m3u8_data = m3u8_response.text
        segments = [line.strip() for line in m3u8_data.split('\n') if line.endswith('.ts')]
        output_file = get_page_title(url) + '.mp4'
        print("电影名：",output_file)
        print("电影下载链接：",decoded_url)
        print("开始下载...")
        print("__________________________")
        with open(output_file, 'wb') as f:
            for segment in tqdm(segments):
                segment_url = decoded_url.rsplit('/', 1)[0] + '/' + segment
                segment_response = requests.get(segment_url, stream=True)
                segment_response.raw.decode_content = True
                shutil.copyfileobj(segment_response.raw, f)
        print("视频下载完成，保存为：" + output_file)

#电影播放链接
url = 'https://www.pian-ku.com/vodplay/145660-1-1/'
download_m3u8_video(url)