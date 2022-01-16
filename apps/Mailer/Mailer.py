import os
import re
from typing import Tuple
from dotenv import load_dotenv
from smtplib import (
	SMTP_SSL, 
	SMTPConnectError,  
	SMTPServerDisconnected
)
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer():
	def __init__(self, server: str, port: str, email: str, password: str)->None:
		"""
		server - url SMTP сервера

		port - номер порта сервера
        """
		self.server = server
		self.port = port
		self.email = email
		self.password = password
		self.__auth__()

	def __auth__(self)->Tuple:
		try:
			self.conn = SMTP_SSL(self.server, self.port)
			#self.conn.set_debuglevel(True)
			self.conn.login(self.email, self.password)
			# self.conn.auth_plain(email, password)
			return (True, "SMTP connect OK")
		except SMTPConnectError:
			return (False, "SMTP connect Failed")

	def get_body(self, path, data)->str:
		"""
		Метод подготовки шаблона к отправке
		"""
		with open(path, 'r', encoding='UTF-8') as f:
			body = f.read()
		for i in data.keys():
			key = "{{" + i + "}}"
			body = re.sub(key, data[i], body)
		return body

	def send(self, to: str, subject: str, template_path: str, data: dict)->Tuple:
		"""
		to 			Указывается в формате email, например to@example.com

		template_path	Путь к шаблону

		data 			Набор пар ключ - значение для установки в шаблон
		"""
		try:
			msg = MIMEMultipart()
			msg['From'] = self.email
			msg['To'] = to
			msg['Subject'] = subject
			body = self.get_body(template_path, data)
			msg.attach(MIMEText(body, 'html', 'utf-8'))
			self.conn.send_message(msg)
			return (True, "Message send")
		# Если приложение разлогинено, мы заново выполняем авторизацию
		except SMTPServerDisconnected:
			self.__auth__()
			self.send(to, subject, template_path, data)
		except BaseException as e:
			return (False, e)

if __name__ == '__main__':
	# Get the path to the directory this file is in
	BASEDIR = (os.path.dirname(os.path.dirname(__file__)))
	# Connect the path with your '.env' file name
	load_dotenv(os.path.join(BASEDIR, 'test.env'))
	data = {"url": "https://google.com", "code":"12345"}
	mail = Mailer(
		os.getenv("SMTP_SERVER"),
		os.getenv("SMTP_PORT"),
		os.getenv("SMTP_LOGIN"),
		os.getenv("SMTP_PASSWORD"))
	mail.send("timoha-john@yandex.ru", "TEST", "template2.html", data)