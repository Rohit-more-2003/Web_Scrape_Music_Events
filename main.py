import sqlite3
import requests
import selectorlib
import smtplib, ssl
import time

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

class Event:
	def scrape(self, url):
		"""Scrape the page source from the url"""
		response = requests.get(url, headers=HEADERS)
		
		source = response.text
		return source
	
	
	def extract(self, source):
		"""Extract the required information"""
		extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
		
		value = extractor.extract(source)["tours"]
		return value


class SendMail:
	def send_email(self, message):
		host = "smtp.gmail.com"
		port = 465
		
		username = "morer4851@gmail.com"
		password = "ifawvsfkxzlfaemw"
		
		receiver = "morer6776@gmail.com"
		context = ssl.create_default_context()
		
		with smtplib.SMTP_SSL(host, port, context=context) as server:
			server.login(username, password)
			server.sendmail(username, receiver, message)
			
		print("Email was sent!")
	

class Database:
	def __init__(self, db_path):
		self.connection = sqlite3.connect(db_path)
	
	
	def store(self, extracted):
		row = extracted.split(',')
		row = [item.strip() for item in row]
		
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
		self.connection.commit()
		
		
	def read(self, extracted):
		row = extracted.split(',')
		row = [item.strip() for item in row]
	
		cursor = self.connection.cursor()
		
		band, city, date = row
		cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
		rows = cursor.fetchall()
		print(rows)
		return rows


if __name__ == "__main__":
	while True:
		event = Event()
		scraped = event.scrape(URL)
		extracted = event.extract(scraped)
		print(extracted)
		
		if extracted != "No upcoming tours":
			db = Database('data.db')
			row = db.read(extracted)
			if not row:
				db.store(extracted)
				
				sm = SendMail()
				sm.send_email(message="Hey, discovered a new event!")
				
		time.sleep(2)