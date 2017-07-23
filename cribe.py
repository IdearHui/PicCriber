# coding=utf-8
import urllib
import itertools
import requests
import os
import re
import sys


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

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_tables = {ord(key): ord(value) for key, value in char_table.items()}


def decode(u):
    """
    解码图片URL
    :param u:
    :return:
    """
    # 先替换字符串
    for key, value in str_table.items():
        u = u.replace(key, value)
    # 再替换剩下的字符
    return u.translate(char_tables)


def get_urls(key_word):
    """
    生成网址列表
    :param key_word:
    :return:
    """
    key = urllib.quote(key_word)   # 解析关键字
    # 根据百度网址模板，填入关键字生成搜索url
    result_url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={key}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={key}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls_list = (result_url.format(key=key, pn=x) for x in itertools.count(start=0, step=60))
    return urls_list


def parse_to_get_url():
    """
    解析JSON获取图片URL
    :return:
    """
    return re.compile(r'"objURL":"(.*?)"')


def get_img_url(html_code):
    """
    根据html提取图片地址
    :param html_code:
    :return:
    """
    re_url = parse_to_get_url()
    image_urls = [decode(x) for x in re_url.findall(html_code)]
    return image_urls


def download_img(img, dir_path, img_name):
    """
    下载图片
    :param img:
    :param dir_path:
    :param img_name:
    :return:
    """
    filename = os.path.join(dir_path, img_name)
    try:
        res = requests.get(img, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":", img)
            return False
    except Exception as e:
        print("抛出异常：", img)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mk_dir(file_path):
    """
    生成本地图片目录
    :param file_path:
    :return:
    """
    fp = os.path.join(sys.path[0], file_path)
    if not os.path.exists(fp):
        os.mkdir(fp)
    return fp


def init():
    """
    请求url、下载图片
    :return:
    """
    index = 0
    for url in urls:
        print("正在请求：", url)
        # 解析页面编码
        html = requests.get(url, timeout=10).content.decode('utf-8')
        img_urls = get_img_url(html)     # 根据页面html获得图片地址
        if len(img_urls) == 0:  # 没有图片则结束
            break
        for img_url in img_urls:
            if download_img(img_url, picture_path, str(index) + ".jpg"):
                index += 1
                print("已下载 %s 张" % index)

if __name__ == '__main__':
    word = raw_input("请输入你要下载的图片关键词：\n")
    picture_path = mk_dir("pic")      # 生成存放图片的目录
    urls = get_urls(word)   # 根据关键字生成搜索的url列表
    init()  # 启动下载图片
