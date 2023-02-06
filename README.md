# nkwspider
牛客网面经爬虫


可以爬取想要的不同领域的面经
安装bs4和requests库即可


1.输入想要爬取的面经组数（一组为30个）
2.打开想要查看的面经领域，如下图：要看Java的面经汇总，查看网址上面的targetID
<img width="1439" alt="截屏2022-03-17 11 24 23" src="https://user-images.githubusercontent.com/79900533/158730659-8980c19f-bdd6-4dc7-bdf9-b6174fb97ebc.png">
然后输入到控制台即可


# 更新于2023-02-06
由于网页结构改变，在一位朋友的提醒下更新了代码
操作步骤也随之改变:
###1.输入要爬取的jobId，获取方法如下：
    -打开如下网址：https://www.nowcoder.com/interview/center?entranceType=%E5%AF%BC%E8%88%AA%E6%A0%8F
    -打开开发者模式，点击网络，然后选择Fetch/XHR
    -在网页下面面试经验部分选择你要爬取的面经领域，然后找到一条list开头的请求，点进去查看载荷，找到jobId输入程序即可
###2.输入爬取的面经组数（一组20个）
###3.等待结果输出
tips：由于网页架构升级，使用同一ip爬取可能会被短暂封ip，若想获得高效服务可以参考如下git代码搭建代理使用
    https://github.com/jhao104/proxy_pool
