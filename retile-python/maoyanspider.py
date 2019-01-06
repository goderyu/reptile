# Author: goderyu
import requests
import re
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        # 添加配置头
        # Windows NT 6.1;WOW64
        # Mozilla/5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36
        headers = {
            'Users-Agent':'Mozilla/5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }
        response = requests.get(url, headers)
        if response.status_code == 200:
            return response.text
        return none
    except RequestException:
        return none

def get_this_page(html):
    # 正则这里，如果只写<dd>.*</dd>，它并不是匹配到第一个遇见的</dd>就停，而是查找字符串直到最后一个</dd>
    # 成功！
    # 为什么要这么写正则：以正向思维来说，在固有的匹配字符之间有一些不确定的字符，
    # 那么常识会想到任意字符任意位数，会使用.*，这种是属于贪婪匹配，也就是说有可能
    # 会覆盖掉之后的匹配，改成非贪婪，就是加一个?相当于任意字符任意位数，但是我只做一次.
    # 试过了组中组，也试过了把所有.*括起来再加上?:不作为组（即(?:.*)），逻辑上其实就和.*是一回事
    # 基本上设计正则的思路就是先宏观逻辑上从自然语言到机器语言的顺序尽可能逻辑性强，思维缜密的多加一些正则限定
    # 写出字符匹配的流程，接着再从内到外的仔细区分出细微差别后进行逻辑修正
    # 再通过反复的调试，去除一些类似于负负得正的多余代码，即可顺利实现正确并且简洁的正则语句
    pattern = re.compile('class="board-index.*?">(\d+)</i>.*?<a'
                         '.*?data-src="(.*?)" alt.*?name">.*?">(.*?)</a></p>'
                         '.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         '.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>', re.S)
    # 这里元组中没有按照预期给出10个结果，总是只有最后一个，猜测是迭代哪里出现了逻辑问题，主要还是要分析正则表达式，但是正则表达式能够正确显示最后一个说明基本逻辑没有问题
    # 已经有了近一步发展，分析正则规范后，发现原因可能是因为.*自以为是匹配任意字符任意多次，但是*的定义是匹配之前的表达式0次或多次，如果不带括号，应该是会一直匹配到第一个再来一次直到最后一次，那么之前9次的结果就被覆盖掉了，属于思维逻辑正确但是和代码的执行逻辑有出入造成的
    items = pattern.findall(html)
    for item in items:
        yield{
            '电影排名': item[0],
            '封面图': item[1],
            '电影名': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5]+item[6]
        }
    return items

def main():
    url = "https://maoyan.com/board/4?"
    html = get_one_page(url)
    for item in get_this_page(html):
        print(item)

if __name__ == '__main__':
    main()