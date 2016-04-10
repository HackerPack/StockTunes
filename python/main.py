import sys
import extract_data as ed
import beat_box
import github_sync


def main():
	if len(sys.argv) != 2:
		print "Incorrect usage. Use as follows:"
		print "python main.py <STOCK_NAME>"
		return
	stock = sys.argv[1].lower()
	print "="*100
	print "FETCHING DATA FOR STOCK: " + stock
	print "="*100
	data = ed.extract_data(stock)
	print
	print

	print "="*100
	print "GENERATING AUDIO FILE"
	print "="*100
	beat_box.generate(stock, data)
	print
	print

	print "="*100
	print "PUSHING TO GITHUB"
	print "="*100
	github_sync.sync_with_github()
	print
	print

	print "="*100
	print "DONE :)"
	print "="*100


if __name__ == "__main__":
	main()