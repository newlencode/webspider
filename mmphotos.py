import requests
from lxml import etree
import os
import time
from multiprocessing import Pool


def get_photos(url):
    time1 = time.time()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    response = requests.get(url,headers = headers)
    html = response.content.decode('gbk')
    content = etree.HTML(html)

    dir_names = content.xpath('/html/body/div[4]/dl//dd/a/img/@alt')
    first_photos = content.xpath('/html/body/div[4]/dl/dd/a/@href')[:20]
    for i in range(len(dir_names)):
        file_address = f'mmphotos/{dir_names[i]}'
        os.mkdir(file_address)
        response = requests.get(first_photos[i], headers=headers)
        html = response.content.decode('gbk')
        content = etree.HTML(html)
        img_name = content.xpath('/html/body/div[5]/div[2]/p[1]/a/img/@alt')[0]
        img = content.xpath('/html/body/div[5]/div[2]/p[1]/a/img/@src')[0]
        response2 = requests.get(img, headers=headers)
        with open(file_address + '/' + img_name + str(1) + '.jpg', 'wb') as f:
            f.write(response2.content)
        j = 2
        while True:
            try:
                url = first_photos[i][:-5] +f'_{j}.html'
                response = requests.get(url, headers=headers)
                html = response.content.decode('gbk')
                content = etree.HTML(html)
                img_name = content.xpath('/html/body/div[5]/div[2]/p[1]/a/img/@alt')[0]
                img = content.xpath('/html/body/div[5]/div[2]/p[1]/a/img/@src')[0]
                response2 = requests.get(img, headers=headers)
                with open(file_address+'/'+ img_name + str(j)+'.jpg','wb') as f:
                    f.write(response2.content)
                j += 1
            except:
                break
    time2 = time.time()
    print(f'当前任务耗时{time2-time1}')
if __name__ == '__main__':
    t_begin = time.time()
    dir = 'mmphotos'
    if not os.path.exists(dir):
        os.mkdir(dir)
    urls = [f'https://www.6emm.com/qingchun/index_{i}.html' for i in range(4, 9)]
    p = Pool(6)
    p.map(get_photos,urls)
    p.close()
    p.join()
    t_end = time.time()
    print(f'总共耗时{t_end-t_begin}秒')
