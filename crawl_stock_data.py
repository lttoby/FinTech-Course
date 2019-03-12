#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:14:44 2019

@author: Barry
"""

import json
import requests
import numpy as np
import pandas as pd
import time
import os


path = os.getcwd()


def get_stock_list(n):
    df = pd.read_csv(path + "/stock_code.csv")
    stock_list = list()
    for stock_code in df['stock_code'][0:n]:
        stock_list.append(stock_code[0:6])
    return stock_list


def get_Html(url):
    count_error = 0
    debug = False
    try:
        r = requests.get(url,
                         headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"})
        if debug:
            print("request get")
        r.close()
        if debug:
            print("request closed")
        r = r.content.decode("utf-8", "ignore")
    except requests.exceptions.ConnectionError:
        time.sleep(70)
        count_error += 1
        print("error count:%s" % count_error)
        r = requests.get(url,
                         headers = {"User-Agent" : "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"})
        r.close()
        r = r.content.decode("utf-8", "ignore")
    return r


def get_minute_data(stock_list, debug = True):

    time_start = time.time()
    df_data = pd.DataFrame()
    for stock_code in stock_list:

        print(stock_code)

        if debug:
            time_start_i = time.time()

        url = (
            'http://www.szse.cn/api/market/ssjjhq/getTimeData?random=0.21065077819046873&marketId=1&code={}'.format(
                stock_code))

        try:
            result = get_Html(url)

            json_data = json.loads(result)
            date = json_data['datetime'][0:10]
            to_df = list()
            for i in range(0,len(json_data['data']['picupdata'])):
                data_list = json_data['data']['picupdata'][i]
                to_df.append(data_list)
        except Exception:
            print(stock_code + "out of range")
            
        df_tmp = pd.DataFrame(to_df, columns=['time', 'price', 'average', 'change', 'chg_pct', 'turnover_shares', 'turnover_value'])
        df_tmp["stock_code"] = stock_code
        df_tmp["trade_date"] = date
        df_data = df_data.append(df_tmp)

        if debug:
            print("getting data time spent:%s" % (time.time() - time_start_i))

    if debug:
        print("total time spent:%s" % (time.time() - time_start))
    return df_data[['trade_date', 'stock_code', 'time', 'price', 'average', 'change', 'chg_pct', 'turnover_shares', 'turnover_value']]


