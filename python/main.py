import sys


def main():
	if len(sys.argv) != 2:
		print "Incorrect usage. Use as follows:"
		print "python main.py <STOCK_NAME>"
		return
	stock = sys.argv[1]
	print "="*100
	print "FETCHING DATA FOR STOCK: " + stock
	print "="*100


if __name__ == "__main__":
	main()