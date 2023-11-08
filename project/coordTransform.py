# -*- coding: utf-8 -*-

import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta) + 0.0002
    gg_lat = z * math.sin(theta) + 0.0047
    return [gg_lng, gg_lat]


# 转化所有的gps坐标
def coord_transform():
    with open('data_use/link_gps.v2', 'r') as infile:
        with open('data_use/link_gps_transformed.v2', 'w') as outfile:
            for line in infile:
                parts = line.strip().split('\t')

                if len(parts) >= 3:
                    link_id = parts[0]
                    longitude = float(parts[1])
                    latitude = float(parts[2])

                    # 调用 bd_to_gcj02 函数进行坐标转换
                    ret = bd09_to_gcj02(longitude, latitude)
                    lon = ret[0]
                    lat = ret[1]

                    outfile.write(f"{link_id}\t{lon}\t{lat}\n")


if __name__ == "__main__":
    coord_transform()
