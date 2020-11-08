import pandas as pd
import time
from termcolor import bcolors
import requests
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_now():
    return time.strftime('%Y-%m-%d %A %p %X', time.localtime(time.time()))

def high_or_low(a,b):
    return bcolors.RED if a >= b else bcolors.GREEN  

def print_stock(url):
    data = requests.get(url)
    lines = data.text.split('\n')
    for line in lines:
        stock_info = line.split(',')
        if stock_info[0]:
            temp  = stock_info[0].split('_')[2].replace('"','').split('=')
            code = temp[0]
            name = temp[1]
        
            tody_opening_price   = float(stock_info[1])
            yesterday_closing_price  = float(stock_info[2])
            current_price   = float(stock_info[3])
            today_highest_price = float(stock_info[4])
            today_lowest_price = float(stock_info[5])
            per = '停牌  ' if '%.2f' % tody_opening_price == '0.00' else  ('%+.2f' % ( ( current_price / yesterday_closing_price - 1 ) * 100 ) )+ '%'
            #红涨绿跌
            tody_opening_price_color = high_or_low(tody_opening_price, yesterday_closing_price)
            current_price_color = high_or_low(current_price, yesterday_closing_price)
            today_highest_price_color = high_or_low(today_highest_price, yesterday_closing_price)
            today_lowest_price_color = high_or_low(today_lowest_price, yesterday_closing_price)
            
            margin = 0
            margin_ratio = 0
            margin_color = bcolors.WHITE
            stock_position = int(df[df.股票代码==code].values[0][1])
            cost_of_carry = float(df[df.股票代码==code].values[0][2])
            
            if '%.2f' % tody_opening_price != '0.00':
                margin = ( current_price - cost_of_carry ) * stock_position
                margin_ratio = 0 if cost_of_carry == 0 else ( '%+.2f' % ( (current_price / cost_of_carry - 1) * 100 ) ) + '%'
                margin_color = high_or_low(current_price, cost_of_carry)
            else:
                margin = ( yesterday_closing_price - cost_of_carry ) * stock_position
                margin_ratio = 0 if cost_of_carry == 0 else ( '%+.2f' % ( (yesterday_closing_price / cost_of_carry - 1) * 100 ) ) + '%'
                margin_color = high_or_low(yesterday_closing_price, cost_of_carry)
            
            print('%s%s%s %s%4s%s %s%10.2f%s %s%10.2f%s %s%10.2f%s %s%10.2f%s %s%10.2f   %s%s    %s%10.2f     %10s%s   %s%10.2f%s' % \
                    (bcolors.WHITE, code, bcolors.ENDC,  
                     bcolors.WHITE, name, bcolors.ENDC,  
                     bcolors.WHITE, yesterday_closing_price, bcolors.ENDC,  
                     tody_opening_price_color, tody_opening_price, bcolors.ENDC, 
                     today_highest_price_color, today_highest_price, bcolors.ENDC, 
                     today_lowest_price_color, today_lowest_price, bcolors.ENDC, 
                     current_price_color, current_price, per, bcolors.ENDC,
                     margin_color, margin, margin_ratio, bcolors.ENDC,
                     bcolors.WHITE, cost_of_carry * stock_position, bcolors.ENDC))

df = pd.read_csv('stocks.csv', delimiter=",")
url = "http://hq.sinajs.cn/list=" + ','.join([ c for c in df['股票代码']])

if __name__ == "__main__":
    while True:
        clear()
        print(bcolors.WHITE, "代码      名称         昨收        今开     最高        最低       现价     涨幅      浮动数额       盈亏比例     成本金额", bcolors.ENDC)
        print(bcolors.YELLOW, get_now(), bcolors.ENDC)
        print_stock(url)
        time.sleep(5)  