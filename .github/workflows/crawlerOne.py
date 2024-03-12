#crawl anything by search keywords
import os
import requests
from bs4 import BeautifulSoup

def save_images_by_keyword(keyword, page_num):
    base_url = "https://www.toopic.cn/index.php/index_index_soso"
    num=0
    for i in range(1,page_num+1):
      params = {'kw': keyword,'page': i}
      response = requests.get(base_url, params=params)
      directory_name = f"{keyword}"
      os.makedirs(directory_name, exist_ok=True)
      soup = BeautifulSoup(response.content, 'html.parser')
      img_tags = soup.find_all('img')
      img_sources = [img['src'] for img in img_tags]
      for idx, src in enumerate(img_sources):
        img_response = requests.get("https://www.toopic.cn/"+src)
        if img_response.status_code == 200:
            num=num+1
            with open(f"{directory_name}/{keyword}{num}.jpg", 'wb') as f:
                f.write(img_response.content)
                print("第",num,"张已下载")
#搜索
save_images_by_keyword("武侠", 2)#20页