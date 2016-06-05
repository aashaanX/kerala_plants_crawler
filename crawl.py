import requests
from bs4 import BeautifulSoup as bs

url = 'http://keralaplants.in/exotic-plants-kerala.aspx'

def releventLinks(url):
	r = requests.get(url)
	soup = bs(r.content,'html5lib')
	href_link = []
	for link in soup.find_all('a'):
		href_link.append(link.get('href'))
	data_links = list(filter(lambda x: 'keralaplantsdetails.aspx?id=' in str(x),href_link))
	return data_links

def dataExtract(url):
	r = requests.get(url)
	soup = bs(r.content,'html5lib')
	string = ''
	print("image url :/http://keralaplants/"+soup.find_all('img')[1]['src']) 
	for link in soup.find_all('span'):
		print(link.text)
data_link = releventLinks(url)
for i in data_link:
	url = 'http://keralaplants.in/'+i
	print(url)
	dataExtract(url)
	print('*****************************************')
