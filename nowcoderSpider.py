# -*- coding = UTF-8 #-*-
# @Time : 2023/2/6 13:25
# @Author : 李宇博
# @File : nowcoderSpider.py
# @SoftWare : PyCharm
import json
import os
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def getJson(page, jobId):
    headers = {
        'authority': 'gw-c.nowcoder.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.nowcoder.com',
        'referer': 'https://www.nowcoder.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'companyList': [],
        'jobId': jobId,
        'level': 3,
        'order': 3,
        'page': page,
        'isNewJob': True,
    }

    response = requests.post(
        'https://gw-c.nowcoder.com/api/sparta/job-experience/experience/job/list',
        headers=headers,
        json=json_data,
    )
    content = json.dumps(response.json(), indent=4, ensure_ascii=False)
    content = json.loads(content)
    return content


# 获取代号
def getId():
    jobId = int(input("请输入你要爬取的jobId:\n"))
    # 获取返回内容
    content = getJson(1, jobId)
    # print("共有{}条记录".format(content['data']['total']))
    groupNum = int(input("请输入你要爬取的面经组数(20个为一组):\n"))
    for i in range(1, groupNum + 1):
        res = getJson(i, jobId)
        with open('textId.txt', 'a') as f:
            for i in range(20):
                try:
                    f.write(str(res['data']['records'][i]['contentData']['entityId']) + "\n")
                except KeyError:
                    f.write(str(res['data']['records'][i]['momentData']['id']) + "\n")
                except IndexError:
                    print("没有这么多面经，请重试！")
                    os.remove('textId.txt')
                    exit(0)
    print("获取文章代号完毕，已写入textId.txt")
    return jobId


def getContent():
    sigNum = 0
    cnt = 1
    result = ""
    with open("textId.txt", "r") as f:
        content = f.read().splitlines()
    for i in content:
        url = "https://www.nowcoder.com/discuss/" + str(i)
        print(cnt, url)
        r = getHtml(url)
        title = re.findall('<title>(.*?)</title>', r.text)[0].replace("_笔经面经_牛客网", '')
        # time = re.findall('<span class ="time-text" data-v-bb417982="" >(.*?)</span>', r.text, re.S)[0].replace("\n", "").replace("  ", "")
        try:
            bs = BeautifulSoup(r.text, 'html.parser')
            res = bs.find_all(name='span', attrs={'class': 'time-text'})
            bs2 = BeautifulSoup(str(res[0]), 'html.parser')
            time = bs2.get_text()
            bs = BeautifulSoup(r.text, 'html.parser')
            res = bs.find_all(name='div', attrs={'class': 'nc-slate-editor-content'})
            bs2 = BeautifulSoup(str(res[0]), 'html.parser')
            content = bs2.get_text()
            print('类型1')
            sigNum = sigNum + 1
        except IndexError:
            try:
                print('类型2')
                bs = BeautifulSoup(r.text, 'html.parser')
                res = bs.find_all(name='span', attrs={'class': 'time-text'})
                bs2 = BeautifulSoup(str(res[0]), 'html.parser')
                time = bs2.get_text()
                bs = BeautifulSoup(r.text, 'html.parser')
                res = bs.find_all(name='div', attrs={'class': 'nc-post-content'})
                bs2 = BeautifulSoup(str(res[0]), 'html.parser')
                content = bs2.get_text()
                sigNum = sigNum + 1
            except IndexError:
                print('IP被封')
                time = "无"
                title = "IP被封，未获取到，请重试"
                content = "IP被封，未获取到，请重试"
        result += content
        with open("final.txt", "a") as f:
            f.write("第" + str(cnt) + "篇面经" + "\n" + "链接:" + str(url) + "\n" + "标题:" + str(title) + "\n" + "时间:" + str(
                time) + "\n" + "内容:" + str(result) + "liyubo")
        # print("链接:" + url, "标题:" + title, "时间:" + time, sep="\t")
        cnt = cnt + 1
        result = ""
    print("内容爬取完毕，共有{}条有效数据，已写入final.txt文件".format(sigNum))


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def getHtml(url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    headers = {'User-Agent': str(UserAgent().random)}
    while retry_count > 0:
        try:
            # 使用代理访问
            # print(proxy)
            # 代理搭建好后可使用这个
            # html = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            # 没搭建好代理用这个
            html = requests.get(url, headers=headers)
            return html
        except Exception:
            retry_count -= 1
            # 删除代理池中代理
            delete_proxy(proxy)
    return None


def clearBlankLine(id):
    file1 = open('final.txt', 'r', encoding='utf-8')  # 要去掉空行的文件
    file2 = open(str(id) + ".txt", 'w', encoding='utf-8')  # 生成没有空行的文件
    try:
        for line in file1.readlines():
            if line == '\n':
                line = line.strip("\n")
            elif line.__contains__("liyubo"):
                line = line.replace("liyubo", "\n\n\n\n")
            file2.write(line)
    finally:
        file1.close()
        file2.close()
        print("空行去除完毕，完成！")


def formatting():
    try:
        os.remove("final.txt")
        os.remove("textId.txt")
    except:
        print("出现异常")


if __name__ == '__main__':
    # 获取文章代号
    jobId = getId()
    # 获取内容并写入文件
    getContent()
    # 格式化处理
    clearBlankLine(jobId)
    formatting()
