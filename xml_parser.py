'''
XMLParser takes a given url, downloads the file, parses the xml into csv.
'''
import argparse
import xml.etree.ElementTree
import logging
import unittest
import urllib2
import csv
from datetime import datetime

logger = logging.getLogger(__name__)

def setup_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--url-file", default='urls.txt', type=str)
	parser.add_argument("--csv-out", default='output.csv', type=str)
	parser.add_argument("--csv-out-dir", default='outputs', type=str)
	return parser.parse_args()

class XMLParser(object):
	'''
	base class that handles grabbing url data, 

	this is a pretty static object, it should injest configs to let it know what xml nodes to look for, etc
	'''
	def __init__(self, url, args):
		self.url = url
		self.args = args

	def get_url(self, url):
		try:
			data = urllib2.urlopen(url).read()
			return data
		except Exception as e:
			logger.error(e)

	def xml_to_objs(self, xml_data, object_xml_node, year, contains_word):
		'''
		parse the xml_data into the given csv format

		 - ideally you would add variables for day, month, year, contains_word(s), doesnt_contain_word(s), etc to make better queries.
		 - ideally you would also add a config file that would register the xml node names associated with the date query and the search string query.
		'''
		if not object_xml_node.startswith('.//'):
			object_xml_node = './/' + object_xml_node
		# TODO: remove this if its stupid.
		if isinstance(year, str) and isinstance(contains_word, str):
			et = xml.etree.ElementTree.fromstring(xml_data)
			objs = et.findall(object_xml_node)
			new_objs = []
			for obj in objs: # for listing in listings
				new_obj = {
					"MlsId": obj.findall(".//MlsId")[0].text,
					"MlsName": obj.findall(".//MlsName")[0].text,
					"DateListed": obj.findall(".//DateListed")[0].text,
					"StreetAddress": obj.findall(".//StreetAddress")[0].text,
					"Price": obj.findall(".//Price")[0].text,
					"Bedrooms": obj.findall(".//Bedrooms")[0].text,
					"Bathrooms": self.get_bathrooms(obj), # obj.findall(".//Bathrooms")[0].text,
					"Appliances": self.get_appliances(obj), #','.join( [ this_obj.text for this_obj in obj.findall(".//Appliances") ]),
					"Rooms": self.get_rooms(obj), #obj.findall(".//Rooms")[0].text,
					"Description": obj.findall(".//Description")[0].text
				}
				date = datetime.strptime(new_obj['DateListed'].split(' ')[0], '%Y-%m-%d')
				if str(date.year) == year:
					if contains_word.lower() in new_obj['Description'].lower():
						new_obj['Description'] = new_obj['Description'][:200]
						new_objs.append(new_obj)
						#print(new_obj)
			return sorted(new_objs, key=lambda item:item['DateListed'])
		else:
			import sys
			logger.error("you have entered an incorrect value for the year or the contains_word variable. Please make sure you use string variables.")
			sys.exit(1)

	def get_rooms(self, obj):
		return ','.join( [ str(room.text) for room in obj.findall(".//Room") ] )

	def get_appliances(self, obj):
		return ','.join( [ str(appliance.text) for appliance in obj.findall(".//Appliance") ] )

	def get_bathrooms(self, obj):
		baths = obj.findall(".//Bathrooms")[0].text
		full_baths = obj.findall(".//FullBathrooms")[0].text
		half_baths = obj.findall(".//HalfBathrooms")[0].text
		three_quarter_baths = obj.findall(".//ThreeQuarterBathrooms")[0].text
		return "Bathrooms:%s | FullBathrooms:%s | HalfBathrooms:%s | ThreeQuarterBathrooms:%s" % (str(baths),str(full_baths),str(half_baths),str(three_quarter_baths))
		
	def process_xml(self, xml_object, year, contains_word):
		data = self.get_url(url)
		objs = self.xml_to_objs(data, object_xml_node=xml_object, year=year, contains_word=contains_word)
		return objs

	def processed_xml_to_csv(self, processed_xml, filename):
		rows = processed_xml[0].keys()
		with open(filename, 'w') as w:
			dw = csv.DictWriter(w, rows)
			dw.writeheader()
			dw.writerows(processed_xml)

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
	for url in urls:
		if url.endswith('\n'):
			url = url.replace('\n','')
		xml_parser = XMLParser(urls, args)
		processed_xml = xml_parser.process_xml(xml_object="Listing", year='2016', contains_word='and')
		xml_parser.processed_xml_to_csv(processed_xml, "%s/%s.%s" % (args.csv_out_dir, url.split('/')[len(url.split('/'))-1], args.csv_out))

