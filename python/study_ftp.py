# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 13:32:40 2020

@author: hankin

https://www.cnblogs.com/z3286586/p/11014468.html
"""

import ftplib
import os

#中转文件名称
temp_file_name = "msg_between_extranet_and_intranet.txt"
#云端指定中转站文件夹路径
remote_dir_path = "VDI/hj/temp/"
#本地临时文件夹路径
local_dir_path = "D:/Downloads/"

if not os.path.exists(local_dir_path):
	   os.makedirs(local_dir_path)

class MyFTP():
	host_ip = "199.200.5.88"
	user_name = "test"
	password = "test"
	
	def __init__(self):     
		self._ftp_connect_()
		self._create_empty_dir_(remote_dir_path)
	
	def _create_empty_dir_(self, dir_path):
		try:
			self.ftp.rmd(remote_dir_path)
		except ftplib.error_perm as err:
			print(err)
		try:
			self.ftp.mkd(remote_dir_path)
		except ftplib.error_perm as err:
			print(err)
			self.ftp.cwd(remote_dir_path)
			files = self.ftp.nlst()
			for file in files:
				self.ftp.delete(file)
	
	def _ftp_connect_(self):
	    """建立ftp连接
		"""
		
	    self.ftp = ftplib.FTP()
	    #ftp.set_debuglevel(2)
	    self.ftp.connect(self.host_ip, 21)
	    self.ftp.login(self.user_name, self.password)
	    self.ftp.encoding = 'gbk'
	    	
	def download_file(self, local_file_path, remote_file_path):
	    """从ftp下载文件
		Parameters
	    ----------
	    local_path : str
	        本地文件路径
	    remote_path : str
	        云端文件路径

	    Returns
	    -------
	    bool
	        成功返回True,失败False
		"""
	    
	    bufsize = 1024
	    fp = open(local_file_path, 'wb')
	    self.ftp.retrbinary('RETR ' + remote_file_path, fp.write, bufsize)
	    self.ftp.set_debuglevel(0)
	    fp.close()
	
	def upload_file(self, local_file_path, remote_file_path):
	    """从本地上传文件到ftp
		Parameters
	    ----------
	    local_path : str
	        本地文件路径
	    remote_path : str
	        云端文件路径
	
	    Returns
	    -------
	    bool
	        成功返回True,失败False
		"""

	    bufsize = 1024
	    fp = open(local_file_path, 'rb')
	    print(11111)
	    self.ftp.storbinary('STOR ' + remote_file_path, fp, bufsize)
	    print(2222)
	    self.ftp.set_debuglevel(0)
	    fp.close()
	
	def ftp_quit(self):
		self.ftp.quit()
		
if __name__ == "__main__":
	ftp = MyFTP()
	
	remote_file_path = remote_dir_path + '山东大学.zip'
	path = "D:/Users/Administrator/Desktop/山东大学.zip"
	#path = path.encode("utf-8", 'ignore').decode("latin1")
	#remote_file_path = remote_file_path.encode("utf-8", 'ignore').decode("latin1")
	#ftp.upload_file(path, remote_file_path)
	#ftp.download_file(local_dir_path, remote_dir_path)



	ftp.ftp_quit()
