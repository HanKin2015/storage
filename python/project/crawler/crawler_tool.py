# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:19:10 2020

@author: hankin
@description:
    Download picture crawler by python and tkinter
"""

import win32api
import win32con
from tkinter import filedialog, messagebox
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button 
import tkinter
import tkinter.font
import os, sys
import base64
import logging
import pandas as pd
import numpy as np
from PIL import ImageTk, Image
import time
import threading

# 增加libary库的搜索路径
sys.path.append('../../libary/')

# 导入可视化窗口库
from visualized_window import VisualizedWindow
# 导入自定义的Entry库
from entrywithplaceholder import EntryWithPlaceholder

# 全局变量
local_dir_path = 'D:/Picture/'
if not os.path.exists(local_dir_path):
    os.makedirs(local_dir_path)

url = ''
log_file_path = './crawler_tool.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_file_path,
                    filemode='a')



class CrawlerTool(VisualizedWindow):
    '''继承可视化窗口
    '''

    def __init__(self):
        '''初始化创建自己的类
        '''
        super().__init__()      # 在继承Tk这个类的基础上在自己的类中添加内容
        self.title("爬虫工具箱")
        self.screen_width, self.screen_height = self.maxsize()  # 获得程序运行机器的分辨率（屏幕的长和宽）
    
    def _create_body_(self):
        '''重写主体布局
        绝对布局：label.place(x=10, y=10)
        相对布局：label.pack(fill=tkinter.X, side=tkinter.TOP)
        表格布局：label.grid(row=0, column=0)
        tkinter.LEFT
        tkinter.BOTTOM
        tkinter.TOP
        tkinter.RIGHT
        
        entry无placeholder
        '''
        # 设置字体slant=tf.ITALIC,underline=1,overstrike=1,consolas
        ft = tkinter.font.Font(family=r'微软雅黑', weight=tkinter.font.NORMAL, size=12)

        # 上面部分
        fm_up = tkinter.Frame()
        #self.input_content = tkinter.Entry(fm_up, width=30, font=ft)
        
        self.default_url = tkinter.ttk.Combobox(fm_up, textvariable=tkinter.StringVar(), font=ft)
        self.default_url['values'] = ('招商', '越秀', '中海')
        #self.default_url.current(0)
        self.default_url.bind('<<ComboboxSelected>>', self.default_url_combox_cliecked)
        self.default_url.grid(row=0, column=0)
        self.default_building = tkinter.ttk.Combobox(fm_up, textvariable=tkinter.StringVar(), font=ft)       
        #self.default_building.bind('<<ComboboxSelected>>', self.default_url_combox_cliecked)
        self.default_building.grid(row=1, column=0)
        
        self.crawling_url = EntryWithPlaceholder(fm_up, '请输入爬取网址', font=ft)
        self.crawling_url.grid(row=0, column=1)
        self.crawling_regex = EntryWithPlaceholder(fm_up, '请输入爬取规则', font=ft)
        self.crawling_regex.grid(row=1, column=1, sticky=tkinter.E+tkinter.W)
        self.crawling_index = EntryWithPlaceholder(fm_up, '请输入爬取索引', font=ft)
        self.crawling_index.grid(row=1, column=2)

        crawling_btn = tkinter.Button(fm_up, text='爬取', width=10, height=1,
                                    command=lambda: self.progressbar_window(), compound='center')
        crawling_btn.grid(row=0, column=3)
        analysis_btn = tkinter.Button(fm_up, text='分析', width=10, height=1,
                                      command=lambda: self.analysis_btn_clicked(),compound='center')
        analysis_btn.grid(row=1, column=3)
        show_btn = tkinter.Button(fm_up, text='显示', width=10, height=1,
                                    command=lambda: self.show_btn_clicked(), compound='center')
        show_btn.grid(row=1, column=4)

        fm_up.pack(fill=tkinter.X)

        # 中间部分
        fm_mid = tkinter.Frame()
        fm_mid.propagate(0)

        # 创建表格
        columns = ('户室号', '楼层', '房屋用途', '房屋类型', '装修状态', '建筑面积', '套内面积', '分摊面积', '销售状态')
        self.hourse_table = tkinter.ttk.Treeview(fm_mid, show = "headings", columns = columns, selectmode = tkinter.BROWSE)
        
        for column in columns:
            print(column)
            self.hourse_table.column(column, width = 50, anchor = 'center')
            self.hourse_table.heading(column, text = column, command=lambda _column=column: self.treeview_sort_column(self.hourse_table, _column, False))
        
        # 鼠标左键抬起
        self.hourse_table.bind('<ButtonRelease-1>', self.treeview_selected_row)
        # 选中行
        #self.hourse_table.bind('<<TreeviewSelect>>', self.treeview_selected_row)
        self.hourse_table.pack(expand='yes', fill='both')
        
        # 创建滚动条
        scroll_bar = Scrollbar(self.hourse_table)
        scroll_bar['command'] = self.hourse_table.yview
        self.hourse_table['yscrollcommand'] = scroll_bar.set
        scroll_bar.pack(side='right', fill='y')

        fm_mid.pack(fill=tkinter.BOTH, expand='yes')

        # 下面部分：预留部分
        fm_down = tkinter.Frame()
        # fm_down.propagate(0)
        copy_btn = tkinter.Button(fm_down, text='青春的羽翼,划破伤痛的记忆', font=ft, compound='center')
        copy_btn.pack(fill='both')
        fm_down.pack(fill='x')
        
    # 获取当前点击行的值
    def treeview_selected_row(self, event):  # 单击
        for item in self.hourse_table.selection():
            item_text = self.hourse_table.item(item, "values")
            print(item_text)
 
    def treeview_sort_column(self, table, column, reverse):#Treeview、列名、排列方式
        l = [(table.set(k, column), k) for k in table.get_children('')]
        #print(table.get_children(''))
        print(type(l))
        print(l)
        l.sort(reverse=reverse)#排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):#根据排序后索引移动
            table.move(k, '', index)
            #print(k)
        table.heading(column, command=lambda: self.treeview_sort_column(table, column, not reverse))#重写标题，使之成为再点倒序的标题

 
    def default_url_combox_cliecked(self, event):
        print(type(event))
        print(self.default_url.current())
        print(self.default_url.get())
        estate = self.default_url.get()
        if estate == '招商':
            self.default_building['values'] = ('9栋', '10栋', '6栋','7栋','8栋', '1栋')
            self.default_building.current(0)
            self.crawling_url.foc_in()
            self.crawling_url.insert(0, 'http://www.cszjxx.net/floorinfo/202004160830')
            self.crawling_regex.foc_in()
            self.crawling_regex.insert(0, 'div.hs_xqxx > table > tbody > tr > td')
            self.crawling_index.foc_in()
            self.crawling_index.insert(0, '3')
      
    def crawling_btn_clicked(self):
        print(self.crawling_url.get())
        print(self.crawling_regex.get())
        print(self.crawling_index.get())
    
    def show_building_information(self, estate, building):
        data = pd.read_excel('./data/data.xlsx', index=False, sheet_name=None)
        sheet_names = list(data.keys()) 
        print(sheet_names)
        for sheet_name in sheet_names:
            # 清空表格数据
            items = self.hourse_table.get_children()
            [self.hourse_table.delete(item) for item in items]
            
            if sheet_name == building:
                data = pd.read_excel('./data/data.xlsx', index=False, sheet_name=sheet_name)
                #print(data.values)
                values = data.values
                
                for value in values:
                    self.hourse_table.insert('', 'end', values=value.tolist())
                break
                
    def show_btn_clicked(self):
        estate = self.default_url.get()
        building = self.default_building.get()
        self.show_building_information(estate, building)  
    
    def analysis_btn_clicked(self):
        top = tkinter.Toplevel()
        top.title('分析结果')
        print(self.screen_width, self.screen_height)
        window_width = 800
        window_hight = 600
        wm_val = '{}x{}+{}+{}'.format(window_width, window_hight, (self.screen_width - window_width) //
                                        4, (self.screen_height - window_hight) // 2)
        top.geometry(wm_val)       # 将窗口设置在屏幕的中间
        
        # 创建表格
        columns = ('对应栋号', '出售状态', '总共数量', '100平方', '124平方', '142平方')
        hourse_table = tkinter.ttk.Treeview(top, show = "headings", columns = columns, selectmode = tkinter.BROWSE)
        
        for column in columns:
            print(column)
            hourse_table.column(column, width = 50, anchor = 'center')
            hourse_table.heading(column, text = column)
            
        hourse_table.pack(expand='yes', fill='both')
        
        # 创建滚动条
        scroll_bar = Scrollbar(hourse_table)
        scroll_bar['command'] = hourse_table.yview
        hourse_table['yscrollcommand'] = scroll_bar.set
        scroll_bar.pack(side='right', fill='y')
        
        data = pd.read_excel('./data/sale_result.xlsx', index=False)
        print('data size = ', data.shape)
        values = data.values
        #print(values)
        for value in values:
            print(type(value[0]))
            # np.NaN是float浮点数，无法比较相等
            if type(value[0]) == float:
                print('This is null.')
                hourse_table.insert('', 'end', values=('','','','','',''))
            else:
                hourse_table.insert('', 'end', values=value.tolist())
            
        top.mainloop()
        
    def start(self):
        def real_traitement():
            self.pb.step(amount=5.0)
            self.pb.start(interval=500)
            while True:
                val = self.val.get()
                self.progress_value.set('{}%'.format(val))
                if val >= 50:
                    break
                time.sleep(1)
                
            self.pb.stop()
            self.pb.grid_forget()
            self.start_btn['state']='normal'
            
        self.start_btn['state']='disabled'
        threading.Thread(target=real_traitement).start()

    def progressbar_window(self):
        top = tkinter.Toplevel()
        top.title('进度条')
        window_width = 600
        window_hight = 150
        wm_val = '{}x{}+{}+{}'.format(window_width, window_hight, (self.screen_width - window_width) //
                                        4, (self.screen_height - window_hight) // 2)
        top.geometry(wm_val)       # 将窗口设置在屏幕的中间
        
        
        tkinter.Label(top, text='下载进度:', ).place(x=50, y=60)
        # 定义变量,必须是使用的是tk里的这个变量
        self.progress_value = tkinter.StringVar()
        self.progress_value.set('0%')
        tkinter.Label(top, textvariable=self.progress_value).place(x=50, y=90)
        
        # 设置窗口图标
        #top.iconbitmap("./image/icon.ico")
        # 设置窗口宽高固定
        top.resizable(0, 0)
        
        '''
        进度条学习：
        mode: determinate/indeterminate
        orient(进度条的方向): HORIZONTAL/VERTICAL
        cursor: 鼠标位于进度条内时的形状
        length: 进度条长度
        maximum: 进度条最大刻度值
        style: 定义进度条的外观
        takefocus: 是否可以通过Tab获得输入焦点
        variable: 与进度条关联的变量。可以设置或获得进度条的当前值
        value: 设置或者获取进度条的当前值
        start(interval=None): 默认间隔是50毫秒。
        step(amount=None): 默认是1.0
        stop()
        '''
        
        # 进度条样式
        style = tkinter.ttk.Style()
        style.theme_use('alt')
        style.configure('blue.Horizontal.TProgressbar',
                        troughcolor  = '#4d4d4d',
                        troughrelief = 'flat',
                        background   = '#2f92ff')
        self.val = tkinter.IntVar() # 这个能解决进度条停止后变为0的问题
        self.pb = tkinter.ttk.Progressbar(top, length=400, style='blue.Horizontal.TProgressbar', orient='horizontal',maximum=100, value=0, mode="determinate", variable=self.val)
        self.pb.pack(pady = 10)
        self.start_btn = tkinter.Button(top, text="开始", command=self.start)
        self.start_btn.pack()
        
        top.mainloop()
    
if __name__ == "__main__":
    app = CrawlerTool()
    app.mainloop()              # 程序运行




















