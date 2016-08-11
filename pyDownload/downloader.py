"""
# inspired by py-wget module.
# url -> "https://github.com/phith0n/py-wget/blob/master/py-wget.py"
# Adding multiple thread control and more functions.
"""


import requests
import re
import os
import time
test_url = "https://github.com/phith0n/py-wget/blob/master/py-wget.py"
task_url = "http://nchc.dl.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz"
class Downloader(object):

	def __init__(self, config = {}):

		self.config = {
			'block': int(config['block'] if 'block' in config else 10240)
		}
		self.total = 0
		self.size = 0
		self.filename = ''


	def download(self, url, headers = {}):
		finished = False
		block = self.config['block']

		local_filename = url.rsplit("/")[-1]
		size = self.size
		total = self.total
		temp_filename = "size_tmp_" + local_filename

		

		# Getting file size #
		self.support_continue(url)
		try:
			with open(temp_filename, "rb") as f:
				self.size = int(f.read())
				print("Current size is: {0}".format(self.size))
				size = self.size+1
		except Exception as e:
			print(e)
			with open(temp_filename, "wb") as f:
				pass
		finally:
			headers['Range'] = "bytes=%d-" % (self.size, )
		# else:
		# 	print("Continue: Not supported.")
		# 	headers['Range'] = "bytes=%d-" % (self.size, )
		# 	self.size = 0

		# Done getting file size #
		# ---------------- #
		# Get file size #

		r = requests.get(url, stream=True, headers = headers)

		if self.total > 0:
			print(" [+] Size: {0}KB".format(total/10240))
		else:
			print(" [+] Size: None")

		# Done getting file size #
		# ---------------- #
		# Open the target file #

		start_t = time.time()
		with open(local_filename, 'ab+') as f:
			f.seek(self.size)
			f.truncate()

			try:
				for chunk in r.iter_content(chunk_size = block):
					if chunk:
						f.write(chunk)
						size += len(chunk)
						f.flush()
					print('\b * 64' + 'Now: {0}, Total {1}'.format(size, self.total))
				finished = True
				if (os.path.exists(temp_filename)):
					os.remove(temp_filename)
				spend = int(time.time() - start_t)
				speed = int((size - self.size) / 10240 / (spend+0.01))
				print("Download finished with speed {0}KB/s".format(speed))
			except Exception as e:
				print(e)
				print("Download paused")
			finally:
				if not finished:
					with open(temp_filename, 'w+') as ftmp:
						ftmp.write((str(size)))

	def support_continue(self, url):

		headers = {
			"Range": "bytes=0-4"
		}

		try:
			r = requests.head(url, headers = headers)
			print(r.headers)
			crange = r.headers['Content-Range']
			self.total = int(re.match(r'^bytes 0-4/(\d+)$', crange).group(1))
			return True
		except Exception as e:
			print(e)
			pass

		try:
			self.total = int(r.headers['content-length'])
		except Exception as e:
			print(e)
			self.total = 0
		return False

d = Downloader()
d.download(task_url)