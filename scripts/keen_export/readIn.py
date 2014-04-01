#imports
from keen.client import KeenClient
import re
import json
from pprint import pprint
import sys
from urlparse import urlparse
from urlparse import parse_qsl
from formatter import formatter


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)


### note 
keen = KeenClient(
	project_id="531cd14e73f4bb0e96000000",
	write_key="087a3f15e84fdece4fdd7e97e89bf48ecf219bb5908b65a8472c30311793a160d6ece270864c61496513094ab3e493bd9dbe41548bcd434e31f2c1bd6d3e601e98584503c8b32ae9443f3c7f0a09ec1ebfdce8965261b92268bee1a0c363126309c592d1f3d3c141b67ad6894e6b2f16",
	read_key="243c0b51c203216621d2d93182345e01a68c40837809ad800332f8b675fec35d46312198861bd646114b6229c840928410ba55974b3d899b92dd763bae2caaf80f2bb79479e0dc18b1da8de6a3f74b7097e0a6861407060ba85818de5d7dd9df02164748f5d7d09d8a77f67d0ef95974"
)
input_file='input'

############### BASIC PARSING

f = open(input_file, 'r')
for line in f:
	if formatter.isPingData(line):
		data=formatter.formatPingData(line)
		prettyString=json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
		w = open('output', 'w+')
		w.write(prettyString)
		break;
	elif formatter.isRequestData(line):
		data=formatter.formatRequestData(line)
		prettyString=json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
		w = open('output', 'w+')
		w.write(prettyString)
		break;
