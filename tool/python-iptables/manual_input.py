import argparse
import iptc
import filter_rule
chain = "INPUT"

def append_rule(input_rule):
	print("Append rule:")
	rule = filter_rule.read_rule_json(input_rule)
	print(rule)
	try:
		filter_rule.append_rule(rule, chain)
		return 0
	except Exception as e:
		print(e)
		return 1

def insert_rule(input_rule, position):
	print("Insert rule at :", position)
	rule = filter_rule.read_rule_json(input_rule)

	try:
		filter_rule.insert_rule(rule, chain, position)
		return 0
	except Exception as e:
		print(e)
		return 1

def main():
	parser = argparse.ArgumentParser(description='Argument you need to know to add rule to firewall')
	group1 = parser.add_mutually_exclusive_group()
	group2 = parser.add_mutually_exclusive_group()
	group3 = parser.add_mutually_exclusive_group()
	parser.add_argument('-I','--insert', type=int, help="""Insert rule in position. Default is location 0, the packet will face this rule first.
							Example : python manual_input.py -I 1 -r "{\"comment\": {\"comment\": \"1\"}, \"protocol\": \"tcp\", \"target\": \"ACCEPT\", \"tcp\": {\"dport\": \"22\"}}"
							""")
	parser.add_argument('-A','--append', action="store_true", help=r"""Insert rule in bottom of list (append). Your packet can face this rule after all other rules.
						Example : python manual_input.py -A -r "{\"comment\": {\"comment\": \"Match tcp.22\"}, \"protocol\": \"tcp\", \"target\": \"ACCEPT\", \"tcp\": {\"dport\": \"22\"}}"
						""")
	parser.add_argument('-r','--rule', required=False,type=str,default="", help='Input rule in json type.')
	parser.add_argument('-f','--flush', action="store_true", help='Clear all rule in this chain INPUT')
	parser.add_argument('-d','--delete',default=None, type=int, help='Delete specific rule in position of this chain INPUT. Default is the first')
	
	parser.add_argument('-L','--listrule', action="store_true", help='Get all rules in json type.')
	
	args = parser.parse_args()
	print(args)
	if args.listrule:
		# print(filter_rule.json_all_rule())
		print(filter_rule.json_all_chain())
		return()

	if args.flush:
		return filter_rule.flush_chain(chain)

	if args.delete != None:
		print("Delete at", args.delete)
		filter_rule.delete_rule(args.delete, chain)
	else:
		if args.append:
			append_rule(args.rule)

		elif args.insert >= 0 and args.insert != None:
			insert_rule(args.rule, args.insert)
		else:
			pass



	# print(args)
if __name__ == "__main__":
	main()

