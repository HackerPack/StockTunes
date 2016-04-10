from bs4 import BeautifulSoup
from lxml import html
import requests
import urllib2

def extract_data(code):

	p = urllib2.urlopen('http://www.nasdaq.com/symbol/'+code+'/historical').read()
	page = BeautifulSoup(p)
	page.prettify()

	div = page.find(id="historicalContainer")

	tables = div.find_all('table')

	for table in tables:
		tr_tags = table.find_all('tr')

	val=[]
	date = []

	count=0
	for tr_tag in tr_tags:
		if count > 1:
			count1=0
			td_tags = tr_tag.find_all('td')
			for td_tag in td_tags:
				if count1 == 4:
					val.append(str(td_tag.string.strip()))
				if count1 == 0:
					date.append(str(td_tag.string.strip()))
				count1=count1+1
		count=count+1

	return {"data": val, "date": date}
