# -*- coding:utf-8 -*-  
import httplib2;
import json;
from urllib.parse import urlencode;
import time;
import matplotlib.pyplot;
import matplotlib.finance;
from matplotlib.pylab import date2num;
import datetime;

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
    data = kline('btc_cny', '1week');
    n = len(data);

    for i in range(0, n):
        data[i][0] = date2num(datetime.datetime.fromtimestamp(data[i][0] / 1000));
        if i >= 9 + 4:
            #买入结构，连续9次收盘价都低于四天前的收盘价
            for j in range(0, 9):
                k = i - j;
                x = data[k];
                y = data[k - 4];
                if x[4] > y[4]:
                    break;
            if j == 8:
                print("Buy %s" % data[i][0]);

            #卖出结构，连续9次收盘价都高于四天前的收盘价
            for j in range(0, 9):
                k = i - j;
                x = data[k];
                y = data[k - 4];
                if x[4] < y[4]:
                    break;
            if j == 8:
                print("Sell %s" % data[i][0]);
    
    _, ax = matplotlib.pyplot.subplots();
    matplotlib.finance.candlestick_ohlc(ax, data);
    matplotlib.pyplot.show();
