import requests
import PyPDF2
import sys
import os
import re

from connection import session
from database_setup import DuesRecord

debug = True

def get_regex(course):
	if course == 'BTECH.pdf':
		return re.compile(r'B\d+\w{2}\s.+\s-?\d+')
	elif course == 'PhD.pdf':
		return re.compile(r'P\d+\w{2}\s.+\s-?\d+')
	else:
		return re.compile(r'M\d+\w{2}\s.+\s-?\d+')


def main():
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
			dues.close()

		pdf_file_obj = open(course, 'rb')
		pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
		total_pages = pdf_reader.numPages

		roll_rex = get_regex(course)
		
		for i in range(total_pages):
			page = pdf_reader.getPage(i)
			text = page.extractText()
			search_res = roll_rex.findall(text)

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

if __name__ == "__main__":
	main()
	sys.exit()
