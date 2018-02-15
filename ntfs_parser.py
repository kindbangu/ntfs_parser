import pytsk3, os, sys, datetime, pytz
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from os.path import expanduser

#from PyQt5 import QtGui, QtWidgets
from PyQt5 import *


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("Crawling Web")
		self.resize(1200, 750)
		toolbar = QToolBar("Toolbar")
		self.addToolBar(toolbar)

		#add select folder button
		select_folder_action = QAction(QIcon(), "Open Folder", self)
		select_folder_action.setToolTip("Open Folder")
		toolbar.addAction(select_folder_action)
		select_folder_action.triggered.connect(self.select_folder_on)

		#add save and view button
		save_view_action = QAction(QIcon(), "Save and View", self)
		save_view_action.setToolTip("Save and View")
		toolbar.addAction(save_view_action)
		save_view_action.triggered.connect(self.save_view_on)
		
		#add lineEdit
		self.le_set_fname = QLineEdit(self)
		toolbar.addSeparator()
		toolbar.addWidget(self.le_set_fname)

	#event
	def select_folder_on(self):
		global datas
		datas = []
		folder_name = self.get_folder_info()
		self.set_volume()
		self.get_fs_info(folder_name)

	def get_folder_info(self):
		global path

		try:
			path = QFileDialog.getExistingDirectory(self, "Open a folder", expanduser("~"), QFileDialog.ShowDirsOnly)
			origin_folder_name = str(path).split('/')[-1]
		except FileNotFoundError:
			pass
		self.le_set_fname.setText(path)

		return origin_folder_name

	def set_volume(self):
		global volume, fs
		volume = '\\\\.\\'+str(path).split('/')[0]
		img = pytsk3.Img_Info(volume)
		fs = pytsk3.FS_Info(img)
		print(volume)

	def get_fs_info(self, folder_name):
		directory = fs.open_dir(path=folder_name)
		cnt = 1
		for f in directory:
			try:
				if (str(f.info.name.name.decode('utf-8')) != '.' and str(f.info.name.name.decode('utf-8')) != '..' and str(f.info.name.name.decode('utf-8')) != '...') and (f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR):
					temp = folder_name + '/' + str(f.info.name.name.decode('utf-8'))
					self.get_fs_info(temp)
				elif f.info.meta.type != pytsk3.TSK_FS_META_TYPE_DIR:
					print("파일이라서 걸림: ", f.info.name.name.decode('utf-8'))
					datalist = [cnt, f.info.name.name.decode('utf-8'), f.info.meta.size, volume.split('.')[1] + '/' + folder_name,
								datetime.datetime.fromtimestamp(int(f.info.meta.mtime)).strftime('%Y-%m-%d %H:%M:%S'),
								datetime.datetime.fromtimestamp(int(f.info.meta.atime)).strftime('%Y-%m-%d %H:%M:%S'),
								datetime.datetime.fromtimestamp(int(f.info.meta.ctime)).strftime('%Y-%m-%d %H:%M:%S'),
								datetime.datetime.fromtimestamp(int(f.info.meta.crtime)).strftime('%Y-%m-%d %H:%M:%S')
								]
					datas.append(datalist)
					#print(datas)
					cnt += 1
			except AttributeError:
				print(cnt, f.info.name.name.decode('utf-8'), "has no attribute")

	def save_html(self):
		global html_file
		html_header = '''<!doctype html>
		<html lang="en">
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

		<title>http://www.blueb.co.kr</title>

		<style type="text/css">
		body{
			font-family:Arial, Helvetica, sans-serif;
			margin:0 auto;
		}
		a:link {
			color: #666;
			font-weight: bold;
			text-decoration:none;
		}
		a:visited {
			color: #666;
			font-weight:bold;
			text-decoration:none;
		}
		a:active,
		a:hover {
			color: #bd5a35;
			text-decoration:underline;
		}


		table a:link {
			color: #666;
			font-weight: bold;
			text-decoration:none;
		}
		table a:visited {
			color: #999999;
			font-weight:bold;
			text-decoration:none;
		}
		table a:active,
		table a:hover {
			color: #bd5a35;
			text-decoration:underline;
		}
		table {
			font-family:Arial, Helvetica, sans-serif;
			color:#666;
			font-size:12px;
			text-shadow: 1px 1px 0px #fff;
			background:#eaebec;
			margin:20px;
			border:#ccc 1px solid;

			-moz-border-radius:3px;
			-webkit-border-radius:3px;
			border-radius:3px;

			-moz-box-shadow: 0 1px 2px #d1d1d1;
			-webkit-box-shadow: 0 1px 2px #d1d1d1;
			box-shadow: 0 1px 2px #d1d1d1;
		}
		table th {
			padding:15px;
			border-top:1px solid #fafafa;
			border-bottom:1px solid #e0e0e0;

			background: #ededed;
			background: -webkit-gradient(linear, left top, left bottom, from(#ededed), to(#ebebeb));
			background: -moz-linear-gradient(top,  #ededed,  #ebebeb);
		}
		table th:first-child{
			text-align: left;
			padding-left:20px;
		}
		table tr:first-child th:first-child{
			-moz-border-radius-topleft:3px;
			-webkit-border-top-left-radius:3px;
			border-top-left-radius:3px;
		}
		table tr:first-child th:last-child{
			-moz-border-radius-topright:3px;
			-webkit-border-top-right-radius:3px;
			border-top-right-radius:3px;
		}
		table tr{
			text-align: center;
			padding-left:20px;
		}
		table tr td:first-child{
			text-align: left;
			padding-left:20px;
			border-left: 0;
		}
		table tr td {
			padding:12px;
			border-top: 1px solid #ffffff;
			border-bottom:1px solid #e0e0e0;
			border-left: 1px solid #e0e0e0;
			
			background: #fafafa;
			background: -webkit-gradient(linear, left top, left bottom, from(#fbfbfb), to(#fafafa));
			background: -moz-linear-gradient(top,  #fbfbfb,  #fafafa);
		}
		table tr.even td{
			background: #f6f6f6;
			background: -webkit-gradient(linear, left top, left bottom, from(#f8f8f8), to(#f6f6f6));
			background: -moz-linear-gradient(top,  #f8f8f8,  #f6f6f6);
		}
		table tr:last-child td{
			border-bottom:0;
		}
		table tr:last-child td:first-child{
			-moz-border-radius-bottomleft:3px;
			-webkit-border-bottom-left-radius:3px;
			border-bottom-left-radius:3px;
		}
		table tr:last-child td:last-child{
			-moz-border-radius-bottomright:3px;
			-webkit-border-bottom-right-radius:3px;
			border-bottom-right-radius:3px;
		}
		table tr:hover td{
			background: #f2f2f2;
			background: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#f0f0f0));
			background: -moz-linear-gradient(top,  #f2f2f2,  #f0f0f0);	
		}
		</style>
		</head>
		<body>
		<table cellspacing='0'>
			<tr>
				<th>No</th>
				<th>Filename</th>
				<th>Size</th>
				<th>Path</th>
				<th>Modified Time</th>
				<th>Accessed Time</th>
				<th>Creadted Time</th>
				<th>Entry Modified Time</th>
			</tr>
			<tr>
		'''
		html_footer = '''</tr>
		</table>
		</body>
		</html>'''
		
		html_file = "testestest.html"
		f = open(html_file, 'w')
		f.write(html_header)

		os.putenv('NLS_LANG', 'KOREAN_KOREA.KO16KSC5601')
		f.write(html_footer)

	#	for rows in :

	def save_view_on(self):
		#save

		#view
		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl(html_file))
		self.setCentralWidget(self.browser)


if __name__ == "__main__":
	global cnt
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()