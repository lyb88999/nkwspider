# -*- coding = UTF-8 #-*-
# @Time : 2022/3/12 11:57 下午
# @Author : 李宇博
# @File : test.py
# @SoftWare : PyCharm

import re
import os

import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def getHtml2(url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    headers = {'User-Agent': str(UserAgent().random)}
    while retry_count > 0:
        try:
            # 使用代理访问
            # print(proxy)
            # html = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            html = requests.get(url, headers=headers)
            return html
        except Exception:
            retry_count -= 1
            # 删除代理池中代理
            delete_proxy(proxy)
    return None


def getNum():
    sum = int(input("请输入你要爬取的面经组数(30个为一组):\n"))
    tagID = int(input("请输入你要爬取的领域代号:\n"))
    for i in range(1, sum + 1):
        r = requests.get("https://www.nowcoder.com/discuss/experience/json?token=&tagId=" + str(
            tagID) + "&companyId=0&phaseId=0&order=3&query=&page=" + str(i))
        content = json.dumps(r.json(), indent=4, ensure_ascii=False)
        content = json.loads(content)
        with open("num2.txt", "a") as f:
            for i in range(30):
                f.write(str(content['data']['discussPosts'][i]['postId']) + "\n")
    print("获取代号完毕")
    return tagID


def getHtml():
    cnt = 1
    result = ""
    with open("num2.txt", "r") as f:
        content = f.read().splitlines()
    for i in content:
        url = "https://www.nowcoder.com/discuss/" + str(i)
        print(cnt, url)
        r = getHtml2(url)
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
    print("内容爬取完毕，已写入final.txt文件")


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
        os.remove("num2.txt")
    except:
        print("出现异常")


if __name__ == '__main__':
    id = getNum()
    getHtml()
    clearBlankLine(id)
    formatting()
