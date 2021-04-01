import argparse, json
import iptc
import filter_rule
chain_name = "OUTPUT"
DEFAULT_TARGET = "DROP"
def init_chain():
    filter_rule.flush_chain(chain_name)
    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
    try:
        chain.set_policy(iptc.Policy("ACCEPT"))
        return 0
    except Exception as e:
        print( e)
        print( "Table Error : table.strerror()")    
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Argument you need to know to add rule to firewall')
    parser.add_argument('--protocol', type=str, default=None,help='Protocol udp or tcp')
    parser.add_argument('--interface', type=str, default=None,help='Rule for which interface. Leave blank for all interface')
    parser.add_argument('--src-ip', type=str, help='IP range source')
    parser.add_argument('--dst-ip', type=str, help='IP range destination')
    parser.add_argument('--src-port', type=str, help='Port range source')
    parser.add_argument('--dst-port', type=str, help='Port range destination')
    parser.add_argument('--port',
                        type=str,
                        help='Port range for both source and destination')
    parser.add_argument('--ip',
                        type=str,
                        help='IP range for both source and destination')
    parser.add_argument('--comment',
                        '-m',
                        type=str,
                        help='Comment for the rule')
    parser.add_argument('--log',
                        '-l',
                        type=str,
                        help='Log prefix for the rule')

    parser.add_argument('-f',
                        '--flush',
                        action="store_true",
                        help='Clear all rule in this chain')
    args = parser.parse_args()
    if args.flush:
        init_chain()
        print( "All rules in %s chain is clear" % chain_name)

    else:
        rule_d = filter_rule.resolveArgsToDict(args)
        if args.log != None:
            rule_d["target"] = {"LOG":{"log-prefix":args.log}}
            filter_rule.append_rule(filter_rule.convertDictToRule(rule_d), chain_name)
        rule_d["target"] = DEFAULT_TARGET
        filter_rule.append_rule(filter_rule.convertDictToRule(rule_d), chain_name)
        table = iptc.Table(iptc.Table.FILTER)
        table.refresh()



if __name__ == "__main__":
    main()
    # init_chain()

