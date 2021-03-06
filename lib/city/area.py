# coding=utf-8
# author: Zeng YueTian
# 获取各板块信息


import requests
from lxml import etree
from lib.city.district import *


def get_district_url(city, district):
    """
    拼接指定城市的区县url
    :param city:
    :param district:
    :return:
    """
    return "http://{0}.lianjia.com/xiaoqu/{1}".format(city, district)


def get_areas(city, district):
    """
    通过城市和区县名获得下级板块名
    :param city: 城市
    :param district: 区县
    :return: 区县列表
    """
    page = get_district_url(city, district)
    xpath = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    areas = list()
    try:
        response = requests.get(page)
        html = response.content
        root = etree.HTML(html)
        links = root.xpath(xpath)

        # 针对a标签的list进行处理
        for link in links:
            relative_link = link.attrib['href']
            # 去掉最后的"/"
            relative_link = relative_link[:-1]
            # 获取最后一节
            area = relative_link.split("/")[-1]
            # 去掉区县名,防止重复
            if area != district:
                chinese_area = link.text
                CHINESE_AREA_DICT[area] = chinese_area
                areas.append(area)
        return areas
    except Exception as e:
        print e


if __name__ == "__main__":
    print get_areas("sh", "pudongxinqu")

