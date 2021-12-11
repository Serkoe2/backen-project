import os
import re
from dotenv import load_dotenv
from smtplib import SMTP_SSL, SMTPConnectError, SMTPSenderRefused, SMTPServerDisconnected
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer():
	def __init__(self, server, port, email, password):
		self.server = server
		self.port = port
		self.email = email
		self.password = password
		self.__auth__()

	def __auth__(self):
		try:
			# Используется защищенное соединение
			self.conn = SMTP_SSL(self.server, self.port)
			# Настройка логгирования модуля
			self.conn.set_debuglevel(True)
			self.conn.login(self.email, self.password)
			# По умолчанию учавствует как способ авторизации 
			# в переборе способов авторизации в методе login
			# Рекомендую добавлять, если не работает login
			# self.conn.auth_plain(email, password)
		except SMTPConnectError:
			return (False, "SMTP connect Failed")

    # Метод подготовки шаблона к отправке
	def get_body(self, path, data):
		with open(path, 'r', encoding='UTF-8') as f:
			body = f.read()
		for i in data.keys():
			key = "{{" + i + "}}"
			body = re.sub(key, data[i], body)
		return body

    # Метод подготовки и отправки сообщения
    # to 			Указывается в формате email, например to@example.com
    # template_path	Путь к шаблону
    # data 			Набор пар ключ - значение для установки в шаблон
	def send(self, to: str, subject: str, template_path: str, data: dict) -> bool:
		try:
			msg = MIMEMultipart()
			msg['From'] = self.email
			msg['To'] = to
			msg['Subject'] = subject
			body = self.get_body(template_path, data)
			msg.attach(MIMEText(body, 'html', 'utf-8'))
			self.conn.send_message(msg)
			return True
		except SMTPServerDisconnected:
			self.__auth__()
			self.send(to, subject, template_path, data)
		except BaseException as e:
			print (e)
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