# Author: goderyu
from lxml import etree
import requests
import xlwt

# 定义一个全局范围空的二维列表，等待get_all_page函数获取数据为其赋值，再在main函数中输出到excel表
cinemas_info = [[] for i in range(2)]


# 爬取猫眼电影网站影院列表中的单页数据
def get_this_page(url):
    html = requests.get(url).text  # 这里一般先打印一下 html 内容，看看是否有内容再继续。
    # print(html)
    s = etree.HTML(html)  # 将源码转化为能被 XPath 匹配的格式
    cinema_name = s.xpath('//body/div[3]/div[2]/div/div[1]/a/text()')  # 返回为一列表
    cinema_addr = s.xpath('//body/div[3]/div[2]/div/div[1]/p/text()')
    for i in range(len(cinema_addr)):
        cinema_addr[i] = cinema_addr[i][3:]
    cinemas_info[0].extend(cinema_name)
    cinemas_info[1].extend(cinema_addr)


# 遍历获取多页的url
def get_all_page():
    # 该网页首页和其余多页的url格式不一致，不能放在循环中，不然会导致第一遍爬取是空
    index_url = 'https://maoyan.com/cinemas'
    get_this_page(index_url)
    for i in range(12, 108, 12):
        url = 'https://maoyan.com/cinemas?offset={}'.format(i)
        # 调用单页爬虫函数，为其循环赋值url
        get_this_page(url)


def main():
    # 创建一个excel文件
    cinema_xls = xlwt.Workbook()
    # 在excel文件中创建一张表
    sheet1 = cinema_xls.add_sheet(u'cinemas_info', cell_overwrite_ok=True)
    # 爬取数据
    get_all_page()
    # 为excel表写入表头
    sheet1.write(0, 0, '序号')
    sheet1.write(0, 1, '影院名称')
    sheet1.write(0, 2, '影院地址')
    # 获取二维列表的行数，对应excel表的列数
    for i in range(len(cinemas_info)):
        # 获取二维列表的列数，对应excel表的行数
        for j in range(len(cinemas_info[i])):
            # 在excel表的第一列每一行写入序号
            sheet1.write(j + 1, 0, j + 1)
            # 在excel表的之后每列每行写入其余信息
            sheet1.write(j + 1, i + 1, cinemas_info[i][j])
    # 将自动写入完成的excel表进行保存
    cinema_xls.save('cinemas_info.xls')


if __name__ == '__main__':
    main()

'''
总结：
    使用xlwt包调用写入excel表的函数；
    使用etree将网页信息转换成xpath可以识别的格式；
    使用xpath的正则表达式规则来匹配想要的标签内的信息并获取信息返回成一个列表；
'''

