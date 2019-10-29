import shelve
import sys

from .create_db import main as update_database


def main():
	INR = u"\u20B9"

	ip = input('Update the database? - (Y/N) : ')
	if ip.upper() == 'Y':
		update_database()
		print('Updated...')
		print()

	dues_list = shelve.open('dues')
	while True:
		try:
			print()
			roll_no = input('Enter roll no: ')
			print()
			roll_no = roll_no.upper()
			if roll_no in dues_list:
				print("Name:", dues_list[roll_no][0])
				print("Dues: " + INR + " ", dues_list[roll_no][1], "/-", sep='')
				print()
			else:
				print("Invalid Roll Number!", end='\n')
				print()
		except:
			print()
			print('Exiting...')
			sys.exit()


if __name__ == "__main__":
	main()
	sys.exit()
# hacktoberfest
