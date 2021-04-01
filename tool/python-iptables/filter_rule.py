import iptc
import json
import re


def split_list_ports(listports):
    # print listports.split()
    return [s for s in re.findall(r'-?\d+\:?\d*', listports)][:15]


def read_rule_json(string_rule):
    """This function read json rule from input in command line and return a object rule can
    be use with other API"""

    # print type(rule), rule
    try:
        # test_inp = {'tcp': {'dport': '22'}, 'protocol': 'tcp', 'comment': {'comment': 'Match tcp.22'}, 'target': 'ACCEPT'}
        # print iptc.easy.encode_iptc_rule(test_inp)
        # print type(string_rule), string_rule
        rule = json.loads(string_rule, 'ascii')
        print(type(string_rule), string_rule)
        return iptc.easy.encode_iptc_rule(rule)
    except Exception as e:
        print(e)
        return 0


def print_all_rule():
    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        print("=======================")
        print("Chain:", chain.name, "Policy:", chain.get_policy().name)
        for rule in chain.rules:
            # print rule.name,"_"*32
            print(json.dumps(iptc.easy.decode_iptc_rule(rule), indent=4))
            # for match in rule.matches:
            # 	(packets, bytes) = rule.get_counters()
            # 	print packets, bytes, match.name, match.sport
    print("=======================")
def json_all_chain():
    table = iptc.Table(iptc.Table.FILTER)
    table_dict  = []
    for chain in table.chains:
        try:
            rules_dict = []
            for rule in chain.rules:
                rules_dict.append(iptc.easy.decode_iptc_rule(rule))
            chain_dict = dict(
                chain_name=chain.name,
                chain_policy=chain.get_policy().name,
                chain_rules=rules_dict
            )
            table_dict.append(chain_dict)
        except:
            continue
    return (json.dumps(table_dict, indent=4))
        

def json_all_rule():
    table = iptc.easy.dump_table(iptc.Table.FILTER)
    return json.dumps(table, indent=4)

# json_all_rule()


def json_rule_chain(chainname):
    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        if chain.name == chainname:
            dictchain = {}
            print("Chain:", chain.name, "Policy:", chain.get_policy().name)
            rules = []
            for rule in chain.rules:
                rules.append(iptc.easy.decode_iptc_rule(rule))
            dictchain[chain.name] = {
                'policy': chain.get_policy().name, 'rules': rules}
    return json.dumps(dictchain, indent=4)

# json_rule_chain("INPUT")


def flush_chain(chain):
    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain)
    try:
        chain.flush()
        table.refresh()
        print("Chain %s has been flushed!" % chain.name)
        return 0
    except Exception as e:
        print(e)
        print(table.strerror())
        return 1


def convertDictToRule(rule_d):
    try:
        return iptc.easy.encode_iptc_rule(rule_d)
    except Exception as e:
        print(e)
        return 1


def insert_rule(rule, chain, position=0):
    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain)

    try:
        chain.insert_rule(rule, position)

    except Exception as e:
        print(e)
        print(table.strerror())
        return 1
    table.refresh()
    return 0


def append_rule(rule, chain):
    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain)

    try:
        chain.append_rule(rule,)

    except Exception as e:
        print(e)
        print(table.strerror())
        return 1
    table.refresh()
    return 0


def delete_rule(position, chain):
    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain)

    try:
        rule = chain.rules[position]
        print(iptc.easy.decode_iptc_rule(rule))
        chain.delete_rule(rule)

    except Exception as e:
        print("Exception:", e)
        print(table.strerror())
        return 1
    table.refresh()
    return 0


def resolveArgsToDict(args):
    print(args)
# Add parameter about ports
    port = dict()
    if args.dst_port != None:
        port['dport'] = args.dst_port
    if args.src_port != None:
        port['sport'] = args.src_port
    if args.port != None:
        port['port'] = args.port
    # print(port)
# Add protocol to rule
    if args.protocol != None:
        if args.protocol.lower() == "udp":
            test_inp = {
                'udp': port,
                'protocol': 'udp'
            }

        elif args.protocol.lower() == "icmp":
            test_inp = {
                'protocol': 'icmp'
            }
        elif args.protocol.lower() == "tcp":
            test_inp = {
                'tcp': port,
                'protocol': 'tcp'
            }
    else:
        test_inp = {}
        return
# Comment parameter
    if args.comment != None:
        test_inp["comment"] = args.comment
# IP paramter
    iprange = dict()
    if args.src_ip != None:
        iprange["src-range"] = args.src_ip
    if args.dst_ip != None:
        iprange["dst-range"] = args.dst_ip
    if args.ip != None:
        iprange["src-range"] = args.ip
        iprange["dst-range"] = args.ip
    if len(iprange) > 0:	
        test_inp["iprange"] = iprange

    print(json.dumps(test_inp, indent=4))
    return test_inp
# delete_rule(1, "INPUT")


# def process(args):
# 	test_inp["target"] = "DROP"
# 	return convertDictToRule(test_inp)
