import requests

test_url = "http://blog.sina.com.cn/s/blog_5e3f971b0102v57i.html"
headers = {}
with open("downloaded", "wb") as f:
	r = requests.get(test_url, stream=True, headers = headers)
	print(r.status_code)
	print(r.headers)
	for chunk in r.iter_content(chunk_size = 1024):
		if chunk:
			f.write(chunk)
			f.flush()

import re
targets = check_output(["ls"]).decode("utf-8")

for file_name in targets.split('\n'):
    if re.match(r"\*\.csv", file_name):
        print(file_name)