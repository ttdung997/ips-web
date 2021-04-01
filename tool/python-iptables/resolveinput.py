import re, json
import iptc

def split_list_ports(listports):
	# print( listports.split())
	return [s for s in re.findall(r'-?\d+\:?\d*', listports)][:15]

def read_rule_json(string_rule):
	"""This function read json rule from input in command line and return a object rule can
	be use with other API"""
	
	# print( type(rule), rule)
	try:
		# test_inp = {'tcp': {'dport': '22'}, 'protocol': 'tcp', 'comment': {'comment': 'Match tcp.22'}, 'target': 'ACCEPT'}
		# print iptc.easy.encode_iptc_rule(test_inp)
		# print type(string_rule), string_rule
		rule = json.loads(string_rule, 'ascii')
		print( type(string_rule), string_rule)
		return iptc.easy.encode_iptc_rule(rule)
	except Exception as e:
		print( e)
		return 0
	# return iptc.easy.encode_iptc_rule(string_rule)



# print split_list_ports("22,xxxasdasd24:68,67,55,1,2,3,4,5,6,78888.112,8,9,0,1,2,34,5,6,74,34,45,6,64")