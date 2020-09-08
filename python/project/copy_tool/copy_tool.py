# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 19:36:49 2020

@author: hankin
@description:
    copy tool for ftp
"""
import win32api,win32con
from ftplib import FTP
from tkinter import filedialog, messagebox #这两个需要单独导入
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button #导入ttk模块中的指定几个组件
import tkinter
import PIL
from editor_style import theme_color, ICONS #这里就是从之前命名的文件中导入两个参数
from PIL import ImageTk
import tkinter.font

class MyFTP():
	host_ip = "199.200.5.88"
	user_name = "test"
	password = "test"
	remote_file_path = "VDI/hj/msg_between_extranet_and_intranet.txt"
	local_file_path = "D:/msg_between_extranet_and_intranet.txt"
	
	def __init__(self):     
		self._ftp_connect_()
		pass
		
	def _ftp_connect_(self):
	    """建立ftp连接
	
		Parameters
	    ----------
	    ftp : str
	        ip地址
	    username : str
	        合法的sql语句
	    password : 
	
	    Returns
	    -------
	    bool
	        成功返回True,失败False
	
		"""
	    self.ftp = FTP()
	    # ftp.set_debuglevel(2)
	    self.ftp.connect(self.host_ip, 21)
	    self.ftp.login(self.user_name, self.password)
	    	
	def download_file(self):
	    """从ftp下载文件
	
		Parameters
	    ----------
	    ftp : str
	        创建的表的名称
	    remotepath : str
	        合法的sql语句
	    localpath : 
	
	    Returns
	    -------
	    bool
	        成功返回True,失败False
	
		"""
	    
	    bufsize = 1024
	    fp = open(self.local_file_path, 'wb')
	    self.ftp.retrbinary('RETR ' + self.remote_file_path, fp.write, bufsize)
	    self.ftp.set_debuglevel(0)
	    fp.close()
	
	def upload_file(self):
	    """从本地上传文件到ftp
	
		Parameters
	    ----------
	    ftp : str
	        创建的表的名称
	    remotepath : str
	        合法的sql语句
	    localpath : 
	
	    Returns
	    -------
	    bool
	        成功返回True,失败False
	
		"""
	    bufsize = 1024
	    fp = open(self.local_file_path, 'rb')
	    self.ftp.storbinary('STOR ' + self.remote_file_path, fp, bufsize)
	    self.ftp.set_debuglevel(0)
	    fp.close()
	
	def ftp_quit(self):
		self.ftp.quit()

class CopyTool(tkinter.Tk):
	'''主窗口ui类
	'''
	
	my_ftp = MyFTP()
	
	def __init__(self):     
		'''初始化自己的创建的CopyTool类
		'''
		
		super().__init__()  	#在继承Tk这个类的基础上在自己的类中添加内容
		self._set_window_() 	#设置程序运行主窗口
		self._create_menu_bar_()#创建菜单组件
		self._create_body_()
		self._create_right_popup_menu()
	
	def _set_window_(self):
		'''设置初始化窗口的属性
		'''
		
		self.title("CopyTool")              			    #窗口名称
		self.resizable(False, False)
		#self.update()
		scn_width, scn_height = self.maxsize() 				#获得程序运行机器的分辨率（屏幕的长和宽）
		wm_val = '750x450+{}+{}'.format((scn_width - 750) // 2, (scn_height - 450) // 2)
		self.geometry(wm_val) 				   				#将窗口设置在屏幕的中间
		self.iconbitmap("icon/copy_tool.ico")  	 	 	 	#加载一下窗口的左上方显示的图片
		self.protocol('WM_DELETE_WINDOW', self.exit_copy_tool) #设置窗口关闭提醒
		
	def _create_menu_bar_(self):
		'''创建菜单栏
		'''
		menu_bar = tkinter.Menu(self)	#继承原来Tk的Menu的对象
		
		file_menu = tkinter.Menu(menu_bar, tearoff = 0)
		file_menu.add_command(label='打开',accelerator = 'Ctrl+O', command=self.open_file)
		file_menu.add_separator()  #设置分割线
		file_menu.add_command(label='退出',accelerator = 'Alt+F4', command=self.exit_copy_tool)
		menu_bar.add_cascade(label='文件',menu = file_menu) 	#创建文件的菜单栏
	
		#编辑菜单
		edit_menu = tkinter.Menu(menu_bar,tearoff = 0)  #基于菜单栏实例化“编辑”关联选项栏对象
		edit_menu.add_command(label='撤销',accelerator = 'Ctrl+Z',command = lambda : self.handle_menu_action('撤销'))
		edit_menu.add_command(label='恢复',accelerator = 'Ctrl+Y',command = lambda : self.handle_menu_action('恢复'))
		edit_menu.add_separator()
		edit_menu.add_command(label='剪切',accelerator = 'Ctrl+X',command = lambda : self.handle_menu_action('剪切'))
		edit_menu.add_command(label='复制',accelerator = 'Ctrl+C',command = lambda : self.handle_menu_action('复制'))
		edit_menu.add_command(label='粘贴',accelerator = 'Ctrl+V',command = lambda : self.handle_menu_action('粘贴'))
		edit_menu.add_separator()
		edit_menu.add_command(label='全选',accelerator = 'Ctrl+A',command = lambda : self.handle_menu_action('全选'))
		menu_bar.add_cascade(label='编辑',menu=edit_menu)  	#将“编辑”关联选项栏放在“编辑”菜单栏上
	
		#视图菜单
		view_menu = tkinter.Menu(menu_bar, tearoff = 0) #将“视图”关联选项栏放在“视图”菜单栏上
		self.is_show_line_num = tkinter.IntVar() 		#为了方便定义的这个变量在类中其他的函数中使用，这里将变量变成类中的实例属性
		self.is_show_line_num.set(1)
		view_menu.add_checkbutton(label='显示行号', variable=self.is_show_line_num,
								  command=self._update_line_num)
		self.is_highlight_line = tkinter.IntVar()		#这里也是和上面一样，因为后面要用到这个变量
		view_menu.add_checkbutton(label='高亮当前行', onvalue=1, offvalue=0,
									  variable=self.is_highlight_line, command=self._toggle_highlight)  #通过checkbutton来实现功能
	
		#在主题菜单中再添加一个子菜单
		theme_menu = tkinter.Menu(menu_bar, tearoff = 0)
		self.theme_choice = tkinter.StringVar()
		self.theme_choice.set('Default')
		for k in sorted(theme_color): 	#这里的theme_color就是之前从editor_style.py文件中导入的参数内容
			theme_menu.add_radiobutton(label=k, variable=self.theme_choice, command=self.change_theme)
		view_menu.add_cascade(label='主题', menu=theme_menu) #注意这里添加的菜单栏指定的对象	
		menu_bar.add_cascade(label='视图', menu=view_menu)  #注意这里添加的菜单栏指定的对象	
	
		#关于菜单
		about_menu = tkinter.Menu(menu_bar, tearoff= 0)
		about_menu.add_command(label = '关于', command=lambda: self.show_messagebox('关于')) #这里暂时未设置快捷键
		about_menu.add_command(label = '帮助', command=lambda: self.show_messagebox('帮助')) #一般是全局的快捷键，比如帮助的快捷键一般是F1
		menu_bar.add_cascade(label='关于',menu=about_menu)
		#注意需要把帮助文档绑定为全局事件
		self.bind_all('<KeyPress-F1>', lambda e: self.show_messagebox("帮助"))
		
		self['menu'] = menu_bar				
	
	def open_file(self,event=None):
		input_file = filedialog.askopenfilename(filetypes=[('所有文件','*.*'),('文本文档','*.txt')])  #弹出文件对话框，设置选择文件的类型
	
		if input_file:   			#如果用户选择了文本，则进行打开
			#print(input_file)   	#这里可以调试，看一下选中文本的路径的形式（绝对路径）
			self.title('{} - EditorPlus'.format(os.path.basename(input_file))) #以文件的名称进行窗口标题的命名
			self.file_name = input_file 	   #将这个打开的文件对象命名为其原来文件的名称
			self.content_text.delete(1.0, tkinter.END)  #删除当前文本内容中的数据
			with open(input_file, 'r') as _file:
				self.content_text.insert(1.0,_file.read())  #将要打开文件中的数据写入到文本内容中
	def show_messagebox(self, type):
		if type == "帮助":
			messagebox.showinfo("帮助", "这是帮助文档！", icon='question')
		else:
			messagebox.showinfo("关于", "CopyTool_V2.0")

		
	#通过设置_update_line_num函数来实现主要的功能
	def _toggle_highlight(self):     #高亮函数
		if self.is_highlight_line.get():  #如果是选择高亮，进行下一步
			self.content_text.tag_remove("active_line", 1.0, "end")    #移除所有的标记
			self.content_text.tag_add("active_line", "insert linestart", "insert lineend+1c")
			#添加新标记
			self.content_text.after(200, self._toggle_highlight)  #递归，不断的检查是否高亮
		else:
			self.content_text.tag_remove("active_line", 1.0, "end")  #取消高亮		

	def change_theme(self):
		selected_theme = self.theme_choice.get()  #选取设定的主体颜色
		fg_bg = theme_color.get(selected_theme)   #包含了前景色和背景色
		fg_color, bg_color = fg_bg.split('.')     #提取颜色
		self.content_text.config(bg=bg_color, fg=fg_color)  #颜色设定

	def _update_line_num(self):
		if self.is_show_line_num.get():  #如果是选择了显示行号，进行下面的内容
			row, col = self.content_text.index("end").split('.')  #主要是获取行数
			line_num_content = "\n".join([str(i) for i in range(1, int(row))]) #获取文本行数据
			self.line_number_bar.config(state='normal')  #将文本栏状态激活
			self.line_number_bar.delete('1.0', 'end')    #删除原有的行号数据
			self.line_number_bar.insert('1.0', line_num_content) #插入行号文本数据
			self.line_number_bar.config(state='disabled') #再次封印行号栏
		else:  #如果不显示行号的话，进行下面的操作
			self.line_number_bar.config(state='normal')  #将文本栏状态激活
			self.line_number_bar.delete('1.0', 'end')  #删除原有的行号数据，这样就没有行号数据了
			self.line_number_bar.config(state='disabled') #再次封印行号栏
		
	def _create_body_(self):
		'''主体部分
		'''
	
		#设置字体slant=tf.ITALIC,underline=1,overstrike=1,consolas
		ft = tkinter.font.Font(family=r'微软雅黑', weight=tkinter.font.NORMAL, size=12)  
	    
	    #上面部分
		fm_up = tkinter.Frame()
		#fm_up.propagate(0)
		input_content = tkinter.Entry(fm_up, width=30, font=ft)
		input_content.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X, padx=5, pady=5)
		upload_btn = tkinter.Button(fm_up,text='send', width=10, height=1,\
                           command=lambda:self.upload_btn_cliecked(self.content_text), font=ft, compound='center') 
		upload_btn.pack(side=tkinter.LEFT, pady=5)     
		download_btn = tkinter.Button(fm_up,text='recive', width=10, height=1,\
                             command=lambda:self.download_btn_cliecked(self.content_text), font=ft, compound='center') 
		download_btn.pack(side=tkinter.LEFT, padx=5) 
    
		fm_up.pack(fill=tkinter.X)
	    
		#中间部分
		fm_mid = tkinter.Frame()
		fm_mid.propagate(0)
		#创建行号栏（takefocus屏蔽焦点）
		self.line_number_bar = tkinter.Text(fm_mid,width=3, padx=3, takefocus=0, border=0,
			background='#F0E68C',state='disabled', font=ft)  #之后会使用这个变量，所以将其转换为实例属性
		self.line_number_bar.pack(side='left',fill='y')
	
		#创建文本输入框
		self.content_text = tkinter.Text(fm_mid, wrap = 'word', undo =True, font=ft)
		self.content_text.pack(expand='yes',fill='both')
		self.content_text.bind('<Control-O>', self.open_file)
		self.content_text.bind('<Control-o>', self.open_file)
		self.content_text.bind('<Alt-F4>', self.exit_copy_tool)
		self.content_text.bind('<Any-KeyPress>', lambda e: self._update_line_num())
		self.content_text.tag_configure('active_line', background='#EEEEE0')
		self.bind_all('<KeyPress-F1>', lambda e: self.show_messagebox("帮助"))
	
		#创建滚动条
		scroll_bar = Scrollbar(self.content_text)
		scroll_bar['command'] = self.content_text.yview
		self.content_text['yscrollcommand'] = scroll_bar.set
		scroll_bar.pack(side='right',fill='y')
		
		fm_mid.pack(fill=tkinter.BOTH, expand='yes')
		
	    #下面部分：拷贝按钮
		fm_down = tkinter.Frame()
		#fm_down.propagate(0)
		copy_btn = tkinter.Button(fm_down,text='copy', command=lambda:self.copy_btn_cliecked(self.content_text), font=ft, compound='center') 
		copy_btn.pack(fill='both')
		fm_down.pack(fill='x')
		
	def _create_right_popup_menu(self):
		popup_menu = tkinter.Menu(self.content_text, tearoff=0)
		for it1, it2 in zip(['剪切', '复制', '粘贴', '撤销', '恢复'],
							['cut', 'copy', 'paste', 'undo', 'redo']):
			popup_menu.add_command(label=it1, compound='left',
								   command=self._shortcut_action(it2))
		popup_menu.add_separator()
		popup_menu.add_command(label='全选', command = lambda: self.handle_menu_action("全选"))
		self.content_text.bind('<Button-3>',
							   lambda event: popup_menu.tk_popup(event.x_root, event.y_root))
		
	def _shortcut_action(self, type):
		def handle():
			if type == "new_file":
				self.new_file()
			elif type == "open_file":
				self.open_file()
			elif type == "save":
				self.save()
			if type == "cut":
				self.handle_menu_action("剪切")
			elif type == "copy":
				self.handle_menu_action("复制")
			elif type == "paste":
				self.handle_menu_action("粘贴")
			elif type == "undo":
				self.handle_menu_action("撤销")
			elif type == "redo":
				self.handle_menu_action("恢复")
			elif type == "find_text":
				self.find_text()
			if type != "copy" and type != "save":
				self._update_line_num()
		return handle #最后返回的是就是handle对象

	def handle_menu_action(self, action_type):
		if action_type == "撤销":
			self.content_text.event_generate("<<Undo>>")
		elif action_type == "恢复":
			self.content_text.event_generate("<<Redo>>")
		elif action_type == "剪切":
			self.content_text.event_generate("<<Cut>>")
		elif action_type == "复制":
			self.content_text.event_generate("<<Copy>>")
		elif action_type == "粘贴":
			self.content_text.event_generate("<<Paste>>")
		elif action_type == "全选":
			self.content_text.event_generate("<<SelectAll>>")
		if action_type != "复制":
			self._update_line_num()

		return 'break'
	
	def exit_copy_tool(self): 
		'''退出提示框
		'''
		
		if messagebox.askokcancel('退出?','确定退出吗?'):      #设置文本提示框
			self.destroy() 									 #满足条件的话主窗口退出
			self.my_ftp.ftp_quit()
	
	def upload_btn_cliecked(self, display_content):
	    '''
	    发送按钮点击事件
	    '''
	    content = display_content.get('0.0', 'end').strip()
	    print('正在写入', self.my_ftp.local_file_path)
	    try:
	        with open(self.my_ftp.local_file_path, 'w', encoding='utf-8') as f:
	            f.write(content)
	    except Exception as ex:
	        print('打开文件失败, error=', ex)
	        
	    self.my_ftp.upload_file()
	    # 提醒OK消息框
	    win32api.MessageBox(0, "上传成功", "提醒", win32con.MB_OK)
	    
	def download_btn_cliecked(self, display_content):
	    '''
	    接收消息按钮点击事件
	    
	    :param display_content:Text组件
	    '''
	    self.my_ftp.download_file()
	    
	    print('正在读取', self.my_ftp.local_file_path)
	    content_list = []
	    
	    try:
	        with open(self.my_ftp.local_file_path, 'r', encoding='utf-8') as f:
	            content_list = f.readlines() 
	    except Exception as ex:
	        print('打开文件失败, error=', ex)
	    
	    content = ''
	    for elem in content_list:
	        content = content + elem
	    
	    display_content.delete('0.0', 'end')
	    display_content.insert('insert', content)
	    
	def copy_btn_cliecked(self, display_content):
	    '''
	    复制内容按钮点击事件
	    '''
	    # 打印显示内容
	    content = display_content.get('0.0', 'end').strip()
	    print(content)
	    
	    # 将内容弄到剪切板
	    display_content.event_generate("<<SelectAll>>")
	    display_content.event_generate("<<Copy>>")
   

    
if __name__ == "__main__":
	app = CopyTool()      #类的实例化
	app.mainloop()			#程序运行
    
    
    
    
    
    