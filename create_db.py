import binascii
import ConfigParser
import datetime
import os
import re
import sys

import PyPDF2
import requests

from connection import session
from database_setup import DuesRecord

debug = False
date = ''
month = ''
year = ''

def get_regex(course):
	if course == 'BTECH.pdf':
		return re.compile(r'B\d+\w{2}\s.+\s-?\d+')
	elif course == 'PhD.pdf':
		return re.compile(r'P\d+\w{2}\s.+\s-?\d+')
	else:
		return re.compile(r'M\d+\w{2}\s.+\s-?\d+')


def parsePDFs():
	URL = 'http://www.nitc.ac.in/app/webroot/img/upload/'
	COURSE = ['BTECH.pdf', 'PG.pdf', 'PhD.pdf']
	session.query(DuesRecord).delete()
	session.commit()
	for course in COURSE:
		if not debug:
			res = requests.get(URL+course)
			dues = open(course, 'wb')
			for chunk in res.iter_content(100000):
				dues.write(chunk)
			dues.write(bin(int(binascii.hexlify("%%EOF"),16)))
			dues.close()

		pdf_file_obj = open(course, 'rb')
		pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
		total_pages = pdf_reader.numPages

		roll_rex = get_regex(course)
		
		for i in range(total_pages):
			page = pdf_reader.getPage(i)
			text = page.extractText()
			search_res = roll_rex.findall(text)

			if i == 0:
				global date
				global month
				global year
				monthDict = { 'JANUARY':'1','FEBRUARY':'2','MARCH':'3',
								'APRIL':'4','MAY':'5','JUNE':'6','JULY':'7',
								'AUGUST':'8','SEPTEMBER':'9','OCTOBER':'10',
								'NOVEMBER':'11','DECEMBER':'12'}
				lines = text.split('\n')
				for line in lines:
					if 'Payment' in line:
						wordsInLine = line.split()
						date = wordsInLine[3].replace("th","")
						month = monthDict[wordsInLine[4].upper()]
						year = wordsInLine[5].replace(")","")

			for res in search_res:
				r = res.split('\n')
				roll, name, due = r[0],r[1],r[2]
				try:
					roll = roll.encode('ascii')
					name = name.encode('ascii','ignore')
					due = due.encode('ascii')
				except:
					sys.exit('An error has occurred')
				session.add(DuesRecord(roll_no=roll, name=name, due=int(due)))
		session.commit()

def updateConfig():
	config = ConfigParser.ConfigParser()
	now = datetime.datetime.now()
	config.add_section('Last_Update')
	config.set('Last_Update','date',now.day)
	config.set('Last_Update','month',now.month)
	config.set('Last_Update','year',now.year)
	config.add_section('Last_Payment_Update')
	config.set('Last_Payment_Update','date',date)
	config.set('Last_Payment_Update','month',month)
	config.set('Last_Payment_Update','year',year)
	with open('config.ini','w') as configFile:
		config.write(configFile)

def main():
	parsePDFs()
	updateConfig()

if __name__ == "__main__":
	main()
