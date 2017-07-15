# 爬取百度海量图片
## 一、 准备环境
1. windows/Linux 机器一台（4GB/8GB内存都ok）
2. python2.7及相关的lib：urllib、itertools、requests等

## 二、原理说明
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们要抓取网页上的图片，其实就相当于是找到网页上图片对应的url，通过url下载相应的图片到本地。而此过程，我们可以分解为以下几个步骤：  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    1.  分析网页结构  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    2.  生成url列表  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    3.  发送http请求获取json数据  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    4.  根据json数据得到图片url  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    5.  请求url下载图片  
因此，第一步，我们先要了解百度图片搜索网页的结构。  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;一般，百度的图片链接有以下四种：  
>"thumbURL":  "http://img1.imgtn.bdimg.com/it/u=757023778,2840825931&fm=21&gp=0.jpg"  
"middleURL":  "http://img1.imgtn.bdimg.com/it/u=757023778,2840825931&fm=21&gp=0.jpg"  
"hoverURL":  "http://img1.imgtn.bdimg.com/it/u=757023778,2840825931&fm=23&gp=0.jpg"  
"objURL":  "http://imgsrc.baidu.com/forum/w=580/sign=b3bcc2f88a5494ee87220f111df4e0e1/78fed309b3de9c82913abac86a81800a18d84344.jpg"  

------
测试后发现前三种都是403 Forbidden，只有最后一种可以打开，因此，我们爬取的对象也是最后一种链接的图片。  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;另外，每次请求搜索url的时候，我们得到的并不是常规的http开头的数据报文，百度的是objURL开头的，参考了其他大神的方法，这里使用字符表进行解码的方法：  
```python
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
```  
## 三、代码  
（见criber.py，注释很详细）
## 四、注意事项
1. 本代码是单线程下的爬虫，效率比较慢
2. 由于目前各大网站都有反爬虫机制，执行程序一段时间后（或反复执行多次后）ip会被禁止访问百度网页，一般要么换个网址访问（不过由于网页结构不同，可能代码需要有所改动）；要么等一段时间再访问。
