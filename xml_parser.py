'''
XMLParser takes a given url, downloads the file, parses the xml into csv.
'''
import argparse
import xml.etree.ElementTree
import logging
import unittest
import urllib2
import os

import xmltodict

logger = logging.getLogger(__name__)

def setup_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--url-file", default='urls.txt', type=str)
	parser.add_argument("--csv-out", default='output.csv', default=str)
	parser.add_argument("--csv-out-dir", default='outputs', default=str)
	return parser.parse_args()

class XMLParser(object):
	'''
	base class that handles grabbing url data, 

	this is a pretty static object, it should injest configs to let it know what xml nodes to look for, etc
	'''
	def __init__(self, urls, args):
		self.urls = urls
		self.args = args

	def get_url(self, url):
		try:
			data = urllib2.urlopen(url)
			return data
		except Excpetion as e:
			logger.error(e)

'''
- Required fields:
	- MlsId
	- MlsName
	- DateListed
	- StreetAddress
	- Price
	- Bedrooms
	- Bathrooms
	- Appliances (all sub-nodes comma joined)
	- Rooms (all sub-nodes comma joined)
	- Description (the first 200 characters)
'''

	def xml_to_csv(self, xml_data, object_xml_node, year, contains_word):
		'''
		parse the xml_data into the given csv format

		 - ideally you would add variables for day, month, year, contains_word(s), doesnt_contain_word(s), etc to make better queries.
		 - ideally you would also add a config file that would register the xml node names associated with the date query and the search string query.
		'''
		if not object_xml_node.startswith('.//'):
			object_xml_node = './/' + object_xml_node
		if isinstance(year, str) and isinstance(contains_word, str):
			et = xml.etree.ElementTree.fromstring(xml_data)
			objs = et.findall(object_xml_node)
			for obj in objs:
				new_obj = {
					"MlsId": obj,
					"MlsName":,
					"DateListed":,
					"StreetAddress":,
					"Price":,
					"Bedrooms":,
					"Bathrooms":,
					"Appliances":,
					"Rooms":,
					"Description":,
				}
		else:
			import sys
			logger.error("you have entered an incorrect value for the year or the contains_word variable. Please make sure you use string variables.")
			sys.exit(1)

	def process_xml(self, year, contains_word):
		if not os.path.isdir(self.args.csv_out_dir):
			os.mkdir(self.args.csv_out_dir)
		processed_data = []
		for url in self.urls:
			data = self.get_url(url)
			csv = self.xml_to_csv(data, object_xml_node='Listing', year=year, contains_word=contains_word)
			processed_data.append(csv)
		processed_data = sort_processed_data_by_date(processed_data)
		for data in processed_data:
			w = open('%s_%s' % (str(n), self.args.csv_out), 'w')
			w.write(csv)
			w.close()

class TestXMLParser(unittest.TestCase):
	def setUp(self):
		self.urls_file = "urls.txt"

	def tearDown(self):
		pass

	def test_create_xml_parser(self):
		self.assertEqual(1, 1)

if __name__ == "__main__":
	args = setup_args()
	urls = [ url for url in open(args.url_file, 'r').readlines() ]
	xml_parser = XMLParser(urls, args)
	xml_parser.process_xml(year='2016', contains_word='and')

