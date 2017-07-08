# -*- coding:utf-8 -*-  
import httplib2;
import json;
from urllib.parse import urlencode;
import time;

def kline(symbol, type):
    http = httplib2.Http();
    data = dict(symbol=symbol, type=type);
    r, c = http.request('https://www.okcoin.cn/api/v1/kline.do?' + urlencode(data));
    if r['status'] == '200':
        return json.loads(c);
    else:
        return [];

if __name__ == '__main__':
    #比特币日K线数据
    data = kline('btc_cny', '1day');
    n = len(data);
    for i in range(0, n):
        if i >= 9 + 4:
            #买入结构，连续9次收盘价都低于四天前的收盘价
            for j in range(0, 9):
                k = i - j;
                x = data[k];
                y = data[k - 4];
                if x[4] > y[4]:
                    break;
            if j == 8:
                print("Buy %s" % (time.strftime("%Y%m%d %H:%M:%S", time.gmtime(data[i][0] / 1000))));

            #卖出结构，连续9次收盘价都高于四天前的收盘价
            for j in range(0, 9):
                k = i - j;
                x = data[k];
                y = data[k - 4];
                if x[4] < y[4]:
                    break;
            if j == 8:
                print("Sell %s" % (time.strftime("%Y%m%d %H:%M:%S", time.gmtime(data[i][0] / 1000))));
