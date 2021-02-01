# -*- coding: utf-8 -*-
"""
Created on 2021.01.30

@author: hankin
@desc:
    分析福利彩票双色球中奖号码
    网站：http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html
@other:
    中国福利彩票双色球规则: 
    一等奖：当奖池资金低于1亿元时，奖金总额为当期高奖级奖金的75%与奖池中累积的资金之和，单注奖金按注均分，单注最高限额封顶500万元。当奖池资金高于1亿元（含）时，奖金总额包括两部分，一部分为当期高奖级奖金的55%与奖池中累积的资金之和，单注奖金按注均分，单注最高限额封顶500万元；另一部分为当期高奖级奖金的20%，单注奖金按注均分，单注最高限额封顶500万元。
    二等奖：奖金总额为当期高奖级奖金的25%，单注奖金按注均分，单注最高限额封顶500万元。
    三等奖：单注奖金固定为3000元。
    四等奖：单注奖金固定为200元。
    五等奖：单注奖金固定为10元。
    六等奖：单注奖金固定为5元。
    一等奖（6+1）中奖概率为：红球33选6乘以蓝球16选1=1/17721088=0.0000056%；
    二等奖（6+0）中奖概率为：红球33选6乘以蓝球16选0=15/17721088=0.0000846%；
    三等奖（5+1）中奖概率为：红球33选5乘以蓝球16选1=162/17721088=0.000914%；
    四等奖（5+0、4+1）中奖概率为：红球33选5乘以蓝球16选0=7695/17721088=0.0434%；
    五等奖（4+0、3+1）中奖概率为：红球33选4乘以蓝球16选0=137475/17721088=0.7758%；
    六等奖（2+1、1+1、0+1）中奖概率为：红球33选2乘以蓝球16选1=1043640/17721088=5.889%；
    共计中奖率：6.71%。
"""

import pandas as pd
import numpy as np
import  requests
import  bs4
import logging
from selenium import webdriver
import time

def lottery_number_handler(lottery_number):
    '''彩票数字处理器
    
    @desc  将字符串类型的彩票数字转换为数字列表
    @param lottery_number: 字符串类型的彩票数字
    @return lottery_number: 彩票数字列表
    '''
    
    print(lottery_number)
    lottery_number = lottery_number.split(' ')
    print(lottery_number)
    try:
        lottery_number.remove(' ')
    except:
        pass
    lottery_number = [int(number) for number in lottery_number]
    return lottery_number

def is_win_a_prize_in_a_lottery(history_data, lottery_number):
    '''是否中奖
    
    @desc  是否在历史长河中中过奖
    @param lottery_numbers: 7个数字的彩票号码
    @param history_data: 历史中奖数据
    @return 是否中奖,中几等奖
    '''
    
    # 判断
    
    prize_numbers = history_data['中奖号码'].values
    print('prize_numbers len: {}.'.format(len(prize_numbers)))
    for prize_number in prize_numbers:
        print('prize_numbers: {}.'.format(prize_number))
        prize_number_list = lottery_number_handler(prize_number)
        red_ball = prize_number_list[:-1]
        blue_ball = prize_number_list[-1:-1]
        print('red_ball: {}, blue_ball: {}.'.format(red_ball, blue_ball))
        break

def get_history_data(is_online=True):
    '''获取历史中奖数据
    
    @desc  网站: http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html
    @param is_online: 是否离线获取,分为网上在线爬取或者本地文件读取
    @return history_data: 返回历史中奖数据
    '''
    # 历史中奖数据文件保存
    save_data_file_path = './历史中奖数据.xlsx'
    # 历史中奖数据dataframe结构体
    history_data = pd.DataFrame()
    
    if is_online:
        # 历史中奖数据列名
        columns = []
        
        # 页面从1开始,但不包括50
        for page_index in range(1, 4):
            # 爬取的网页地址
            url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_{}.html'.format(page_index)
            
            # 使用read.html爬取表格数据
            table_data = pd.read_html(url, header=0, encoding='utf-8')[0]
            print('table count = {}, type = {}.'.format(len(table_data), type(table_data)))
            
            # 默认的header不如第0行,更换列名
            print(table_data.columns.values.tolist())
            print(table_data.iloc[0].values)
            columns = table_data.iloc[0].values
            
            # 去除0行和21行的数据,去除详细一列的数据
            table_data = table_data.drop([0,21])
            table_data = table_data.drop(['详细'],axis=1)
            columns = np.delete(columns, len(columns)-1)
            
            if history_data.shape[0]:
                history_data = history_data.append(table_data)
            else:
                history_data = table_data.copy()
            print('DataFrame [history_data] shape: [{} x {}].'.format(history_data.shape[0], history_data.shape[1]))
        
        # 对历史中奖数据列名重命名
        print('history_data type: {}, columns: {}.'.format(type(history_data), columns))
        history_data.columns = columns
        
        # 保存文件到本地
        history_data.to_excel(save_data_file_path, index=False, header=True)
    else:
        history_data = pd.read_excel(save_data_file_path)
        
    return history_data
    
if __name__ == '__main__':
    begin_time = time.time()
    
    # 获取历史中奖数据
    history_data = get_history_data(False)
    print('history_data.shape: {}.'.format(history_data.shape))
    
    # 处理彩票数字
    lottery_number = '01 09 23 24 27 29 06'
    lottery_number = lottery_number_handler(lottery_number)
    
    # 查询是否中奖
    is_win_a_prize_in_a_lottery(history_data, lottery_number)
    
    end_time = time.time()
    print('共花费 {} s时间'.format(round(end_time - begin_time, 2)))



