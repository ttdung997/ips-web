import iptc, json
# table = iptc.Table(iptc.Table.FILTER)
# rule = iptc.Rule()
# rule.protocol = "tcp"
# rule.in_interface = "ens38"
# rule.scr = "192.168.1.10"
# match = iptc.Match(rule, "tcp")
# match.dport = "80"
# rule.add_match(match)
# match = iptc.Match(rule, "iprange")
# match.src_range = "192.168.1.10-192.168.1.200"
# rule.add_match(match)
# match = iptc.Match(rule, "tcp")
# match.in_interface = "ens38"
# chain = "INPUT"
# for chain in table.chains:
#     print("=======================")
#     print("Chain:", chain.name, "Policy:", chain.get_policy().name)
#     for rule in chain.rules:
        # print rule.name,"_"*32
#         print(json.dumps(iptc.easy.decode_iptc_rule(rule), indent=4))
# print(iptc.easy.decode_iptc_rule)
# rule.target = rule.create_target("LOG")
# chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
# chain.insert_rule(rule)

# print("Rule imported:\n", iptc.easy.decode_iptc_rule(rule))
# table.commit()
# table.autocommit = True
rule_d = {'conntrack': {'ctstate': 'ESTABLISHED,RELATED'}, 'target': 'ACCEPT'}
# iptc.easy.add_rule('filter', 'INPUT', rule_d, ipv6=False)
# iptc.easy.add_rule('filter', 'INPUT', rule_d, ipv6=True)
# iptc.easy.add_rule('filter', 'INPUT', rule_d, ipv6=False)
print(json.dumps(iptc.easy.dump_chain('filter', input, ipv6=True), indent=4))

# json.dumps(iptc.easy.dump_table('filter', ipv6=False), indent=4)