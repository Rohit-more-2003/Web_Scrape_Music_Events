import requests
import selectorlib # Used to get data from the string format of the web page

URL = "http://programmer100.pythonanywhere.com/tours/"
# Sometimes some web pages do not get scrapped, so HEADERS is given so that page behaves as web page and is scrapped
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def scrape(url):
	"""Scrape the page source from the url"""
	response = requests.get(url, headers=HEADERS)
	
	source = response.text # returns web page in html.text format
	return source


def extract(source):
	"""Extract the required information"""
	extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
	
	value = extractor.extract(source)["tours"]
	return value


def send_email():
	print("Email was sent.")
	

def store(extracted, filepath):
	with open(filepath, "a") as file:
		file.write(extracted + '\n')
		
		
def read(filepath):
	with open(filepath, 'r') as file:
		return file.read()


if __name__ == "__main__":
	scraped = scrape(URL)
	extracted = extract(scraped)
	print(extracted)
	
	if extracted != "No upcoming tours": # There is tour!
		filepath = "data.txt"
		content = read(filepath)
		if extracted not in content: # Which is not already saved
			store(extracted, filepath)
			send_email()