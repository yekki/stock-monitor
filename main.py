#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import time
import requests
import os
from click import secho, style
from pathlib import Path


ALERT_STOCK = 'sh601668'
ALERT_VALVE = 3
ALERT_TOGGLE = False
ALERT_MESSAGE = ''


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def now_dt():
    return time.strftime('%Y-%m-%d %A %p %X', time.localtime(time.time()))


def high_or_low(a, b):
    # return bcolors.RED if a >= b else bcolors.GREEN
    return 'red' if a >= b else 'green'


def print_stock(url):
    data = requests.get(url)
    lines = data.text.split('\n')
    for line in lines:
        stock_info = line.split(',')
        if stock_info[0]:
            temp = stock_info[0].split('_')[2].replace('"', '').split('=')
            code = temp[0]
            name = temp[1]

            tody_opening_price = float(stock_info[1])
            yesterday_closing_price = float(stock_info[2])
            current_price = float(stock_info[3])
            today_highest_price = float(stock_info[4])
            today_lowest_price = float(stock_info[5])
            per = '停牌  ' if '%.2f' % tody_opening_price == '0.00' else (
                '%+.2f' % ((current_price / yesterday_closing_price - 1) * 100)) + '%'
            # 红涨绿跌
            tody_opening_price_color = high_or_low(
                tody_opening_price, yesterday_closing_price)
            current_price_color = high_or_low(
                current_price, yesterday_closing_price)
            today_highest_price_color = high_or_low(
                today_highest_price, yesterday_closing_price)
            today_lowest_price_color = high_or_low(
                today_lowest_price, yesterday_closing_price)

            margin = 0
            margin_ratio = 0
            stock_position = int(df[df.股票代码 == code].values[0][1])
            stock_volume = float(df[df.股票代码 == code].values[0][2])

            if '%.2f' % tody_opening_price != '0.00':
                margin = (current_price - stock_volume) * stock_position
                margin_ratio = '/' if stock_volume == 0 else (
                    '%+.2f' % ((current_price / stock_volume - 1) * 100)) + '%'
                margin_color = high_or_low(current_price, stock_volume)
            else:
                margin = (yesterday_closing_price -
                          stock_volume) * stock_position
                margin_ratio = '/' if stock_volume == 0 else (
                    '%+.2f' % ((yesterday_closing_price / stock_volume - 1) * 100)) + '%'
                margin_color = high_or_low(
                    yesterday_closing_price, stock_volume)

            output = style(
                f'{code} {name} {yesterday_closing_price: 10.2f}', fg='white')
            output += style(f' {tody_opening_price:10.2f}',
                            fg=tody_opening_price_color)
            output += style(f' {today_highest_price:10.2f}',
                            fg=today_highest_price_color)
            output += style(f' {today_lowest_price:10.2f}',
                            fg=today_lowest_price_color)
            output += style(f' {current_price:10.2f}', fg=current_price_color)
            output += style(f' {per:>8}', fg=current_price_color)
            output += style(f' {"/":>6}', fg=margin_color) if margin == 0 else style(f' {stock_volume:>6.2f}',
                                                                                     fg=margin_color)
            output += style(f' {margin_ratio:>10}',
                            fg=margin_color)
            output += style(f' {"/":>10}', fg=margin_color) if margin == 0 else style(f' {margin:10.2f}',
                                                                                      fg=margin_color)
            output += style(f' {"/":>10}', fg=margin_color) if margin == 0 else style(f' {stock_position:10}',
                                                                                      fg='white')
            secho(output)

            # alert check
            global ALERT_TOGGLE, ALERT_VALVE, ALERT_STOCK, ALERT_MESSAGE
            if not ALERT_TOGGLE:

                gap = (current_price / yesterday_closing_price - 1) * 100

                if gap > ALERT_VALVE and code == ALERT_STOCK:
                    ALERT_TOGGLE = True
                    ALERT_MESSAGE = style(
                        f'\t涨幅告警: {name} - {gap:.2f}%', bg='red')


df = pd.read_csv(os.path.join(Path.home(), '.stocks'), delimiter=",")
url = "http://hq.sinajs.cn/list=" + ','.join([c for c in df['股票代码']])

if __name__ == "__main__":
    while True:
        clear()
        secho("代码      名称         昨收        今开     最高        最低       现价     涨幅    成本   盈亏比例    持仓市值   持仓股数", fg='white', bold=True)
        print_stock(url)
        secho(style(now_dt(), fg='yellow') + ALERT_MESSAGE)
        time.sleep(5)
